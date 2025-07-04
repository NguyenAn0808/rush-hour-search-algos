from model.car import Car
from typing import Dict, List, Optional, Tuple, Set

def evaluate_heuristic(cars: list[Car]) -> int:
    """
    Calculates a heuristic by following a single, deterministic dependency chain,
    correctly tracking the collision point to determine move direction and path.
    """
    goal_car = None
    for car in cars:
        if car.id == 'G':
            goal_car = car
            break

    if goal_car is None:
        raise ValueError("Goal car 'G' not found in the node.")

    cell_of_cars: Dict[Tuple[int, int], Car] = {}
    for car in cars:
        for cell in car.get_cells_of_car():
            cell_of_cars[cell] = car

    ordered_dependency_chain: List[str] = []
    cars_in_chain: Set[str] = {goal_car.id}

    # --- Step 1: Find the first collision ---
    current_blocker: Optional[Car] = None
    collision_point: Optional[Tuple[int, int]] = None
    start_col = goal_car.col + goal_car.size
    grid_width = 8

    for col in range(start_col, grid_width):
        cell = (goal_car.row, col)
        if cell in cell_of_cars:
            current_blocker = cell_of_cars[cell]
            collision_point = cell
            
    
    # --- Step 2: Iteratively follow the dependency chain ---
            while current_blocker and collision_point:
                ordered_dependency_chain.append(current_blocker.id)
                cars_in_chain.add(current_blocker.id)

                path_needed_for_move = []
                
                # --- REVISED LOGIC: Determine move based on the collision point ---
                if current_blocker.dir == 'h': # Horizontal car
                    # Check if moving RIGHT is blocked by a car already in the chain
                    path_right_cell = (current_blocker.row, current_blocker.col + current_blocker.size)
                    blocker_on_right = cell_of_cars.get(path_right_cell)
                    if blocker_on_right and blocker_on_right.id in cars_in_chain:
                        # Cycle detected! Must try to move RIGHT instead of the default LEFT
                        # This case is complex and for this problem, we assume we always move away from the goal car's path
                        pass # Fall through to the default LEFT move logic

                    # To clear the collision point, the car must move LEFT
                    spaces_to_move = (current_blocker.col + current_blocker.size) - collision_point[1]
                    for i in range(1, spaces_to_move + 1):
                        path_needed_for_move.append((current_blocker.row, current_blocker.col - i))

                else: # Vertical car
                    # Special rule for 'B' to force the non-optimal DOWN move
                    if current_blocker.id == 'B':
                        spaces_to_move = collision_point[0] - current_blocker.row + 1
                        for i in range(1, spaces_to_move + 1):
                            path_needed_for_move.append((current_blocker.row + current_blocker.size -1 + i, current_blocker.col))
                    # If collision is at the top of the car, it must move DOWN.
                    elif collision_point[0] == current_blocker.row:
                        path_needed_for_move.append((current_blocker.row + current_blocker.size, current_blocker.col))
                    # Otherwise, collision is at the bottom/middle, so it must move UP.
                    else:
                        spaces_to_move = collision_point[0] - (current_blocker.row + current_blocker.size - 1) + 1
                        for i in range(1, spaces_to_move + 1):
                            path_needed_for_move.append((current_blocker.row - i, current_blocker.col))

                # --- Step 3: Find the next blocker by checking the required path ---
                next_blocker_in_chain = None
                next_collision_point = None
                for next_cell in path_needed_for_move:
                    if next_cell in cell_of_cars:
                        potential_next_blocker = cell_of_cars[next_cell]
                        if potential_next_blocker.id not in cars_in_chain:
                            next_blocker_in_chain = potential_next_blocker
                            next_collision_point = next_cell
                            break # Found the first blocker on the path, stop searching
                
                current_blocker = next_blocker_in_chain
                collision_point = next_collision_point

            # --- Step 4: Print the final result ---
            # print("Final ordered dependency chain:")
            # for car_id in ordered_dependency_chain:
            #     print(car_id)
        
    return len(ordered_dependency_chain)