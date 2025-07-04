from __future__ import annotations  # Allows a class to contain type hints that refer to itself. We use Node instead of 'Node'
from model import Node
from .solution import Solution
from collections import deque

MAX_DEPTH = 100

class IDS(Solution):
    name = "IDS"
    
    def calculate_cost(self, parent_cost: int, new_cost: int):
        return 0
    
    def calculate_heuristic(self, current_node: Node):
        return 0

    def get_successors(self, current_node):
        return super().get_successors(current_node)
    
    def dls(self, start_node: Node, depth_limit) -> Node:
        # Push dô stack
        Stack = deque([(start_node, 0)])          
        visited = {start_node}

        while len(Stack) != 0:
            # Expand node
            current_node, depth = Stack.popleft()
            self.number_expanded_nodes += 1

            if current_node.is_goal():
                return current_node
            
            if depth >= depth_limit:
                continue

            for new_node in self.get_successors(current_node):   
                if new_node not in visited:          
                    new_node.parent = current_node

                    Stack.appendleft((new_node, depth + 1))
                    visited.add(new_node)         

        return None
                    
    def solve(self) -> Node: # IDS
        for depth_limit in range(MAX_DEPTH + 1):
            current_state = self.dls(self.initial_node, depth_limit)
            if current_state:
                print(depth_limit)
                return current_state
            
        return None

    def print_informations(self, goal_node: Node):
        self.number_expanded_nodes -= 1
        return super().print_informations(goal_node)

    def find_path(self, goal_node: Node) -> list:
        return super().find_path(goal_node)
