from __future__ import annotations # Allows a class to contain type hints that refer to itself. We use Node instead of 'Node'
from model.car import Car

class Node:  
    """
    A node is used to represent the state in the search space.
    State here is a matrix 6x6 with a goal state is moving the speicify car to the exit.
    The node contains the matrix, the position of all cars, parent node, heuristic value and the cost of the current node from initial state.
    """
    def __init__(self, cars: list[Car], action=None, parent: Node | None = None, cost: int = 0, heuristic: int = 0):
        self.cars = cars  # List of cars in the current state

        self.cars_tuple = tuple(sorted(self.cars, key = lambda car: car.id))  # Convert list of cars to a tuple for hashing and equality checks

        self.action = action  # Action taken to reach this node, need to trace the path back to the initial state
        self.parent = parent  # Parent node to trace the path back to the initial state

        self.cost = cost  # g(n) is the cost from the initial state to the current node
        self.heuristic = heuristic  # h(n) = Heuristic value for A*
        
        self.state = [["X" for _ in range(10)] for _ in range(10)]  # Initialize a 10x10 matrix with "X" cells
        self.state[4][8] = self.state[4][9] = '-'

        for i in range(2, 8):
            for j in range(2, 8):
                if self.state[i][j] == 'X':
                    self.state[i][j] = '-'

        for car in self.cars:
            # Place each car in the matrix 
            for row, col in car.get_cells_of_car():
                self.state[row][col] = car.id
    
    def __hash__(self) -> int:
        return hash(self.cars_tuple) # Use the tuple of cars for hashing
    # Print node
    def __str__(self) -> str:
        return "\n".join([" ".join(row) for row in self.state])

    def __eq__(self, other: Node) -> bool:
        """
        Check if two nodes are equal based on their cars and f(n).
        """
        return self.cars_tuple == other.cars_tuple
    
    def __lt__(self, other: Node) -> bool:
        """
        Compare with another node with f(n) = g(n) + h(n) = cost + heuristic.
        """
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)
       
    def get_goal_car(self) -> Car | None:
        for car in self.cars:
            if car.id == 'G':
                return car
        return None 
    
    def is_goal(self) -> bool: 
        car = self.get_goal_car()
        if car is None:
            return False
        else:
            return (car.id == 'G' and car.col == 6)

    def is_valid_move(self, car: Car, name_move: str) -> bool:
        row, col = car.row, car.col 

        if name_move == "left":
            return (col > 2 and self.state[row][col - 1] == '-')
        elif name_move == "right":
            return (col + car.size <= 7 and self.state[row][col + car.size] == '-')
        elif name_move == "up":
            return (row > 2 and self.state[row - 1][col] == '-')
        else: # down
            return (row + car.size <= 7 and self.state[row + car.size][col] == '-')

        return False 
    
    def get_next_possible_moves(self):    
        h_move = [('left', 0, -1), ('right', 0, 1)]  # 'h'
        v_move = [('up', -1, 0), ('down', 1, 0)]     # 'v'
        
        for car in self.cars:
            move = h_move if car.dir == 'h' else v_move

            for name_move, drow, dcol in move:
                if self.is_valid_move(car, name_move):
                    # top-left corner
                    new_row = car.row + drow
                    new_col = car.col + dcol 

                    temp_cars = self.cars.copy()
                    new_car = Car(car.id, car.dir, new_row, new_col, car.size)

                    if car in temp_cars:
                        temp_cars.remove(car)
                        temp_cars.append(new_car)

                    action = f"Move {car.id} {name_move}"
                    yield temp_cars, action, new_car 
