def restore_snapshot(original, changed):
    # Create a deep copy of the original dictionary
    return {k: v for k, v in original.items() if k not in changed}
