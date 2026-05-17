import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import logging
import yaml
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import pytest
from torch.utils.data import Dataset, DataLoader
import wandb
from tqdm import tqdm
from transformers import LlamaForCausalLM, LlamaTokenizer
from torch.distributions import Categorical
from nltk.translate.bleu_score import sentence_bleu

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Config:
    """Configuration management"""
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self._validate_config()
    
    def _validate_config(self):
        required_fields = [
            'vocab_size', 'random_input_dim', 'learning_rate',
            'batch_size', 'num_epochs', 'max_length', 'llama_model_path',
            'distill_epochs'
        ]
        for field in required_fields:
            if field not in self.config:
                raise ValueError(f"Missing required config field: {field}")
    
    def save(self, path: str):
        with open(path, 'w') as f:
            yaml.dump(self.config, f)

class TextDataset(Dataset):
    def __init__(self, texts, random_data, tokenizer, max_length):
        self.texts = texts
        self.random_data = random_data
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        random_input = self.random_data[idx]
        
        tokens = self.tokenizer.encode(
            text,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': tokens,
            'random_input': torch.tensor(random_input, dtype=torch.float32)
        }

class MappingLayer(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, dropout=0.1):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.Dropout(dropout),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.Dropout(dropout),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )
    
    def forward(self, x):
        return self.network(x)

class MovingAverageBaseline:
    def __init__(self, decay=0.99):
        self.decay = decay
        self.value = 0
    
    def update(self, reward):
        self.value = self.decay * self.value + (1 - self.decay) * reward
        return self.value

class TransformerWithRL(nn.Module):
    def __init__(self, 
                 vocab_size,
                 random_input_dim,
                 d_model=512,
                 nhead=8,
                 num_encoder_layers=6,
                 num_decoder_layers=6,
                 dropout=0.1):
        super().__init__()
        
        self.mapping = MappingLayer(random_input_dim, d_model, d_model, dropout)
        
        self.transformer = nn.Transformer(
            d_model=d_model,
            nhead=nhead,
            num_encoder_layers=num_encoder_layers,
            num_decoder_layers=num_decoder_layers,
            dropout=dropout
        )
        
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.positional_encoding = self.create_positional_encoding(5000, d_model)
        self.output_layer = nn.Linear(d_model, vocab_size)
        
        # RL components
        self.saved_log_probs = []
        self.rewards = []
        self.baseline = MovingAverageBaseline()
        
        # Initialize weights
        self.apply(self._init_weights)
    
    def _init_weights(self, module):
        if isinstance(module, (nn.Linear, nn.Embedding)):
            module.weight.data.normal_(mean=0.0, std=0.02)
            if isinstance(module, nn.Linear) and module.bias is not None:
                module.bias.data.zero_()
    
    def create_positional_encoding(self, max_seq_length, d_model):
        position = torch.arange(max_seq_length).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-np.log(10000.0) / d_model))
        pos_encoding = torch.zeros(max_seq_length, d_model)
        pos_encoding[:, 0::2] = torch.sin(position * div_term)
        pos_encoding[:, 1::2] = torch.cos(position * div_term)
        return pos_encoding
    
    def forward(self, random_input, target_text=None):
        mapped_input = self.mapping(random_input)
        src = mapped_input + self.positional_encoding[:mapped_input.size(0)]
        
        if target_text is not None:
            tgt = self.embedding(target_text) + self.positional_encoding[:target_text.size(0)]
            tgt_mask = nn.Transformer.generate_square_subsequent_mask(target_text.size(0))
            output = self.transformer(src, tgt, tgt_mask=tgt_mask)
        else:
            output = self.transformer.encoder(src)
        
        return self.output_layer(output)
    
    def select_action(self, random_input, temperature=1.0):
        logits = self(random_input)
        probs = torch.softmax(logits / temperature, dim=-1)
        m = Categorical(probs)
        action = m.sample()
        self.saved_log_probs.append(m.log_prob(action))
        return action

class DistillationLoss(nn.Module):
    def __init__(self, temperature=2.0):
        super().__init__()
        self.temperature = temperature
        self.kl_div = nn.KLDivLoss(reduction='batchmean')
    
    def forward(self, student_logits, teacher_logits):
        soft_student = torch.log_softmax(student_logits / self.temperature, dim=-1)
        soft_teacher = torch.softmax(teacher_logits / self.temperature, dim=-1)
        return self.kl_div(soft_student, soft_teacher) * (self.temperature ** 2)

class LlamaDistillationTrainer:
    def __init__(self, student_model, device, teacher_model_path):
        self.student = student_model
        self.device = device
        
        self.teacher = LlamaForCausalLM.from_pretrained(teacher_model_path)
        self.teacher.eval()
        self.teacher.to(device)
        
        self.tokenizer = LlamaTokenizer.from_pretrained(teacher_model_path)
        self.distill_loss = DistillationLoss()
    
    def distill_step(self, batch, optimizer):
        optimizer.zero_grad()
        
        with torch.no_grad():
            teacher_logits = self.teacher(batch['input_ids']).logits
        
        student_logits = self.student(batch['random_input'])
        loss = self.distill_loss(student_logits, teacher_logits)
        
        loss.backward()
        optimizer.step()
        
        return loss.item()

class Trainer:
    def __init__(self, model, optimizer, train_loader, val_loader, device):
        self.model = model
        self.optimizer = optimizer
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.device = device
        
        wandb.init(project="transformer-rl", config={
            "learning_rate": optimizer.param_groups[0]['lr'],
            "architecture": "TransformerWithRL",
            "dataset": "custom"
        })
    
    def compute_advantage(self, rewards):
        advantages = []
        for r in rewards:
            advantage = r - self.model.baseline.value
            self.model.baseline.update(r)
            advantages.append(advantage)
        return torch.tensor(advantages)
    
    def train_epoch(self, reward_fn):
        self.model.train()
        total_loss = 0
        
        for batch in self.train_loader:
            random_input = batch['random_input'].to(self.device)
            target_text = batch['input_ids'].to(self.device)
            
            loss = self.train_step(random_input, target_text, reward_fn)
            total_loss += loss
            
            wandb.log({
                "batch_loss": loss,
                "reward": np.mean(self.model.rewards)
            })
        
        return total_loss / len(self.train_loader)
    
    def train_step(self, random_input, target_text, reward_fn):
        self.optimizer.zero_grad()
        
        action = self.model.select_action(random_input)
        reward = reward_fn(action, target_text)
        self.model.rewards.append(reward)
        
        advantages = self.compute_advantage(self.model.rewards)
        
        policy_loss = []
        for log_prob, advantage in zip(self.model.saved_log_probs, advantages):
            policy_loss.append(-log_prob * advantage)
        policy_loss = torch.cat(policy_loss).sum()
        
        # Add entropy bonus
        probs = torch.softmax(self.model.output_layer.weight, dim=-1)
        entropy = -(probs * torch.log(probs + 1e-10)).sum(-1).mean()
        loss = policy_loss - 0.01 * entropy
        
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
        self.optimizer.step()
        
        self.model.rewards = []
        self.model.saved_log_probs = []
        
        return loss.item()
    
    @torch.no_grad()
    def validate(self, reward_fn):
        self.model.eval()
        total_reward = 0
        
        for batch in self.val_loader:
            random_input = batch['random_input'].to(self.device)
            target_text = batch['input_ids'].to(self.device)
            
            generated = self.model.select_action(random_input)
            reward = reward_fn(generated, target_text)
            total_reward += reward
        
        return total_reward / len(self.val_loader)

class ModelCheckpoint:
    def __init__(self, save_dir: str):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
    
    def save(self, model, optimizer, epoch, metrics, filename=None):
        if filename is None:
            filename = f"checkpoint_epoch_{epoch}.pt"
        
        checkpoint = {
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'epoch': epoch,
            'metrics': metrics
        }
        
        path = self.save_dir / filename
        torch.save(checkpoint, path)
        logger.info(f"Saved checkpoint to {path}")
    
    def load(self, path, model, optimizer=None):
        checkpoint = torch.load(path)
        model.load_state_dict(checkpoint['model_state_dict'])
        
        if optimizer is not None:
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        
        return checkpoint['epoch'], checkpoint['metrics']

def main():
    try:
        # Load configuration
        config = Config('config.yaml')
        
        # Initialize model and components
        model = TransformerWithRL(
            vocab_size=config.config['vocab_size'],
            random_input_dim=config.config['random_input_dim']
        ).to(config.config['device'])
        
        optimizer = optim.AdamW(
            model.parameters(),
            lr=config.config['learning_rate'],
            weight_decay=0.01
        )
        
        scheduler = optim.lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=config.config['num_epochs']
        )
        
        # Initialize distillation trainer
        distillation_trainer = LlamaDistillationTrainer(
            student_model=model,
            device=config.config['device'],
            teacher_model_path=config.config['llama_model_path']
        )
        
        # Initialize checkpoint handler
        checkpointer = ModelCheckpoint('checkpoints')
        
        # Phase 1: Knowledge Distillation
        logger.info("Starting knowledge distillation phase...")
        for epoch in tqdm(range(config.config['distill_epochs'])):
            try:
                distill_loss = distillation_trainer.distill_step(batch, optimizer)
                logger.info(f"Distillation epoch {epoch}, loss: {distill_loss}")
            except Exception as e:
                logger.error(f"Error during distillation epoch {epoch}: {e}")
                continue
        
        # Phase 2: RL Training
        logger.info("Starting RL training phase...")
        trainer = Trainer(
            model=model,
            optimizer=optimizer,
            train_loader=train_loader,
            val_loader=val_loader,
            device=config.config['device']
        )
        
        def reward_fn(predicted_text, target_text):
            return torch.tensor(sentence_bleu([target_text], predicted_text))
        
        best_reward = float('-inf')
        for epoch in tqdm(range(config.config['num_epochs'])):
            try:
                train_loss = trainer.train_epoch(reward_fn)
                val_reward = trainer.validate(reward_fn)
                
                scheduler.step()
                
                # Log metrics
                wandb.log({
                    "epoch": epoch,
                    "train_loss": train_loss,
                    "val_reward": val_reward,
                    "learning_rate": scheduler.get_last_lr()[0]
                })
                
                # Save best model
                if val_reward > best_reward:
                    best_reward = val_reward
                    checkpointer.save(
                        model,
                        optimizer,
                        epoch,
                        {
                            "train_loss": train_loss,
                            "val_reward": val_reward
                        },
                        "best_model.pt"
                    )
                
                logger.info(f"Epoch {epoch}: Train Loss = {train_loss:.4f}, Val Reward = {val_reward:.4f}")
                
            except Exception as e:
		logger.error(f"Error during training epoch {epoch}: {e}")
                continue
        
        # Save final model
        try:
            torch.save(model.state_dict(), 'final_model.pt')
            config.save('final_config.yaml')
        except Exception as e:
            logger.error(f"Error saving final model: {e}")
        
        # Clean up
        wandb.finish()
        
    except Exception as e:
        logger.error(f"Fatal error in training: {e}")
        raise

if __name__ == "__main__":
    # Run tests before training
    pytest.main([__file__])
    
    # Start training
    main()