import torch
import ray
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple, List, Optional
import logging
import atexit
import os
import time
import sys

# Configure logging for immediate feedback
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

class NetworkState(Enum):
    EXPLORING = 1    # Initial exploration phase
    CONNECTING = 2   # Forming connections between resources
    OPTIMIZING = 3   # Optimizing network structure
    STABLE = 4       # Final stable network configuration

@dataclass
class NetworkConfig:
    """
    Configuration parameters for the fungal network simulation.
    
    Optimized parameters based on analysis for better network formation:
    - Increased space_dims to allow better exploration
    - Higher growth_rate to encourage exploration
    - Balanced decay_rate and connection parameters
    - Increased resource spacing and influence
    """
    num_nodes: int                      # Number of nodes in the network
    space_dims: Tuple[int, int, int]    # Dimensions of the space (x, y, z)
    growth_rate: float = 0.18           # Increased from 0.1 for better exploration
    decay_rate: float = 0.03            # Reduced from 0.05 for more balanced decay
    connection_threshold: float = 1.5   # Balanced threshold (was 1.0)
    pattern_threshold: float = 0.4      # Lowered from 0.5 to detect patterns more easily
    resource_influence: float = 2.5     # Increased from 2.0 for stronger influence on network formation
    device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # Resource arrangement parameters
    resource_arrangement: str = 'random'  # 'random', 'circle', 'cross'
    num_resources: int = 9               # Number of resources (wood blocks in the paper)
    resource_spacing: float = 7.5        # Increased from 5.0 for better spacing between resources

@ray.remote
class NetworkRegion:
    def __init__(self, config: NetworkConfig, region_id: int):
        self.config = config
        self.region_id = region_id
        self.device = torch.device(config.device)
        
        # Network state - COMPLETELY REDESIGNED: Initialization with strategic node placement
        initial_nodes = config.num_nodes
        
        # Create positions tensor
        positions = torch.zeros((initial_nodes, 3), device=self.device)
        
        # Set up resource positions first to guide initialization
        self.resource_positions = self._setup_resources()
        
        # Distribute nodes strategically
        # 1. Central cluster (30% of nodes)
        central_count = int(initial_nodes * 0.3)
        for i in range(central_count):
            # Place in a small central cluster
            angle = torch.rand(1, device=self.device).item() * 2 * np.pi
            distance = torch.rand(1, device=self.device).item() * 2.0  # Small central cluster
            positions[i, 0] = distance * np.cos(angle)  # x coordinate
            positions[i, 1] = distance * np.sin(angle)  # y coordinate
        
        # 2. Resource-affiliated nodes (50% of nodes)
        resource_count = int(initial_nodes * 0.5)
        if len(self.resource_positions) > 0:
            nodes_per_resource = resource_count // len(self.resource_positions)
            idx = central_count
            
            for r_idx, r_pos in enumerate(self.resource_positions):
                for j in range(nodes_per_resource):
                    if idx < initial_nodes:
                        # Place near resource with some randomness
                        angle = torch.rand(1, device=self.device).item() * 2 * np.pi
                        distance = torch.rand(1, device=self.device).item() * 2.5  # Distance from resource
                        
                        positions[idx, 0] = r_pos[0] + distance * np.cos(angle)
                        positions[idx, 1] = r_pos[1] + distance * np.sin(angle)
                        idx += 1
        
        # 3. Pathway nodes (20% of nodes)
        # Create paths between central cluster and resources, and between resources
        remaining = initial_nodes - idx
        if remaining > 0 and len(self.resource_positions) > 0:
            # First, paths from center to resources
            center = torch.zeros(2, device=self.device)
            for r_idx, r_pos in enumerate(self.resource_positions):
                if idx >= initial_nodes:
                    break
                    
                # Calculate number of nodes for this path
                dist_to_center = torch.norm(r_pos[:2])
                path_nodes = min(remaining // len(self.resource_positions), int(dist_to_center / 2))
                
                for j in range(path_nodes):
                    if idx < initial_nodes:
                        # Position along path with jitter
                        t = (j + 1) / (path_nodes + 1)  # Position along path (0 to 1)
                        path_pos = t * r_pos[:2]  # Interpolate from center (0,0) to resource
                        
                        # Add some randomness to make natural paths
                        jitter = (torch.rand(2, device=self.device) - 0.5) * dist_to_center * 0.3
                        positions[idx, 0] = path_pos[0] + jitter[0]
                        positions[idx, 1] = path_pos[1] + jitter[1]
                        idx += 1
            
            # If still have nodes, create paths between some resources
            while idx < initial_nodes and len(self.resource_positions) >= 2:
                # Pick two random distinct resources
                r1_idx = torch.randint(0, len(self.resource_positions), (1,), device=self.device).item()
                r2_idx = (r1_idx + 1 + torch.randint(0, len(self.resource_positions) - 1, (1,), device=self.device).item()) % len(self.resource_positions)
                
                r1_pos = self.resource_positions[r1_idx]
                r2_pos = self.resource_positions[r2_idx]
                
                # Calculate direct distance
                dist = torch.norm(r1_pos - r2_pos)
                path_nodes = min(remaining, int(dist / 2))
                
                for j in range(path_nodes):
                    if idx < initial_nodes:
                        # Position along path with jitter
                        t = (j + 1) / (path_nodes + 1)  # Position along path (0 to 1)
                        path_pos = r1_pos + t * (r2_pos - r1_pos)  # Interpolate between resources
                        
                        # Add some randomness for natural paths
                        jitter = torch.randn(3, device=self.device) * dist * 0.05
                        positions[idx] = path_pos + jitter
                        idx += 1
                
                remaining = initial_nodes - idx
                if remaining <= 0:
                    break
        
        # Fill any remaining positions randomly throughout the space
        if idx < initial_nodes:
            for i in range(idx, initial_nodes):
                # Random position within the space bounds
                positions[i, 0] = (torch.rand(1, device=self.device) * 2 - 1) * config.space_dims[0] * 0.4
                positions[i, 1] = (torch.rand(1, device=self.device) * 2 - 1) * config.space_dims[1] * 0.4
        
        self.positions = positions
        self.resources = torch.ones(config.num_nodes, device=self.device)
        self.connections = torch.zeros((config.num_nodes, config.num_nodes), device=self.device)
        self.state = NetworkState.EXPLORING
        
        # Resource states - initialized after resource positions
        self.resource_decay = torch.zeros(len(self.resource_positions), device=self.device)
        self.resource_connections = torch.zeros(len(self.resource_positions), device=self.device)
        
        # Pattern templates
        self.patterns = {
            'circle': self._create_circle(),
            'cross': self._create_cross(),
            'triangle': self._create_triangle(),
            'square': self._create_square(),
            'hexagon': self._create_hexagon(),
            'star': self._create_star(),
            'spiral': self._create_spiral(),
            'grid': self._create_grid(),
            'web': self._create_web(),
            'tree': self._create_tree()
        }
        
        # Feature tracking
        self.pattern_history = []
        self.efficiency_history = []
        self.current_pattern = None
        self.steps = 0
        
    def _setup_resources(self) -> List[torch.Tensor]:
        """
        Set up resource positions based on arrangement type.
        
        IMPROVED: 
        - Increased circle radius to prevent resources from being too close
        - Enhanced spacing in cross arrangement
        - Improved random distribution to use more of the available space
        """
        resources = []
        spacing = self.config.resource_spacing
        num_resources = self.config.num_resources
        
        if self.config.resource_arrangement == 'circle':
            # IMPROVED: Create resources in a circle with better spacing
            # Changed from spacing/(2*sin(pi/num_resources)) to spacing*1.5 for better exploration
            radius = spacing * 1.5
            for i in range(num_resources):
                angle = 2 * np.pi * i / num_resources
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                resources.append(torch.tensor([x, y, 0.0], device=self.device))
                
        elif self.config.resource_arrangement == 'cross':
            # IMPROVED: Create resources in a cross with better spacing
            # Center block
            resources.append(torch.tensor([0.0, 0.0, 0.0], device=self.device))
            
            # Middle blocks (adjacent to center) with improved spacing
            for dx, dy in [(spacing, 0), (0, spacing), (-spacing, 0), (0, -spacing)]:
                resources.append(torch.tensor([dx, dy, 0.0], device=self.device))
                
            # Outer blocks with improved spacing
            for dx, dy in [(2*spacing, 0), (0, 2*spacing), (-2*spacing, 0), (0, -2*spacing)]:
                resources.append(torch.tensor([dx, dy, 0.0], device=self.device))
                
        else:  # random arrangement with better distribution
            # IMPROVED: Use a more spread out random distribution
            max_dim = max(self.config.space_dims[0], self.config.space_dims[1]) * 0.8
            for _ in range(num_resources):
                x = (torch.rand(1, device=self.device) * 2 - 1) * max_dim
                y = (torch.rand(1, device=self.device) * 2 - 1) * max_dim
                resources.append(torch.tensor([x.item(), y.item(), 0.0], device=self.device))
                
        return resources
        
    def _create_circle(self) -> torch.Tensor:
        n = self.config.num_nodes
        angles = torch.linspace(0, 2*torch.pi, n, device=self.device)
        x = torch.cos(angles)
        y = torch.sin(angles)
        z = torch.zeros_like(x)
        return self._normalize_pattern(torch.stack([x, y, z], dim=1))
        
    def _create_cross(self) -> torch.Tensor:
        n = self.config.num_nodes
        n_per_arm = n // 4
        arm = torch.linspace(-1, 1, n_per_arm, device=self.device)
        
        # Create the cross with 4 arms, ensuring total points is n
        x_parts = [arm, torch.zeros(n_per_arm, device=self.device), -arm, torch.zeros(n_per_arm, device=self.device)]
        y_parts = [torch.zeros(n_per_arm, device=self.device), arm, torch.zeros(n_per_arm, device=self.device), -arm]
        
        # Add any remaining points to make total = n
        remaining = n - 4 * n_per_arm
        if remaining > 0:
            x_parts.append(torch.zeros(remaining, device=self.device))
            y_parts.append(torch.zeros(remaining, device=self.device))
        
        x = torch.cat(x_parts)
        y = torch.cat(y_parts)
        z = torch.zeros_like(x)
        
        return self._normalize_pattern(torch.stack([x, y, z], dim=1))
        
    def _create_triangle(self) -> torch.Tensor:
        n = self.config.num_nodes
        n_per_side = n // 3
        
        angles = torch.tensor([0, 2*np.pi/3, 4*np.pi/3], device=self.device)
        vertices_x = torch.cos(angles)
        vertices_y = torch.sin(angles)
        
        # Create points along each side
        sides_x = []
        sides_y = []
        
        for i in range(3):
            start_x, end_x = vertices_x[i], vertices_x[(i+1)%3]
            start_y, end_y = vertices_y[i], vertices_y[(i+1)%3]
            
            side_x = torch.linspace(start_x, end_x, n_per_side, device=self.device)
            side_y = torch.linspace(start_y, end_y, n_per_side, device=self.device)
            
            sides_x.append(side_x)
            sides_y.append(side_y)
        
        # Combine all sides
        x = torch.cat(sides_x)
        y = torch.cat(sides_y)
        
        # Add any remaining points to reach n
        remaining = n - x.size(0)
        if remaining > 0:
            center_x = torch.zeros(remaining, device=self.device)
            center_y = torch.zeros(remaining, device=self.device)
            x = torch.cat([x, center_x])
            y = torch.cat([y, center_y])
        
        z = torch.zeros_like(x)
        return self._normalize_pattern(torch.stack([x, y, z], dim=1))
        
    def _create_square(self) -> torch.Tensor:
        n = self.config.num_nodes
        n_per_side = n // 4
        
        # Create four sides of a square
        side = torch.linspace(-1, 1, n_per_side, device=self.device)
        
        x_parts = [side, torch.ones(n_per_side, device=self.device), -side.flip(0), -torch.ones(n_per_side, device=self.device)]
        y_parts = [torch.ones(n_per_side, device=self.device), -side, -torch.ones(n_per_side, device=self.device), side.flip(0)]
        
        # Add remaining points to reach n
        remaining = n - 4 * n_per_side
        if remaining > 0:
            x_parts.append(torch.zeros(remaining, device=self.device))
            y_parts.append(torch.zeros(remaining, device=self.device))
            
        x = torch.cat(x_parts)
        y = torch.cat(y_parts)
        z = torch.zeros_like(x)
        
        return self._normalize_pattern(torch.stack([x, y, z], dim=1))
        
    def _create_hexagon(self) -> torch.Tensor:
        n = self.config.num_nodes
        n_per_side = n // 6
        
        angles = torch.linspace(0, 2*torch.pi, 7, device=self.device)[:-1]  # 6 points
        vertices_x = torch.cos(angles)
        vertices_y = torch.sin(angles)
        
        # Create points along each side
        sides_x = []
        sides_y = []
        
        for i in range(6):
            start_x, end_x = vertices_x[i], vertices_x[(i+1)%6]
            start_y, end_y = vertices_y[i], vertices_y[(i+1)%6]
            
            side_x = torch.linspace(start_x, end_x, n_per_side, device=self.device)
            side_y = torch.linspace(start_y, end_y, n_per_side, device=self.device)
            
            sides_x.append(side_x)
            sides_y.append(side_y)
        
        # Combine all sides
        x = torch.cat(sides_x)
        y = torch.cat(sides_y)
        
        # Add remaining points to reach n
        remaining = n - x.size(0)
        if remaining > 0:
            center_x = torch.zeros(remaining, device=self.device)
            center_y = torch.zeros(remaining, device=self.device)
            x = torch.cat([x, center_x])
            y = torch.cat([y, center_y])
            
        z = torch.zeros_like(x)
        return self._normalize_pattern(torch.stack([x, y, z], dim=1))
        
    def _create_star(self) -> torch.Tensor:
        n = self.config.num_nodes
        points = 5
        total_points = points * 2
        n_per_point = n // total_points
        
        # Create inner and outer radii at alternating angles
        angles = torch.linspace(0, 2*torch.pi, total_points+1, device=self.device)[:-1]
        radii = torch.ones(total_points, device=self.device)
        # Set every other radius to 0.5 for the star effect
        radii[1::2] = 0.5
        
        # Create points between each vertex
        all_x = []
        all_y = []
        
        for i in range(total_points):
            start_angle = angles[i]
            end_angle = angles[(i+1) % total_points]
            start_r = radii[i]
            end_r = radii[(i+1) % total_points]
            
            # Linear interpolation between points
            t = torch.linspace(0, 1, n_per_point, device=self.device)
            interp_angle = start_angle * (1-t) + end_angle * t
            interp_r = start_r * (1-t) + end_r * t
            
            x = interp_r * torch.cos(interp_angle)
            y = interp_r * torch.sin(interp_angle)
            
            all_x.append(x)
            all_y.append(y)
        
        x = torch.cat(all_x)
        y = torch.cat(all_y)
        
        # Add remaining points to reach n
        remaining = n - x.size(0)
        if remaining > 0:
            center_x = torch.zeros(remaining, device=self.device)
            center_y = torch.zeros(remaining, device=self.device)
            x = torch.cat([x, center_x])
            y = torch.cat([y, center_y])
            
        z = torch.zeros_like(x)
        return self._normalize_pattern(torch.stack([x, y, z], dim=1))
        
    def _create_spiral(self) -> torch.Tensor:
        n = self.config.num_nodes
        t = torch.linspace(0, 6*torch.pi, n, device=self.device)
        r = t/6
        x = r * torch.cos(t)
        y = r * torch.sin(t)
        z = torch.zeros_like(x)
        return self._normalize_pattern(torch.stack([x, y, z], dim=1))
        
    def _create_grid(self) -> torch.Tensor:
        n = self.config.num_nodes
        side = int(np.sqrt(n))
        
        # Create a grid of side x side points
        x_coords = torch.linspace(-1, 1, side, device=self.device)
        y_coords = torch.linspace(-1, 1, side, device=self.device)
        
        # Create the grid
        y_grid, x_grid = torch.meshgrid(y_coords, x_coords, indexing='ij')
        x = x_grid.reshape(-1)
        y = y_grid.reshape(-1)
        
        # Add remaining points to reach n
        grid_size = side * side
        remaining = n - grid_size
        if remaining > 0:
            extra_x = torch.zeros(remaining, device=self.device)
            extra_y = torch.zeros(remaining, device=self.device)
            x = torch.cat([x, extra_x])
            y = torch.cat([y, extra_y])
        elif remaining < 0:
            # If we have too many points, truncate
            x = x[:n]
            y = y[:n]
            
        z = torch.zeros_like(x)
        return self._normalize_pattern(torch.stack([x, y, z], dim=1))
        
    def _create_web(self) -> torch.Tensor:
        n = self.config.num_nodes
        rings = 5
        points_per_ring = n // rings
        
        all_x = []
        all_y = []
        
        for ring in range(rings):
            radius = 0.2 + 0.8 * (ring / (rings - 1))
            angles = torch.linspace(0, 2*torch.pi, points_per_ring, device=self.device)
            
            x = radius * torch.cos(angles)
            y = radius * torch.sin(angles)
            
            all_x.append(x)
            all_y.append(y)
        
        x = torch.cat(all_x)
        y = torch.cat(all_y)
        
        # Add remaining points to reach n
        remaining = n - x.size(0)
        if remaining > 0:
            center_x = torch.zeros(remaining, device=self.device)
            center_y = torch.zeros(remaining, device=self.device)
            x = torch.cat([x, center_x])
            y = torch.cat([y, center_y])
        elif remaining < 0:
            # If we have too many points, truncate
            x = x[:n]
            y = y[:n]
            
        z = torch.zeros_like(x)
        return self._normalize_pattern(torch.stack([x, y, z], dim=1))
        
    def _create_tree(self) -> torch.Tensor:
        n = self.config.num_nodes
        levels = 4
        branches = 2
        
        all_x = []
        all_y = []
        all_z = []
        
        for level in range(levels):
            spread = 2.0 ** (level-levels+1)
            height = 1 - level/levels
            branch_points = branches**level
            points_per_branch = max(1, n // sum([branches**l for l in range(levels)]))
            
            for b in range(branch_points):
                x_pos = (b - branch_points/2 + 0.5) * spread
                x = torch.full((points_per_branch,), x_pos, device=self.device)
                y = torch.full((points_per_branch,), height, device=self.device)
                z = torch.zeros(points_per_branch, device=self.device)
                
                all_x.append(x)
                all_y.append(y)
                all_z.append(z)
        
        x = torch.cat(all_x)
        y = torch.cat(all_y)
        z = torch.cat(all_z)
        
        # Add remaining points to reach n
        remaining = n - x.size(0)
        if remaining > 0:
            extra_x = torch.zeros(remaining, device=self.device)
            extra_y = torch.zeros(remaining, device=self.device)
            extra_z = torch.zeros(remaining, device=self.device)
            x = torch.cat([x, extra_x])
            y = torch.cat([y, extra_y])
            z = torch.cat([z, extra_z])
        elif remaining < 0:
            # If we have too many points, truncate
            x = x[:n]
            y = y[:n]
            z = z[:n]
            
        return self._normalize_pattern(torch.stack([x, y, z], dim=1))
        
    def _normalize_pattern(self, pattern: torch.Tensor) -> torch.Tensor:
        """Normalize pattern and ensure it matches the required shape"""
        n, dims = pattern.shape
        
        # Ensure pattern has exactly self.config.num_nodes points
        if n < self.config.num_nodes:
            # Pad if needed
            padding = torch.zeros((self.config.num_nodes - n, dims), device=pattern.device)
            pattern = torch.cat([pattern, padding], dim=0)
        elif n > self.config.num_nodes:
            # Truncate if needed
            pattern = pattern[:self.config.num_nodes]
        
        # Normalize the pattern
        max_val = torch.max(torch.abs(pattern))
        if max_val > 0:  # Avoid division by zero
            pattern = pattern / max_val
            
        return pattern
        
    def update(self, dt: float) -> None:
        """Update network region"""
        self.steps += 1
        
        # Early stages - Initial exploration (days 1-13 in the paper)
        if self.steps < 50:
            self._explore_resources(dt)
            self.state = NetworkState.EXPLORING
            
        # Mid stages - Network formation (days 14-34 in the paper)
        elif self.steps < 150:
            self._connect_resources(dt)
            self.state = NetworkState.CONNECTING
            
        # Later stages - Network optimization (days 35-116 in the paper)
        else:
            self._optimize_network(dt)
            # Update network state based on steps
            if self.steps < 250:
                self.state = NetworkState.OPTIMIZING
            else:
                self.state = NetworkState.STABLE
                
        self._update_resources(dt)
        self._update_connections()
        self._track_features()
        
    def _explore_resources(self, dt: float) -> None:
        """
        Initial exploration phase - grow towards resources
        
        COMPLETELY REDESIGNED:
        - Direct resource targeting with strong attraction
        - Resource-centric exploration pattern
        - Explicit path creation toward resources
        - Distance-based movement speed (faster when farther)
        """
        # First, distribute some nodes directly to resources during early steps
        # This ensures we have nodes near each resource to start forming connections
        if self.steps < 30:  # During early exploration
            resources_per_step = max(1, len(self.resource_positions) // 15)
            
            for _ in range(resources_per_step):
                # Select a random resource to target
                r_idx = torch.randint(0, len(self.resource_positions), (1,), device=self.device).item()
                r_pos = self.resource_positions[r_idx]
                
                # Find nodes that are not already near resources
                central_nodes = []
                for i, pos in enumerate(self.positions):
                    min_dist = min([torch.norm(pos - res) for res in self.resource_positions])
                    if min_dist > 4.0:  # Not near any resource yet
                        central_nodes.append(i)
                
                if central_nodes:
                    # Select random nodes from central area to send toward this resource
                    num_to_move = min(5, len(central_nodes))
                    nodes_to_move = np.random.choice(central_nodes, num_to_move, replace=False)
                    
                    for i in nodes_to_move:
                        # Calculate direction from node to resource
                        direction = r_pos - self.positions[i]
                        distance = torch.norm(direction) + 1e-6
                        normalized_dir = direction / distance
                        
                        # Move the node a significant distance toward the resource
                        # Higher speed for farther distances to ensure it gets there
                        speed = min(5.0, 0.5 + (distance / 10.0))
                        self.positions[i] += normalized_dir * speed * dt * self.config.growth_rate * 5.0
        
        # Direct attraction to resources - strong pull toward nearest resource
        for i, pos in enumerate(self.positions):
            # Find distances to all resources
            distances = [torch.norm(pos - r_pos) for r_pos in self.resource_positions]
            closest_idx = np.argmin(distances)
            closest_dist = distances[closest_idx]
            
            # Different movement strategies based on distance to closest resource
            if closest_dist < 2.0:
                # Already near a resource - make small movements to optimize position
                move_prob = 0.3
                if torch.rand(1, device=self.device).item() < move_prob:
                    direction = self.resource_positions[closest_idx] - pos
                    # Gentle movement for fine positioning
                    movement = dt * self.config.growth_rate * direction * 0.5
                    self.positions[i] += movement
                    
            elif closest_dist < 6.0:
                # Medium distance - actively move toward resource
                move_prob = 0.8
                if torch.rand(1, device=self.device).item() < move_prob:
                    direction = self.resource_positions[closest_idx] - pos
                    distance = torch.norm(direction) + 1e-6
                    normalized_dir = direction / distance
                    
                    # Stronger movement for medium distance
                    speed = 1.0 + (distance / 5.0)
                    self.positions[i] += normalized_dir * speed * dt * self.config.growth_rate * 3.0
                    
            else:
                # Far from any resource - very strong attraction
                move_prob = 0.95
                if torch.rand(1, device=self.device).item() < move_prob:
                    direction = self.resource_positions[closest_idx] - pos
                    distance = torch.norm(direction) + 1e-6
                    normalized_dir = direction / distance
                    
                    # Aggressive movement for long distance
                    speed = 2.0 + (distance / 5.0)
                    self.positions[i] += normalized_dir * speed * dt * self.config.growth_rate * 4.0
        
        # Create "pathfinder" nodes that form trails between central cluster and resources
        if self.steps < 60:  # During exploration phase, create paths
            # Every few steps, send pathfinder nodes
            if self.steps % 5 == 0:
                for r_idx, r_pos in enumerate(self.resource_positions):
                    # Find closest nodes to the resource
                    nodes_near_resource = []
                    for i, pos in enumerate(self.positions):
                        dist = torch.norm(pos - r_pos)
                        if dist < 4.0:  # Already near resource
                            nodes_near_resource.append((i, dist.item()))
                    
                    # If no nodes are near this resource, create a path
                    if len(nodes_near_resource) < 3:
                        # Find a node near the center to start a path from
                        central_nodes = []
                        center = torch.zeros(3, device=self.device)
                        
                        for i, pos in enumerate(self.positions):
                            dist_to_center = torch.norm(pos)
                            if dist_to_center < 3.0:  # Near center
                                central_nodes.append(i)
                        
                        if central_nodes:
                            # Select a random central node
                            start_idx = np.random.choice(central_nodes)
                            start_pos = self.positions[start_idx]
                            
                            # Create a path by moving several nodes along it
                            path_length = torch.norm(r_pos - start_pos)
                            num_path_nodes = min(10, int(path_length / 2.0))
                            
                            for step in range(1, num_path_nodes + 1):
                                # Position along the path
                                t = step / (num_path_nodes + 1)
                                path_pos = start_pos + t * (r_pos - start_pos)
                                
                                # Find a free node to move to this position
                                free_nodes = []
                                for i, pos in enumerate(self.positions):
                                    if i != start_idx and i not in central_nodes:
                                        # Check if not already on a path
                                        min_dist = min([torch.norm(pos - res) for res in self.resource_positions])
                                        if min_dist > 5.0:  # Not near any resource yet
                                            free_nodes.append(i)
                                
                                if free_nodes:
                                    # Move a free node to this path position
                                    node_idx = np.random.choice(free_nodes)
                                    # Add some randomness to avoid perfectly straight lines
                                    jitter = torch.randn(3, device=self.device) * 0.5
                                    self.positions[node_idx] = path_pos + jitter
        
        # Apply node repulsion to avoid overcrowding
        repulsion_radius = 0.5  # Radius within which nodes repel each other
        repulsion_strength = 0.1 * dt  # Strength of repulsion
        
        for i in range(len(self.positions)):
            pos_i = self.positions[i]
            repulsion = torch.zeros(3, device=self.device)
            
            # Only apply repulsion to a random subset of nearby nodes for efficiency
            if torch.rand(1, device=self.device).item() < 0.3:  # 30% chance
                for j in range(len(self.positions)):
                    if i != j:
                        pos_j = self.positions[j]
                        diff = pos_i - pos_j
                        dist = torch.norm(diff)
                        
                        if dist < repulsion_radius and dist > 1e-6:
                            # Repulsion force inversely proportional to distance
                            force = repulsion_strength * (repulsion_radius - dist) / dist
                            repulsion += force * diff
                
                # Apply accumulated repulsion
                self.positions[i] += repulsion
        
    def _connect_resources(self, dt: float) -> None:
        """
        Connection phase - form links between resources
        
        COMPLETELY REDESIGNED:
        - Direct resource-to-resource connection building
        - Active identification of resource paths
        - Prioritized connection of nodes near resources
        - Dynamic scoring of potential connections
        """
        # Reduced reliance on exploration - focus on directed connection
        self._explore_resources(dt * 0.2)
        
        # PHASE 1: Create connections between nodes and resources
        for r_idx, r_pos in enumerate(self.resource_positions):
            # Find all nodes near this resource
            nodes_near_resource = []
            for i, pos in enumerate(self.positions):
                dist_to_resource = torch.norm(pos - r_pos)
                if dist_to_resource < 4.0:  # Within resource radius
                    nodes_near_resource.append((i, dist_to_resource.item()))
            
            # Sort by distance to resource
            nodes_near_resource.sort(key=lambda x: x[1])
            
            # Mark these nodes as having a connection to this resource
            if nodes_near_resource:
                # Connect all nearby nodes to each other (create resource sub-network)
                for idx1, dist1 in nodes_near_resource:
                    # Increase resource connection counter immediately
                    self.resource_connections[r_idx] += 0.01 * dt
                    
                    # Connect to other nodes near the same resource
                    for idx2, dist2 in nodes_near_resource:
                        if idx1 != idx2:
                            # Calculate distance between nodes
                            node_dist = torch.norm(self.positions[idx1] - self.positions[idx2])
                            
                            # If they're close enough, connect them
                            max_dist = 2.0 + (0.2 * dist1 + 0.2 * dist2)  # Adaptive threshold
                            if node_dist < max_dist:
                                # Set strong connection strength
                                strength = 0.5 + 0.5 * (1.0 - node_dist / max_dist)
                                self.connections[idx1, idx2] = max(self.connections[idx1, idx2], strength)
                                self.connections[idx2, idx1] = max(self.connections[idx2, idx1], strength)
        
        # PHASE 2: Build resource-to-resource connections through pathways
        # Identify all resource pairs
        for r1_idx, r1_pos in enumerate(self.resource_positions):
            for r2_idx, r2_pos in enumerate(self.resource_positions):
                if r1_idx >= r2_idx:  # Avoid redundant pairs
                    continue
                
                # Find all nodes near each resource
                nodes_near_r1 = []
                nodes_near_r2 = []
                
                for i, pos in enumerate(self.positions):
                    dist_to_r1 = torch.norm(pos - r1_pos)
                    dist_to_r2 = torch.norm(pos - r2_pos)
                    
                    if dist_to_r1 < 4.0:
                        nodes_near_r1.append(i)
                    if dist_to_r2 < 4.0:
                        nodes_near_r2.append(i)
                
                # Skip if either resource has no nearby nodes
                if not nodes_near_r1 or not nodes_near_r2:
                    continue
                
                # Check if there's a "pathway" between these resources
                r1_to_r2 = torch.norm(r1_pos - r2_pos)
                direct_path_threshold = r1_to_r2 * 1.4  # Allow 40% extra distance for path
                
                # Look for series of nodes creating a pathway
                for idx1 in nodes_near_r1:
                    for idx2 in nodes_near_r2:
                        if idx1 == idx2:
                            continue
                        
                        # Calculate length of path between nodes
                        node_distance = torch.norm(self.positions[idx1] - self.positions[idx2])
                        
                        # If direct path is possible, create a strong connection
                        if node_distance < direct_path_threshold:
                            # Create direct connection with high strength
                            strength = 1.0 - (node_distance / direct_path_threshold) * 0.5
                            self.connections[idx1, idx2] = max(self.connections[idx1, idx2], strength)
                            self.connections[idx2, idx1] = max(self.connections[idx2, idx1], strength)
                            
                            # Increment resource connections for both resources
                            self.resource_connections[r1_idx] += 0.05 * dt
                            self.resource_connections[r2_idx] += 0.05 * dt
                            
                            # Create connections with intermediate nodes
                            for k, pos_k in enumerate(self.positions):
                                if k == idx1 or k == idx2:
                                    continue
                                
                                # Check if this node is on the path between the two resource nodes
                                dist_to_idx1 = torch.norm(pos_k - self.positions[idx1])
                                dist_to_idx2 = torch.norm(pos_k - self.positions[idx2])
                                
                                # If node is between the two endpoints and near the path
                                if dist_to_idx1 + dist_to_idx2 < node_distance * 1.3:
                                    # Connect to both endpoints
                                    strength1 = 0.8 - (dist_to_idx1 / node_distance) * 0.5
                                    self.connections[idx1, k] = max(self.connections[idx1, k], strength1)
                                    self.connections[k, idx1] = max(self.connections[k, idx1], strength1)
                                    
                                    strength2 = 0.8 - (dist_to_idx2 / node_distance) * 0.5
                                    self.connections[idx2, k] = max(self.connections[idx2, k], strength2)
                                    self.connections[k, idx2] = max(self.connections[k, idx2], strength2)
        
        # PHASE 3: Create a network backbone connecting central nodes to resource nodes
        center = torch.zeros(3, device=self.device)
        
        # Find central nodes
        central_nodes = []
        for i, pos in enumerate(self.positions):
            dist_to_center = torch.norm(pos)
            if dist_to_center < 3.0:  # Near center
                central_nodes.append(i)
        
        # Find resource nodes
        resource_nodes = []
        for r_idx, r_pos in enumerate(self.resource_positions):
            for i, pos in enumerate(self.positions):
                if torch.norm(pos - r_pos) < 4.0:  # Near resource
                    resource_nodes.append(i)
        
        # Connect central to resource nodes with intermediates
        if central_nodes and resource_nodes:
            for central_idx in central_nodes[:10]:  # Limit to avoid too many connections
                for resource_idx in resource_nodes[:20]:  # Limit to avoid too many connections
                    if central_idx == resource_idx:
                        continue
                    
                    # Get positions
                    central_pos = self.positions[central_idx]
                    resource_pos = self.positions[resource_idx]
                    
                    # Find nodes that might be along the path
                    for k, pos_k in enumerate(self.positions):
                        if k == central_idx or k == resource_idx:
                            continue
                        
                        # Check if this node is near the path
                        direct_dist = torch.norm(resource_pos - central_pos)
                        dist_to_central = torch.norm(pos_k - central_pos)
                        dist_to_resource = torch.norm(pos_k - resource_pos)
                        
                        # If node is close to the direct path
                        if dist_to_central + dist_to_resource < direct_dist * 1.3:
                            # Connect to both endpoints
                            self.connections[central_idx, k] = max(self.connections[central_idx, k], 0.3)
                            self.connections[k, central_idx] = max(self.connections[k, central_idx], 0.3)
                            
                            self.connections[resource_idx, k] = max(self.connections[resource_idx, k], 0.3)
                            self.connections[k, resource_idx] = max(self.connections[k, resource_idx], 0.3)
                            
                            # Also connect to resource
                            for r_idx, r_pos in enumerate(self.resource_positions):
                                if torch.norm(resource_pos - r_pos) < 4.0:  # If near resource
                                    self.resource_connections[r_idx] += 0.01 * dt
        
    def _optimize_network(self, dt: float) -> None:
        """
        Optimization phase - refine network structure
        
        FIXED:
        - Bug fix: Added .item() to convert tensor to scalar to prevent dimension mismatch
        
        IMPROVED:
        - Reduced pruning probability for less aggressive pruning
        - More gradual connection reset during pruning
        """
        # Compute centrality of nodes (how connected they are)
        node_centrality = torch.sum(self.connections, dim=1)
        
        # Prune low centrality nodes with reduced probability
        prune_threshold = torch.median(node_centrality)
        for i in range(len(self.positions)):
            if node_centrality[i] < prune_threshold:
                # IMPROVED: Reduced pruning probability for less aggressive pruning
                prune_prob = 0.05 * dt  # Reduced from 0.1
                if torch.rand(1, device=self.device).item() < prune_prob:
                    # "Prune" by moving node to more central position
                    # Find a high centrality node
                    high_centrality = torch.nonzero(node_centrality > prune_threshold).squeeze()
                    if high_centrality.dim() > 0:  # Ensure there's at least one high centrality node
                        # FIXED BUG: Add .item() to convert tensor to scalar
                        idx = high_centrality[torch.randint(0, high_centrality.size(0), (1,), device=self.device)].item()
                        # Move towards it
                        self.positions[i] += 0.1 * (self.positions[idx] - self.positions[i])
                        # IMPROVED: Reset connections more gradually
                        self.connections[i, :] *= 0.5  # Instead of complete reset
                        self.connections[:, i] *= 0.5  # Instead of complete reset
        
        # Strengthen important connections
        for i in range(len(self.positions)):
            for j in range(i+1, len(self.positions)):
                if self.connections[i, j] > 0:
                    # Find resource affiliations
                    i_distances = [torch.norm(self.positions[i] - r_pos) for r_pos in self.resource_positions]
                    j_distances = [torch.norm(self.positions[j] - r_pos) for r_pos in self.resource_positions]
                    i_resource = np.argmin(i_distances)
                    j_resource = np.argmin(j_distances)
                    
                    # Strengthen based on resource decay - simulate more connections where more decay occurs
                    if i_resource != j_resource:
                        # Check if both resources have high decay (active decomposition)
                        if self.resource_decay[i_resource] > 0.2 and self.resource_decay[j_resource] > 0.2:
                            # Strengthen the connection
                            self.connections[i, j] += 0.1 * dt
                            self.connections[j, i] += 0.1 * dt
                            
                            # Update position to emphasize this connection
                            midpoint = (self.positions[i] + self.positions[j]) / 2
                            self.positions[i] += 0.01 * dt * (midpoint - self.positions[i])
                            self.positions[j] += 0.01 * dt * (midpoint - self.positions[j])
        
    def _update_resources(self, dt: float) -> None:
        """
        Update resource distribution and consumption
        
        COMPLETELY REDESIGNED:
        - Resource-aware distribution system
        - Explicit resource decay based on connections
        - Active resource consumption mechanics
        - Distance-weighted resource distribution
        """
        # Identify nodes connected to each resource
        resource_connected_nodes = {}
        resource_used_connections = {}
        
        for r_idx, r_pos in enumerate(self.resource_positions):
            connected_nodes = []
            
            # Find nodes close to this resource
            for i, pos in enumerate(self.positions):
                if torch.norm(pos - r_pos) < 4.0:  # Increased resource influence radius
                    connected_nodes.append(i)
            
            resource_connected_nodes[r_idx] = connected_nodes
            
            # Calculate how many actual connections this resource has to other resources
            if connected_nodes:
                other_resources_connected = set()
                
                for i in connected_nodes:
                    # Find connections to nodes near other resources
                    for j in range(len(self.positions)):
                        if self.connections[i, j] > 0.2:  # Significant connection
                            # Check if j is near another resource
                            for other_idx, other_pos in enumerate(self.resource_positions):
                                if other_idx != r_idx and torch.norm(self.positions[j] - other_pos) < 4.0:
                                    other_resources_connected.add(other_idx)
                
                # Store actual used connections
                resource_used_connections[r_idx] = len(other_resources_connected)
                # Update resource connections
                self.resource_connections[r_idx] = resource_used_connections.get(r_idx, 0)
        
        # Initialize resource changes
        resource_change = torch.zeros_like(self.resources)
        
        # PHASE 1: Resource flow along connections
        # First, identify resource nodes and their connections
        resource_nodes = {}
        
        for r_idx, nodes in resource_connected_nodes.items():
            resource_nodes[r_idx] = nodes
        
        # Flow resources along connections from resource nodes to network
        for r_idx, nodes in resource_nodes.items():
            if not nodes:
                continue
                
            # Calculate total flow out from this resource
            connected_count = resource_used_connections.get(r_idx, 0)
            total_flow = 0.1 * dt * (1.0 + connected_count * 0.2)  # More flow for well-connected resources
            
            # Flow to each node
            for node_idx in nodes:
                # Share of flow based on connection strength
                total_connection = torch.sum(self.connections[node_idx, :])
                if total_connection > 0:
                    # This node gets resources proportional to its total connection strength
                    flow = total_flow * (total_connection / (len(nodes) * 5.0))
                    resource_change[node_idx] += flow
        
        # PHASE 2: Resource consumption for nodes near resources
        for r_idx, nodes in resource_connected_nodes.items():
            if not nodes:
                continue
                
            # Total consumption proportional to number of connected nodes
            total_consumption = 0.04 * dt * len(nodes)
            
            # Distribute consumption among nodes
            for node_idx in nodes:
                # Consumption based on node activity (connections)
                node_activity = torch.sum(self.connections[node_idx, :])
                consumption = total_consumption * (node_activity / (len(nodes) * 5.0 + 1e-6))
                
                resource_change[node_idx] -= consumption
                
                # Update resource decay
                self.resource_decay[r_idx] += 0.01 * dt * (1.0 + resource_used_connections.get(r_idx, 0) * 0.1)
        
        # PHASE 3: Resource sharing along network connections
        for i in range(len(self.positions)):
            for j in range(len(self.positions)):
                if self.connections[i, j] > 0.2:  # Strong connection
                    # Flow from higher to lower resource levels
                    resource_diff = self.resources[j] - self.resources[i]
                    
                    # Scaled by connection strength and difference
                    flow = 0.05 * dt * self.connections[i, j] * resource_diff
                    resource_change[i] += flow
                    resource_change[j] -= flow
        
        # Apply all resource changes
        self.resources += resource_change
        
        # PHASE 4: Resource growth away from network
        # Growth for nodes that are not connected to the network
        isolated_nodes = []
        for i in range(len(self.positions)):
            total_connections = torch.sum(self.connections[i, :])
            if total_connections < 0.5:  # Not well connected
                isolated_nodes.append(i)
        
        # Add resources to isolated nodes
        for i in isolated_nodes:
            self.resources[i] += 0.02 * dt
        
        # Ensure resources stay within valid range
        self.resources = torch.clamp(self.resources, min=0.1, max=2.0)
        
    def _update_connections(self) -> None:
        """
        Update network connections based on proximity and resources
        
        IMPROVED:
        - Enhanced resource influence on connections
        - Better proximity threshold calculation
        """
        # Calculate physical distance between all nodes
        distances = torch.cdist(self.positions, self.positions)
        
        # Existing connections decay slightly over time
        self.connections *= (1.0 - 0.01)
        
        # New connections form based on proximity
        proximity_mask = distances < self.config.connection_threshold
        proximity_mask.fill_diagonal_(False)  # No self-connections
        
        # IMPROVED: Enhanced resource influence on connections
        resource_factor = torch.outer(self.resources, self.resources) * self.config.resource_influence / 2.0
        
        # Update connections based on proximity and resources
        new_connections = proximity_mask.float() * resource_factor * 0.1
        self.connections = torch.max(self.connections, new_connections)
        
        # Ensure connections are symmetric
        self.connections = 0.5 * (self.connections + self.connections.T)
        
        # Update resource connection counts (degree of connection in paper)
        for r_idx, r_pos in enumerate(self.resource_positions):
            # IMPROVED: Find nodes close to this resource with increased radius
            close_node_indices = []
            for i, pos in enumerate(self.positions):
                if torch.norm(pos - r_pos) < 4.0:  # Increased from 2.0
                    close_node_indices.append(i)
            
            # Count unique connections to other resources
            if close_node_indices:
                connected_resources = set()
                for i in close_node_indices:
                    # Find connected nodes
                    connections = torch.nonzero(self.connections[i] > 0.1).squeeze()
                    if connections.dim() > 0:  # Ensure there's at least one connected node
                        for j in connections:
                            # Determine which resource the connected node is closest to
                            j_dists = [torch.norm(self.positions[j] - res_pos) for res_pos in self.resource_positions]
                            closest_res = np.argmin(j_dists)
                            if closest_res != r_idx:  # Different resource
                                connected_resources.add(closest_res)
                
                # Update resource connections count
                self.resource_connections[r_idx] = len(connected_resources)
                
    def _optimize(self) -> None:
        """Optimize the positions of nodes based on connections"""
        connected = torch.nonzero(self.connections)
        if len(connected) > 0:
            for i, j in connected:
                # Calculate force based on connection strength
                direction = self.positions[j] - self.positions[i]
                distance = torch.norm(direction) + 1e-6  # Avoid division by zero
                
                # Force is stronger for stronger connections, weaker for longer distances
                force = self.connections[i,j] * direction / distance
                
                # Apply forces (move closer for strong connections)
                self.positions[i] += 0.01 * force
                self.positions[j] -= 0.01 * force
                
    def _track_features(self) -> None:
        """Track network features and pattern matching"""
        # Update network pattern matching
        self.current_pattern = self._match_pattern()
        self.pattern_history.append(self.current_pattern)
        
        # Calculate network efficiency
        total_connections = torch.sum(self.connections)
        total_resources = torch.sum(self.resources)
        if total_resources > 0:
            efficiency = total_connections / total_resources
        else:
            efficiency = 0.0
            
        self.efficiency_history.append(efficiency.item())
        
    def _match_pattern(self) -> Optional[str]:
        """Match the current network to known patterns
        
        This uses a combination of:
        1. Connection pattern matching (network topology)
        2. Resource arrangement matching
        3. Position pattern matching
        """
        # Resource arrangement matching first (most important)
        resource_pattern = self._match_resource_pattern()
        if resource_pattern:
            return resource_pattern
            
        # Traditional pattern matching as fallback
        best_match = None
        best_score = 0.0
        
        # Reshape positions for pattern matching
        state = self.positions.reshape(-1)
        
        # Try each pattern
        for name, pattern in self.patterns.items():
            pattern_flat = pattern.reshape(-1)
            
            # Ensure both tensors have the same size
            if pattern_flat.size(0) != state.size(0):
                if pattern_flat.size(0) < state.size(0):
                    padding = torch.zeros(state.size(0) - pattern_flat.size(0), device=pattern_flat.device)
                    pattern_flat = torch.cat([pattern_flat, padding])
                else:
                    pattern_flat = pattern_flat[:state.size(0)]
            
            # Calculate match score using cosine similarity
            score = torch.nn.functional.cosine_similarity(
                state.unsqueeze(0),
                pattern_flat.unsqueeze(0)
            ).item()
            
            if score > best_score:
                best_score = score
                best_match = name
                
        return best_match if best_score > self.config.pattern_threshold else None
    
    def _match_resource_pattern(self) -> Optional[str]:
        """Match patterns based on resource arrangement and connections"""
        # Count connections per resource
        connection_counts = self.resource_connections.cpu().numpy()
        
        # Create network density map (2D histogram)
        x_coords = self.positions[:, 0].cpu().numpy()
        y_coords = self.positions[:, 1].cpu().numpy()
        
        # Check if arrangement matches Circle
        if self.config.resource_arrangement == 'circle':
            # In circle pattern, connection counts should be relatively uniform
            if np.std(connection_counts) < 2.0:
                # Check if network forms a circle-like pattern
                # This uses a simple distance-from-center metric
                distances = np.sqrt(x_coords**2 + y_coords**2)
                # Calculate how circular the network is
                mean_dist = np.mean(distances)
                if mean_dist > 0:
                    distance_std = np.std(distances) / mean_dist
                    if distance_std < 0.5:  # Relatively uniform distance from center
                        return 'circle'
        
        # Check if arrangement matches Cross
        elif self.config.resource_arrangement == 'cross':
            # In cross pattern, outer blocks should have more connections
            if len(connection_counts) >= 9:  # Ensure we have enough resources
                # Classify resources into center, middle, and outer
                center_idx = 0  # Center position
                middle_idx = [1, 2, 3, 4]  # Middle positions
                outer_idx = [5, 6, 7, 8]  # Outer positions
                
                # Calculate average connections per group
                if np.mean(connection_counts[outer_idx]) > np.mean(connection_counts[middle_idx]):
                    # Check if network forms a cross-like pattern
                    # This looks at the density along the x and y axes vs. diagonals
                    axis_density = np.sum((np.abs(x_coords) < 1.0) | (np.abs(y_coords) < 1.0))
                    diagonal_density = len(x_coords) - axis_density
                    
                    # If density is higher along axes than diagonals, it's cross-like
                    if axis_density > diagonal_density:
                        return 'cross'
        
        # No specific resource pattern matched
        return None
        
    def get_state(self) -> Dict:
        """Return the current state of the network region"""
        return {
            'positions': self.positions.cpu(),
            'resources': self.resources.cpu(),
            'connections': self.connections.cpu(),
            'resource_positions': [r.cpu() for r in self.resource_positions],
            'resource_decay': self.resource_decay.cpu(),
            'resource_connections': self.resource_connections.cpu(),
            'current_pattern': self.current_pattern,
            'efficiency': self.efficiency_history[-1] if self.efficiency_history else 0.0,
            'state': self.state,
            'steps': self.steps
        }

class FungalNetwork:
    def __init__(self, config: NetworkConfig, num_regions: int = 1):
        # Initialize Ray if not already done
        if not ray.is_initialized():
            ray.init()
            
        self.config = config
        self.regions = [NetworkRegion.remote(config, i) for i in range(num_regions)]
        self.start_time = time.time()
        
        # Create visualizations directory
        self.viz_dir = "fungal_network_viz"
        os.makedirs(self.viz_dir, exist_ok=True)
        
        # Register cleanup function
        atexit.register(self.cleanup)
        
    def step(self, dt: float) -> None:
        try:
            ray.get([region.update.remote(dt) for region in self.regions])
        except Exception as e:
            logger.error(f"Error during step: {e}")
            raise
        
    def get_state(self) -> Dict:
        try:
            states = ray.get([region.get_state.remote() for region in self.regions])
            return {
                'positions': torch.cat([s['positions'] for s in states]),
                'resources': torch.cat([s['resources'] for s in states]),
                'connections': torch.block_diag(*[s['connections'] for s in states]),
                'resource_positions': states[0]['resource_positions'],  # Use first region
                'resource_decay': states[0]['resource_decay'],
                'resource_connections': states[0]['resource_connections'],
                'patterns': [s['current_pattern'] for s in states],
                'efficiency': [s['efficiency'] for s in states],
                'states': [s['state'] for s in states],
                'steps': states[0]['steps']
            }
        except Exception as e:
            logger.error(f"Error getting state: {e}")
            return {}
            
    def visualize(self, step: int) -> None:
        """
        Create visualization of the current network state
        
        FURTHER IMPROVED:
        - Added dual visualization: full view and zoomed view
        - Enhanced node and connection visualization
        - Dynamic axis scaling based on content
        - Added node density heatmap
        - Added detailed statistics display
        """
        try:
            state = self.get_state()
            if not state:
                return
                
            # Create a figure with two subplots: full view and zoomed view
            fig = plt.figure(figsize=(18, 10))
            
            # Create GridSpec for layout control - simplified to not use heatmap
            gs = plt.GridSpec(1, 3, width_ratios=[2, 2, 1], figure=fig, wspace=0.3, hspace=0.3)
            
            # Full view subplot
            ax_full = fig.add_subplot(gs[0])
            # Zoomed view subplot
            ax_zoom = fig.add_subplot(gs[1])
            # Stats subplot - text only, no plots
            ax_stats = fig.add_subplot(gs[2])
            ax_stats.axis('off')  # Turn off axis for stats panel
            
            # Extract data
            positions = state['positions'].numpy()
            connections = state['connections'].numpy()
            resources = state['resources'].numpy()
            resource_positions = [r.numpy() for r in state['resource_positions']]
            resource_decay = state['resource_decay'].numpy()
            resource_connections = state['resource_connections'].numpy()
            pattern = state['patterns'][0]  # Use first region's pattern
            
            # Calculate network statistics
            connection_count = np.sum(connections > 0.1) / 2  # Divide by 2 to count each connection once
            avg_connection_strength = np.mean(connections[connections > 0.1]) if np.any(connections > 0.1) else 0
            total_resource = np.sum(resources)
            
            # Calculate the range of node positions for auto-zooming
            x_positions = positions[:, 0]
            y_positions = positions[:, 1]
            
            # For full view: show all resources
            r_x_positions = np.array([r[0] for r in resource_positions])
            r_y_positions = np.array([r[1] for r in resource_positions])
            
            # Calculate bounds for full view (include all resources)
            full_x_min, full_x_max = np.min(r_x_positions) - 2, np.max(r_x_positions) + 2
            full_y_min, full_y_max = np.min(r_y_positions) - 2, np.max(r_y_positions) + 2
            
            # Ensure aspect ratio is maintained
            full_x_range = full_x_max - full_x_min
            full_y_range = full_y_max - full_y_min
            if full_x_range > full_y_range:
                # Expand y-range to match x-range aspect ratio
                margin = (full_x_range - full_y_range) / 2
                full_y_min -= margin
                full_y_max += margin
            else:
                # Expand x-range to match y-range aspect ratio
                margin = (full_y_range - full_x_range) / 2
                full_x_min -= margin
                full_x_max += margin
                
            # Calculate bounds for zoomed view (focus on active nodes)
            # Find non-isolated nodes that have connections
            active_nodes = np.where(np.sum(connections, axis=1) > 0)[0]
            
            if len(active_nodes) > 0:
                # Use active nodes for zooming
                active_x = x_positions[active_nodes]
                active_y = y_positions[active_nodes]
                
                # Calculate active node bounds
                x_min, x_max = np.min(active_x), np.max(active_x)
                y_min, y_max = np.min(active_y), np.max(active_y)
                
                # Add margin
                x_margin = max(1.0, (x_max - x_min) * 0.2)
                y_margin = max(1.0, (y_max - y_min) * 0.2)
                
                zoom_x_min = x_min - x_margin
                zoom_x_max = x_max + x_margin
                zoom_y_min = y_min - y_margin
                zoom_y_max = y_max + y_margin
                
                # Include nearby resources in the zoomed view
                for r_pos in resource_positions:
                    if (zoom_x_min <= r_pos[0] <= zoom_x_max and 
                        zoom_y_min <= r_pos[1] <= zoom_y_max):
                        # Resource is already in view
                        continue
                    
                    # Check if resource is close to the view
                    x_dist = min(abs(r_pos[0] - zoom_x_min), abs(r_pos[0] - zoom_x_max))
                    y_dist = min(abs(r_pos[1] - zoom_y_min), abs(r_pos[1] - zoom_y_max))
                    
                    if x_dist < 2.0 and y_dist < 2.0:
                        # Expand view to include this resource
                        if r_pos[0] < zoom_x_min:
                            zoom_x_min = r_pos[0] - 0.5
                        elif r_pos[0] > zoom_x_max:
                            zoom_x_max = r_pos[0] + 0.5
                            
                        if r_pos[1] < zoom_y_min:
                            zoom_y_min = r_pos[1] - 0.5
                        elif r_pos[1] > zoom_y_max:
                            zoom_y_max = r_pos[1] + 0.5
            else:
                # If no active nodes, use a default zoom around the center
                zoom_x_min, zoom_x_max = -5, 5
                zoom_y_min, zoom_y_max = -5, 5
                
            # Ensure minimal zoom area even with few nodes
            min_range = 3.0  # Minimum range to show
            if zoom_x_max - zoom_x_min < min_range:
                center = (zoom_x_max + zoom_x_min) / 2
                zoom_x_min = center - min_range/2
                zoom_x_max = center + min_range/2
                
            if zoom_y_max - zoom_y_min < min_range:
                center = (zoom_y_max + zoom_y_min) / 2
                zoom_y_min = center - min_range/2
                zoom_y_max = center + min_range/2
            
            # Draw in both views
            for ax, is_zoomed in [(ax_full, False), (ax_zoom, True)]:
                # Set view limits
                if is_zoomed:
                    ax.set_xlim(zoom_x_min, zoom_x_max)
                    ax.set_ylim(zoom_y_min, zoom_y_max)
                    ax.set_title(f"Zoomed View - Active Network")
                else:
                    ax.set_xlim(full_x_min, full_x_max)
                    ax.set_ylim(full_y_min, full_y_max)
                    ax.set_title(f"Full View - Step {step}: {state['states'][0].name}")
                
                # Draw connections with enhanced color and opacity scaling
                for i in range(len(positions)):
                    for j in range(i+1, len(positions)):
                        if connections[i, j] > 0.1:
                            # Color connections based on strength
                            strength = min(1.0, connections[i, j])
                            color = plt.cm.Blues(0.5 + strength/2)  # Stronger connections are darker blue
                            ax.plot([positions[i, 0], positions[j, 0]],
                                    [positions[i, 1], positions[j, 1]],
                                    color=color, alpha=min(0.8, strength), 
                                    linewidth=max(0.5, connections[i, j] * 1.5))
                
                # Draw nodes colored by resource level with size based on connectivity
                node_colors = plt.cm.viridis(resources / max(2.0, resources.max()))
                
                # Node size based on connectivity and zoomed status (larger in zoomed view)
                base_size = 15 if is_zoomed else 10
                scaling = 8 if is_zoomed else 5
                node_sizes = np.sum(connections, axis=1) * scaling + base_size
                
                ax.scatter(positions[:, 0], positions[:, 1], c=node_colors, s=node_sizes, alpha=0.7, zorder=10)
                
                # Draw resources with enhanced visual indicators - IMPROVED: Red color and higher z-order
                for i, r_pos in enumerate(resource_positions):
                    # Size based on decay, but now with red color for better visibility
                    base_resource_size = 300 if is_zoomed else 200
                    size = base_resource_size + 800 * resource_decay[i]
                    
                    # Fixed red color instead of plasma colormap for better visibility
                    # Vary the intensity based on connections
                    color_val = min(1.0, resource_connections[i] / max(1.0, resource_connections.max()))
                    red_color = [1.0, 0.3 * (1-color_val), 0.3 * (1-color_val), 0.8]  # Bright red with varying intensity
                    
                    # Draw resource with high zorder (20) to ensure it appears on top
                    ax.scatter(r_pos[0], r_pos[1], c=[red_color], s=size, alpha=0.9, 
                              marker='s', zorder=20, edgecolors='black', linewidths=1)
                    
                    # Add formatted resource connection count - white text with black outline for better contrast
                    connection_text = f"{resource_connections[i]:.1f}" if resource_connections[i] < 100 else f"{resource_connections[i]:.0f}"
                    ax.text(r_pos[0], r_pos[1], connection_text, ha='center', va='center', 
                           fontweight='bold', color='white', zorder=25,  # Higher zorder than resource
                           path_effects=[plt.matplotlib.patheffects.withStroke(linewidth=2, foreground='black')])  # Text outline
                
                # Draw connections between connected resources for better visualization
                for i in range(len(resource_positions)):
                    for j in range(i+1, len(resource_positions)):
                        # If both resources have connections, show a link between them
                        if resource_connections[i] > 0 and resource_connections[j] > 0:
                            # Opacity based on connection strength
                            combined_strength = min(1.0, (resource_connections[i] + resource_connections[j]) / 200)
                            ax.plot([resource_positions[i][0], resource_positions[j][0]],
                                   [resource_positions[i][1], resource_positions[j][1]],
                                   'g--', alpha=0.2 + 0.6 * combined_strength, linewidth=1 + combined_strength)
                
                # Add grid for better reference
                ax.grid(True, alpha=0.2)
                
                # Add equal aspect to maintain shape
                ax.set_aspect('equal')
                
            # Display network stats in the third subplot directly
            # No heatmap, just stats panel for cleaner layout
            
            # Enhanced network statistics text (without heatmap, we can make this more detailed)
            stats_text = (
                f"Network Statistics\n"
                f"------------------\n"
                f"Step: {step}\n"
                f"Pattern: {pattern if pattern else 'No pattern'}\n"
                f"State: {state['states'][0].name}\n\n"
                f"Nodes: {len(positions)}\n"
                f"Connections: {connection_count:.0f}\n"
                f"Avg Strength: {avg_connection_strength:.3f}\n"
                f"Total Resource: {total_resource:.1f}\n\n"
                f"Resource Connections:\n"
            )
            
            for i, conn in enumerate(resource_connections):
                stats_text += f"  R{i+1}: {conn:.1f}\n"
                
            stats_text += f"\nResource Decay:\n"
            for i, decay in enumerate(resource_decay):
                stats_text += f"  R{i+1}: {decay*100:.1f}%\n"
            
            # Place text in the stats axis panel
            ax_stats.text(0.5, 0.5, stats_text, fontsize=10, 
                          verticalalignment='center', horizontalalignment='center',
                          transform=ax_stats.transAxes,
                          bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
            
            # Add shared legend at the bottom
            handles = [
                plt.Line2D([0], [0], color='blue', lw=2, alpha=0.7, label='Node connections'),
                plt.Line2D([0], [0], color='green', lw=1, linestyle='--', alpha=0.7, label='Resource connections'),
                plt.scatter([0], [0], c='green', s=100, alpha=0.5, marker='s', label='Resources'),
                plt.scatter([0], [0], c='blue', s=50, alpha=0.7, label='Nodes')
            ]
            fig.legend(handles=handles, loc='lower center', ncol=4, framealpha=0.7, fontsize=10)
            
            # Using simple figure adjustments instead of tight_layout to avoid warnings
            plt.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9, wspace=0.25)
            
            # Save figure with better DPI for higher quality
            filename = os.path.join(self.viz_dir, f"network_step_{step:04d}.png")
            plt.savefig(filename, dpi=150)
            plt.close(fig)
            
            logger.info(f"Saved visualization to {filename}")
            
        except Exception as e:
            logger.error(f"Error creating visualization: {e}")
            import traceback
            logger.error(traceback.format_exc())
    
    def cleanup(self):
        """Clean up resources properly"""
        # Make sure regions are released
        self.regions = []
        
        # Log total runtime
        runtime = time.time() - self.start_time
        logger.info(f"Total runtime: {runtime:.2f} seconds")
        
        # Don't shut down Ray here if it might be used elsewhere in the application

def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    """
    Call in a loop to create terminal progress bar
    """
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

def run_simulation(name, config, total_steps=200):
    """Run a simulation with progress feedback"""
    logger.info(f"Starting {name} arrangement simulation...")
    try:
        network = FungalNetwork(config)
        
        # Log initial state
        logger.info(f"Initialized {name} network with {config.num_nodes} nodes and {config.num_resources} resources")
        
        for step in range(total_steps):
            # Update progress bar every step
            print_progress_bar(step + 1, total_steps, prefix=f'{name} Progress:', 
                              suffix=f'Step {step+1}/{total_steps}', length=40)
            
            # Process step
            network.step(0.1)
            
            # Visualize periodically
            if step % 10 == 0 or step == total_steps - 1:
                network.visualize(step)
                
            # Log detailed status periodically    
            if step % 20 == 0 or step == total_steps - 1:
                state = network.get_state()
                
                # Show pattern and state
                pattern = state['patterns'][0] if 'patterns' in state else None
                net_state = state['states'][0].name if 'states' in state else "Unknown"
                logger.info(f"\n{name}: Step {step}, Pattern: {pattern}, State: {net_state}")
                
                # Log resource connections and decay
                if 'resource_connections' in state and 'resource_decay' in state:
                    conn = state['resource_connections'].numpy()
                    decay = state['resource_decay'].numpy()
                    
                    # Format for readability
                    conn_str = ', '.join([f"{c:.1f}" for c in conn])
                    decay_str = ', '.join([f"{d*100:.1f}%" for d in decay])
                    
                    logger.info(f"{name}: Resource Connections: [{conn_str}]")
                    logger.info(f"{name}: Resource Decay: [{decay_str}]")
                    
                # Log memory usage
                import psutil
                process = psutil.Process()
                memory_info = process.memory_info()
                logger.info(f"Memory usage: {memory_info.rss / 1024 / 1024:.1f} MB")
                
        logger.info(f"{name} simulation completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in {name} simulation: {e}")
    finally:
        if ray.is_initialized():
            ray.shutdown()
            logger.info(f"Ray resources for {name} simulation released")

if __name__ == "__main__":
    logger.info("Starting Fungal Network Algorithm simulation")
    logger.info(f"Using device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    
    # FURTHER OPTIMIZED: Enhanced parameters for better network formation
    circle_config = NetworkConfig(
        num_nodes=300,               # Increased node count for denser network connections
        space_dims=(50, 50, 1),      # Larger space for better resource distribution
        growth_rate=0.3,             # Much higher growth rate for faster network development
        decay_rate=0.03,             # Balanced decay
        connection_threshold=3.0,    # Increased for more selective connections
        pattern_threshold=0.4,       # Lowered to detect patterns more easily
        resource_influence=4.0,      # Significantly stronger influence
        resource_arrangement='circle',
        num_resources=9,
        resource_spacing=15.0        # Much larger spacing between resources
    )
    
    # FURTHER OPTIMIZED: Enhanced parameters for cross arrangement
    cross_config = NetworkConfig(
        num_nodes=300,               # Increased node count for denser network connections
        space_dims=(50, 50, 1),      # Larger space for better resource distribution 
        growth_rate=0.3,             # Much higher growth rate for faster network development
        decay_rate=0.03,             # Balanced decay
        connection_threshold=3.0,    # Increased for more selective connections
        pattern_threshold=0.4,       # Lowered to detect patterns more easily
        resource_influence=4.0,      # Significantly stronger influence
        resource_arrangement='cross',
        num_resources=9,
        resource_spacing=15.0        # Much larger spacing between resources
    )
    
    # Run circle simulation with progress feedback
    run_simulation("Circle", circle_config, total_steps=200)
    
    # Run cross simulation with progress feedback
    run_simulation("Cross", cross_config, total_steps=200)
    
    logger.info("All simulations completed!")
    logger.info(f"Visualizations saved to {os.path.abspath('fungal_network_viz')}")