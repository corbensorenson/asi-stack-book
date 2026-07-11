def choose_route(routes):
    # Sort routes by numeric cost in ascending order
    sorted_routes = sorted(routes, key=lambda x: x.numeric_cost)
    
    # Initialize variables to track the lowest-cost route
    lowest_cost_route = None
    lowest_cost_value = float('inf')
    
    # Iterate through the sorted routes
