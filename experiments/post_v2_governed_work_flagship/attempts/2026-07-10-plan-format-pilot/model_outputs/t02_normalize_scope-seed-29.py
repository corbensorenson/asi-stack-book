def normalize_scope(paths):
    # Normalize paths by removing absolute paths and any path containing '..'
    normalized_paths = [path for path in paths if not path.startswith('http://') and not path.startswith('https://')]
    return sorted(normalized_paths)
