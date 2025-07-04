from model.car import Car

impossible = int(1e9)

def find_cars_to_move(path_to_clear: list[tuple[int, int]], visited: set[str], 
                            cell_of_cars: dict[tuple[int, int], Car]) -> set[str]:
    """
    Calculates the min cars need to move to clear a path of cells
    """
    # Find all cars directly block on the path
    blockers_on_path = set()
    for cell in path_to_clear:
        blocker = cell_of_cars[cell]

        if blocker.id in visited:
            return {impossible}

        blockers_on_path.add(blocker)

    # No cars to move
    if not blockers_on_path:
        return set()
    
    total_cars = {car.id for car in blockers_on_path}
    new_visited = visited.union(total_cars)
    result = {} # 1 car = 1 cost

    for blocker in blockers_on_path:
        if blocker.dir == 'h':
            path_left = [(blocker.row, blocker.col - 1)]
            move_cars_left = find_cars_to_move(path_left, new_visited, cell_of_cars)

            path_right = [(blocker.row, blocker.col + blocker.size)]
            move_cars_right = find_cars_to_move(path_right, new_visited, cell_of_cars)

            if impossible in move_cars_left and impossible in move_cars_right:
                return {impossible}
            elif impossible in move_cars_left:
                better_path = move_cars_right
            elif impossible in move_cars_right:
                better_path = move_cars_left
            elif len(move_cars_left) < len(move_cars_right):
                better_path = move_cars_left
            else:
                better_path = move_cars_right  
            
        else:
            path_up = [(blocker.row - 1, blocker.col)]
            move_cars_up = find_cars_to_move(path_up, new_visited, cell_of_cars)

            path_down = [(blocker.row + blocker.size, blocker.col)]
            move_cars_down = find_cars_to_move(path_down, new_visited, cell_of_cars)

            if impossible in move_cars_up and impossible in move_cars_down:
                return {impossible}
            elif impossible in move_cars_up:
                better_path = move_cars_down
            elif impossible in move_cars_down:
                better_path = move_cars_up
            elif len(move_cars_down) < len(move_cars_up):
                better_path = move_cars_down
            else:
                better_path = move_cars_up

        if impossible in better_path:
            return {impossible}

        result.update(better_path)

    return result  

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

    visited = {goal_car.id}

    space_exit = 8 - (goal_car.col + goal_car.size) # way to exit gate
    path_exit = []
    for i in range(1, space_exit + 1):
        path_exit.append((goal_car.row, goal_car.col + 1))

    moved_exit = find_cars_to_move(path_exit, visited, cell_of_cars)

    if impossible in moved_exit:
        return impossible
    
    for id in moved_exit:
        print(id)
        
    return len(moved_exit)

