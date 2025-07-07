from collections import defaultdict

import numpy as np

from model.car import Car


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