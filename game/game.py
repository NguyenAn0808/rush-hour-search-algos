from model import Car, Node
from solution import Solution, BFS, UCS, AStar, IDS

class Game:
    def __init__(self, initial_node: Node, name_algo: str):
        self.initial_node = initial_node

        self.name_algo = name_algo    
        solver_classes = [AStar, BFS, UCS, IDS]
    
        solvers = {solver_class.name: solver_class for solver_class in solver_classes}
        self.algorithm = solvers[self.name_algo]
    
        self.solution = self.algorithm(initial_node)

        self.is_playing = False 
        self.reset = False

        # Animation
        self.solution_path = []
        self.step = 0
        
        #Display message
        self.message = ""
        

       # self.display_game()


