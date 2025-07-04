from model.car import Car

def evaluate_blocking_heuristic(cars: list[Car]) -> int:
    for car in cars:
        if car.id == 'G':
            goal_car = car 
            
    if goal_car is None:
        raise ValueError("Goal car not found in the node.")
    
    blockers = 0
    for car in cars:
        
        # Check if the goal car is blocked the another car. It must be vertical. 
        if car.dir != 'v' or car.id == 'G':
            continue
        
        if car.row + car.size - 1 >= goal_car.row and car.col > goal_car.col + goal_car.size - 1:  
            blockers += 1
    
    return blockers 
    
