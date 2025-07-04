from solution import AStar, UCS, BFS, IDS
from model import Car, Node
from collections import defaultdict

import tracemalloc
import numpy as np
import time 
import psutil
import os

def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

def main():
    
    with open("Map/expert.txt") as file:
        lines = [list(line.strip()) for line in file.readlines()]

    matrix = np.array(lines, dtype=str) # Matrix 10x10

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

    A = Node(cars=all_cars)
    solution = AStar(A)
                      
    start_time = time.perf_counter()
    # tracemalloc.start()
    start_mem = process_memory()
    goal_node = solution.solve()

    # start_mem, end_mem = tracemalloc.get_traced_memory()
    end_mem = process_memory()
    tracemalloc.stop()
    end_time = time.perf_counter()

    solution.search_time = end_time - start_time
    solution.memory_usage = end_mem - start_mem

    print(solution.memory_usage)

    # solution.print_informations(goal_node)
    # path = solution.find_path(goal_node)

    # for i, node in enumerate(path):
    #     print(f"\n-----Step {i} -----")
    #     if i == 0:
    #         print ("Initial node")
    #     elif node.action:
    #         print(f"Action : {node.action}")
        
    #     print(node)

    # print("Goal node")

if __name__ == "__main__":
    main()