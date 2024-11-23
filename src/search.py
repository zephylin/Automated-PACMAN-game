from collections import deque
from queue import PriorityQueue
from typing import List, Tuple, Dict, Set
from .constants import *

class SearchAlgorithms:
    def __init__(self, maze):
        self.maze = maze

    def get_legal_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Returns list of legal moves from current position."""
        moves = []
        for direction in DIRECTIONS.values():
            new_x = pos[0] + direction[0]
            new_y = pos[1] + direction[1]
            
            # Check if the move is within bounds and not a wall
            if (0 <= new_x < len(self.maze) and 
                0 <= new_y < len(self.maze[0]) and 
                self.maze[new_x][new_y] != WALL):
                moves.append((new_x, new_y))
        return moves

    def bfs(self, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Breadth-First Search implementation.
        Returns the shortest path from start to goal.
        """
        # Initialize the queue and visited set
        queue = deque([[start]])
        visited = {start}
        
        while queue:
            # Get the current path
            path = queue.popleft()
            current = path[-1]
            
            # Check if we've reached the goal
            if current == goal:
                return path[1:]  # Exclude the start position
            
            # Explore neighbors
            for next_pos in self.get_legal_moves(current):
                if next_pos not in visited:
                    visited.add(next_pos)
                    new_path = list(path)
                    new_path.append(next_pos)
                    queue.append(new_path)
        
        return []  # No path found

    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Calculate Manhattan distance between two positions."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def a_star(self, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        A* Search implementation.
        Returns the optimal path from start to goal using Manhattan distance heuristic.
        """
        # Initialize the priority queue and tracking dictionaries
        frontier = PriorityQueue()
        frontier.put((0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}
        
        while not frontier.empty():
            current = frontier.get()[1]
            
            if current == goal:
                break
                
            for next_pos in self.get_legal_moves(current):
                new_cost = cost_so_far[current] + 1
                
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + self.manhattan_distance(next_pos, goal)
                    frontier.put((priority, next_pos))
                    came_from[next_pos] = current
        
        # Reconstruct path
        if goal not in came_from:
            return []
            
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def find_nearest_target(self, start: Tuple[int, int], targets: List[Tuple[int, int]], 
                          use_bfs: bool = False) -> Tuple[List[Tuple[int, int]], Tuple[int, int]]:
        """
        Find the nearest target position and the path to reach it.
        targets: List of target positions (e.g., food pellets)
        use_bfs: If True, uses BFS; if False, uses A*
        Returns: (path_to_target, target_position)
        """
        nearest_path = []
        nearest_target = None
        min_distance = float('inf')
        
        for target in targets:
            # Use Manhattan distance for initial filtering
            dist = self.manhattan_distance(start, target)
            if dist < min_distance:
                # Find actual path using selected algorithm
                path = self.bfs(start, target) if use_bfs else self.a_star(start, target)
                if path and len(path) < min_distance:
                    min_distance = len(path)
                    nearest_path = path
                    nearest_target = target
                    
        return nearest_path, nearest_target