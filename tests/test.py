from model.car import Car

def calculate_minimum_unique_cars(path_to_clear: list[tuple[int, int]], blocker: Car, visited: set[str], 
                            cell_of_cars: dict[tuple[int, int]], space: int) -> tuple[int, set[str]]:
    """
    Calculates the min cost and min cars need to move to clear a path of cells
    """

    if blocker.id in visited:
        return (int(1e9), set()) # Has a cycle, cars cannot be considered twice

    new_visited = visited.copy()
    new_visited.add(blocker.id)

    result = set() # 1 car = 1 cost

    # Move to clear the way 
    for cell in path_to_clear:
        row, col = cell

        if not (2 <= row <= 7 and 2 <= col <= 7):
            return (int(1e9), set())

        if cell in cell_of_cars and cell_of_cars[cell].id != blocker.id:
            # Blocked situation -> recursion 
            blocker = cell_of_cars[cell]

            if blocker.dir == 'h':
                space_left = (blocker.col + blocker.size) - col
                path_left = [(blocker.row, blocker.col - i) for i in range(1, space_left + 1)]

                cost_left, moved_cars_left = calculate_minimum_unique_cars(path_left, blocker, new_visited, cell_of_cars, space_left)

                space_right = (col + 1) - blocker.col
                path_right = [(blocker.row, blocker.col + blocker.size - 1 + i) for i in range(1, space_right + 1)]
                cost_right, moved_cars_right = calculate_minimum_unique_cars(path_right, blocker, new_visited, cell_of_cars, space_right)

                if cost_left < cost_right:
                    result.update(moved_cars_left)
                else:
                    result.update(moved_cars_right)

            else:
                space_down = (row + 1) - blocker.row
                path_down = [(blocker.row + blocker.size - 1 + i, blocker.col) for i in range(1, space_down + 1)]
                cost_down, moved_cars_down = calculate_minimum_unique_cars(path_down, blocker, new_visited, cell_of_cars, space_down)

                space_up = (blocker.row + blocker.size) - row
                path_up = [(blocker.row - i, blocker.col) for i in range(1, space_up + 1)]
                cost_up, moved_cars_up = calculate_minimum_unique_cars(path_up, blocker, new_visited, cell_of_cars, space_up)

                if cost_down < cost_up:
                    result.update(moved_cars_down)
                else:
                    result.update(moved_cars_up)
            
            result.add(blocker.id)

    return (len(result), result)

def evaluate_heuristic(cars: list[Car]) -> int: 
    """
    Recursively counts the minimum number of unique cars need to move out of the goal car to clear the way to exit gate 
    """
    for car in cars:
        if car.id == 'G':
            goal_car = car 
            break 

    if goal_car is None:
        raise ValueError("Goal car not found in the node.")
    
    cell_of_cars = {}

    for car in cars:
        cells = car.get_cells_of_car()
        for cell in cells:
            cell_of_cars[cell] = car

    blocker = goal_car
    visited = set()

    space_exit = 8 - (goal_car.col + goal_car.size) # way to exit gate
    path_exit = []
    for i in range(1, space_exit + 1):
        for j in range(goal_car.size):
            path_exit.append((goal_car.row, goal_car.col + j + i))

    cost_exit, moved_exit = calculate_minimum_unique_cars(path_exit, blocker, visited, cell_of_cars, space_exit)

    if cost_exit == int(1e9):
        return int(1e9)
    
    for id in moved_exit:
        print(id)
        
    return cost_exit

