from solution import AStar, UCS, BFS, IDS
from model import Car, Node
from collections import defaultdict

import tracemalloc
import numpy as np
import time 
import sys
import os
import psutil
import os

def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

<<<<<<< Updated upstream
def read_map(path):
    with open(path) as file:
=======
def main():
    
    with open("Map/11.txt") as file:
>>>>>>> Stashed changes
        lines = [list(line.strip()) for line in file.readlines()]

    matrix = np.array(lines, dtype=str) # Matrix 10x10

    return matrix

def store_car(matrix):
    cars = defaultdict(list)
    all_cars = []

    for i in range(10):
        for j in range(10):
            if matrix[i][j] != "-" and matrix[i][j] != 'X':
                cars[matrix[i][j]].append((i, j))   
    
    for car_id, positions in cars.items(): 
        dir = ''
        if isinstance(positions, list):
            size = len(positions)
            if positions[0][0] == positions[1][0]:
                dir = 'h'
            else:
                dir = 'v'
        
        car = Car(id = car_id, dir = dir, row = positions[0][0], col = positions[0][1], size = size)
        all_cars.append(car)
    
    return cars, all_cars

<<<<<<< Updated upstream
def calculate_used_resourcess(solution):
    # tracemalloc.start()
=======
    A = Node(cars=all_cars)
    
    solver_classes = [AStar, BFS, UCS, IDS]

# Use the built-in __name__ for the key and your custom display_name for the value
    solvers = {solver_class.name: solver_class for solver_class in solver_classes}
    algo = solvers["AStar"]

    solution = algo(A)
                      
>>>>>>> Stashed changes
    start_time = time.perf_counter()
    start_mem = process_memory()

    goal_node = solution.solve()

    # start_mem, end_mem = tracemalloc.get_traced_memory()
    end_mem = process_memory()
    tracemalloc.stop()
    end_time = time.perf_counter()

<<<<<<< Updated upstream
    search_time = end_time - start_time
    memory_usage = end_mem - start_mem    
    
    return goal_node, search_time, memory_usage

def print_path(path):
=======
    peak_memory_usage = end_mem - start_mem
    solution.search_time = end_time - start_time
    solution.memory_usage = peak_memory_usage 

    print(solution.memory_usage)

    path = solution.find_path(goal_node)
    solution.print_informations(goal_node)

>>>>>>> Stashed changes
    for i, node in enumerate(path):
        print(f"\n-----Step {i} -----")
        if i == 0:
            print ("Initial node")
        elif node.action:
            print(f"Action : {node.action}")
        
        print(node)

    print("Goal node")
<<<<<<< Updated upstream

def main():
    map = read_map("Map/11.txt")

    cars, all_cars = store_car(map)

    A = Node(cars=all_cars)
    solution = UCS(A)
                    
    goal_node, solution.search_time, solution.memory_usage = calculate_used_resourcess(solution)

    path = solution.find_path(goal_node)
    solution.print_informations(goal_node)

    print_path(path)
=======
>>>>>>> Stashed changes

if __name__ == "__main__":
    main()