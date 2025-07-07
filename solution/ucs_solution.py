from __future__ import annotations  # Allows a class to contain type hints that refer to itself. We use Node instead of 'Node'
from model import Node
from .solution import Solution

import heapq

class UCS(Solution):
    name = "UCS"
    
    def calculate_cost(self, parent_cost: int, new_cost: int):
        return parent_cost + new_cost

    def calculate_heuristic(self, current_node: Node):
        return 0

    def get_successors(self, current_node):
        return super().get_successors(current_node)
    
    def solve(self) -> Node:
        frontier = []
        path_cost = {} # Store g(n) of each node and update if it's optimal

        heapq.heappush(frontier, (0, self.initial_node))
        path_cost[self.initial_node] = self.initial_node.cost

        while frontier:
            f_cost, current_node = heapq.heappop(frontier)

            # Crucial
            if current_node.cost > path_cost[current_node]:
                continue
            
            if current_node.is_goal():
                self.total_cost = current_node.cost
                
                return current_node
        
            self.number_expanded_nodes += 1

            for node in self.get_successors(current_node):
                if node not in path_cost or node.cost < path_cost[node]:
                    path_cost[node] = node.cost
                    node.parent = current_node
                    heapq.heappush(frontier, (node.cost, node))
                    
        raise ValueError("The puzzle cannot be solved. No solution found.")
    
    def print_informations(self, goal_node: Node):
        return super().print_informations(goal_node)

    def find_path(self, goal_node: Node) -> list:
        return super().find_path(goal_node)