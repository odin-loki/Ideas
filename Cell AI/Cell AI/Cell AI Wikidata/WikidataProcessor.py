import json
import os
import argparse
import requests
from tqdm import tqdm
import gzip
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_wikidata_dump(output_dir='./wikidata_dumps', dump_url=None):
    """
    Download the latest Wikidata JSON dump or use provided URL
    """
    os.makedirs(output_dir, exist_ok=True)
    
    if dump_url is None:
        # Default to a small recent dump if no URL provided
        dump_url = "https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.gz"
    
    output_path = os.path.join(output_dir, os.path.basename(dump_url))
    
    if os.path.exists(output_path):
        logging.info(f"Dump file already exists at {output_path}, skipping download")
        return output_path
    
    logging.info(f"Downloading Wikidata dump from {dump_url}")
    
    # Download with progress bar
    response = requests.get(dump_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(output_path, 'wb') as f:
        for chunk in tqdm(response.iter_content(chunk_size=1024*1024), 
                         total=total_size // (1024*1024), 
                         unit='MB',
                         desc="Downloading"):
            if chunk:
                f.write(chunk)
    
    logging.info(f"Downloaded Wikidata dump to {output_path}")
    return output_path

def process_wikidata_dump(dump_path, output_path, max_items=100000, language='en'):
    """
    Process Wikidata JSON dump and extract text data for training
    
    Args:
        dump_path: Path to the Wikidata dump file (.json.gz)
        output_path: Path to save the processed data
        max_items: Maximum number of items to process
        language: Language code for extracting labels and descriptions
    """
    logging.info(f"Processing Wikidata dump: {dump_path}")
    logging.info(f"Extracting up to {max_items} items with language: {language}")
    
    count = 0
    
    with gzip.open(dump_path, 'rt', encoding='utf-8') as f_in:
        with open(output_path, 'w', encoding='utf-8') as f_out:
            # Skip first line which is just an opening bracket
            next(f_in)
            
            for line in tqdm(f_in, desc="Processing entities"):
                # Remove trailing comma if present
                if line.endswith(',\n'):
                    line = line[:-2]
                
                # Skip last line which is just a closing bracket
                if line.strip() == ']':
                    continue
                
                try:
                    entity = json.loads(line)
                    
                    # Extract data for the specified language
                    text_data = {}
                    
                    # Get label
                    if 'labels' in entity and language in entity['labels']:
                        text_data['label'] = entity['labels'][language]['value']
                    
                    # Get description
                    if 'descriptions' in entity and language in entity['descriptions']:
                        text_data['description'] = entity['descriptions'][language]['value']
                    
                    # Get aliases
                    if 'aliases' in entity and language in entity['aliases']:
                        text_data['aliases'] = [alias['value'] for alias in entity['aliases'][language]]
                    
                    # Get claims (P-values) with their labels when available
                    if 'claims' in entity:
                        claims = []
                        for prop, claim_list in entity['claims'].items():
                            for claim in claim_list:
                                if 'mainsnak' in claim and 'datavalue' in claim['mainsnak']:
                                    if 'value' in claim['mainsnak']['datavalue']:
                                        value = claim['mainsnak']['datavalue']['value']
                                        if isinstance(value, dict) and 'id' in value:
                                            claims.append(f"{prop}: {value['id']}")
                                        elif isinstance(value, str):
                                            claims.append(f"{prop}: {value}")
                        
                        if claims:
                            text_data['claims'] = claims
                    
                    # Combine all text fields into a single document
                    if text_data:
                        full_text = ""
                        
                        if 'label' in text_data:
                            full_text += f"Title: {text_data['label']}\n"
                        
                        if 'description' in text_data:
                            full_text += f"Description: {text_data['description']}\n"
                        
                        if 'aliases' in text_data:
                            full_text += f"Also known as: {', '.join(text_data['aliases'])}\n"
                        
                        if 'claims' in text_data:
                            full_text += "Facts:\n"
                            for claim in text_data['claims'][:20]:  # Limit to 20 claims per entity
                                full_text += f"- {claim}\n"
                        
                        # Write processed text to output file
                        output = {
                            'id': entity['id'],
                            'text': full_text.strip()
                        }
                        f_out.write(json.dumps(output) + '\n')
                        
                        count += 1
                        if count >= max_items:
                            break
                        
                        if count % 10000 == 0:
                            logging.info(f"Processed {count} entities")
                
                except json.JSONDecodeError:
                    logging.warning(f"Failed to parse JSON line")
                    continue
                except Exception as e:
                    logging.error(f"Error processing entity: {e}")
                    continue
    
    logging.info(f"Completed processing. Saved {count} entities to {output_path}")

def create_training_samples(input_path, output_path, min_length=50):
    """
    Create training samples from processed Wikidata.
    Filter out entries that are too short and prepare data in the right format.
    """
    logging.info(f"Creating training samples from {input_path}")
    
    count = 0
    with open(input_path, 'r', encoding='utf-8') as f_in:
        with open(output_path, 'w', encoding='utf-8') as f_out:
            for line in tqdm(f_in, desc="Creating training samples"):
                try:
                    item = json.loads(line)
                    
                    if 'text' in item and len(item['text']) >= min_length:
                        # Additional processing can be done here
                        f_out.write(json.dumps({'text': item['text']}) + '\n')
                        count += 1
                
                except Exception as e:
                    logging.error(f"Error processing line: {e}")
                    continue
    
    logging.info(f"Created {count} training samples in {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Process Wikidata dumps for TextCellAI training')
    parser.add_argument('--download', action='store_true', help='Download Wikidata dump')
    parser.add_argument('--dump-url', type=str, help='URL to Wikidata dump (if not using default)')
    parser.add_argument('--dump-path', type=str, help='Path to existing Wikidata dump')
    parser.add_argument('--output-dir', type=str, default='./wikidata_processed', help='Output directory')
    parser.add_argument('--max-items', type=int, default=100000, help='Maximum items to process')
    parser.add_argument('--language', type=str, default='en', help='Language code')
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Download dump if requested
    if args.download:
        dump_path = download_wikidata_dump(
            output_dir=os.path.join(args.output_dir, 'dumps'),
            dump_url=args.dump_url
        )
    else:
        dump_path = args.dump_path
        if not dump_path or not os.path.exists(dump_path):
            logging.error("Please provide a valid dump path or use --download")
            return
    
    # Process dump
    processed_path = os.path.join(args.output_dir, 'wikidata_processed.jsonl')
    process_wikidata_dump(
        dump_path=dump_path,
        output_path=processed_path,
        max_items=args.max_items,
        language=args.language
    )
    
    # Create training samples
    training_path = os.path.join(args.output_dir, 'wikidata_training.jsonl')
    create_training_samples(
        input_path=processed_path,
        output_path=training_path
    )
    
    logging.info(f"Processing complete. Training data saved to {training_path}")
    logging.info(f"Use this file with TextCellAI: python textcellai.py train --data {training_path}")

if __name__ == "__main__":
    main()