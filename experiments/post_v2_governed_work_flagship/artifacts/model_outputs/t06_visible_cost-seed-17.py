def total_visible_cost(items: List[dict]) -> int:
    """
    Calculate the total cost of items that are visible.

    Parameters:
    items (List[dict]): A list of dictionaries, where each dictionary represents an item with a 'cost' and a 'visible' key.

    Returns:
    int: The sum of the costs of items that are visible.
    """
    total_cost = 0
    for item in items:
        if item['visible']:
            total_cost += item['cost']
    return total_cost
