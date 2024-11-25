# search.py
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

    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Calculate Manhattan distance between two positions."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def bfs(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        """BFS implementation that returns both path and explored nodes."""
        queue = deque([[start]])
        visited = {start}
        explored_nodes = []
        
        while queue:
            path = queue.popleft()
            current = path[-1]
            explored_nodes.append(current)
            
            if current == goal:
                return path[1:], explored_nodes
            
            for next_pos in self.get_legal_moves(current):
                if next_pos not in visited:
                    visited.add(next_pos)
                    new_path = list(path)
                    new_path.append(next_pos)
                    queue.append(new_path)
        
        return [], explored_nodes

    def dfs(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        """DFS implementation that returns both path and explored nodes."""
        stack = [[start]]
        visited = {start}
        explored_nodes = []
        
        while stack:
            path = stack.pop()
            current = path[-1]
            explored_nodes.append(current)
            
            if current == goal:
                return path[1:], explored_nodes
            
            for next_pos in reversed(self.get_legal_moves(current)):
                if next_pos not in visited:
                    visited.add(next_pos)
                    new_path = list(path)
                    new_path.append(next_pos)
                    stack.append(new_path)
        
        return [], explored_nodes

    def a_star(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        """A* implementation that returns both path and explored nodes."""
        frontier = PriorityQueue()
        frontier.put((0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}
        explored_nodes = []
        
        while not frontier.empty():
            current = frontier.get()[1]
            explored_nodes.append(current)
            
            if current == goal:
                # Reconstruct path
                path = []
                while current != start:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path, explored_nodes
                
            for next_pos in self.get_legal_moves(current):
                new_cost = cost_so_far[current] + 1
                
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + self.manhattan_distance(next_pos, goal)
                    frontier.put((priority, next_pos))
                    came_from[next_pos] = current
        
        return [], explored_nodes