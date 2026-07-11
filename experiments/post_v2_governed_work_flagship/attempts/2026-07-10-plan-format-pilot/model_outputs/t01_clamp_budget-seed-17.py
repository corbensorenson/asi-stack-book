def clamp_budget(value, ceiling):
    """
    Clamp the given value to the inclusive integer range 0 through ceiling.
    
    Args:
    value (int): The value to be clamped.
    ceiling (int): The upper limit of the inclusive range.
    
    Returns:
    int: The clamped value.
    """
    return max(0, min(value, ceiling))
