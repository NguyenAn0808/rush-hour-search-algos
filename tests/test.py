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

def read_map(path):
    with open(path) as file:
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
    
    return all_cars

def calculate_used_resourcess(solution):
    # tracemalloc.start()
    start_time = time.perf_counter()
    start_mem = process_memory()

    goal_node = solution.solve()

    # start_mem, end_mem = tracemalloc.get_traced_memory()
    end_mem = process_memory()
    tracemalloc.stop()
    end_time = time.perf_counter()

    search_time = end_time - start_time
    memory_usage = end_mem - start_mem    
    
    return goal_node, search_time, memory_usage

def print_path(path):
    for i, node in enumerate(path):
        print(f"\n-----Step {i} -----")
        if i == 0:
            print ("Initial node")
        elif node.action:
            print(f"Action : {node.action}")
        
        print(node)

    print("Goal node")

def main():
    # X X X X X X X X X X
    # X X X X X X X X X X
    # X X - - - Y Y Y X X
    # X X - - - - - - X X
    # X X - - A G G F - -
    # X X E E A - D F X X
    # X X C - A - D F X X
    # X X C - B B B - X X
    # X X X X X X X X X X
    # X X X X X X X X X X

    # "X": outside play area, "-": possible position, "alphabet": car/truck 
    # map: save as matrix
    map = read_map("tests/test_map.txt")

    # all_cars: list of obstacle vehicles (include: id, direction, x, y, length)
    all_cars = store_car(map)
    
    A = Node(cars=all_cars)
    print(A)
    # Class solution has acccesible property: init_state, number of expanded nodes, search time, memory usage, total cost, step count
    solution = AStar(A)
    print(solution.calculate_heuristic(solution.initial_node))
    # goal_node = goal state            
    # goal_node, solution.search_time, solution.memory_usage = calculate_used_resourcess(solution)
    # print(solution.initial_node.heuristic)
    # path: list of states in solution path 
    # path = solution.find_path(goal_node)

    # print number of expanded nodes, search time, memory usage, total cost, step count
    # solution.print_informations(goal_node)

    # print solution path
    # print_path(path)

if __name__ == "__main__":
 main()
