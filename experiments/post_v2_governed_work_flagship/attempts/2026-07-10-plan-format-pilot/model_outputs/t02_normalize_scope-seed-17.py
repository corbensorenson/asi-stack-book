def normalize_scope(paths):
    # Normalize paths by removing absolute paths and paths containing '..'
    normalized_paths = [path for path in paths if not path.startswith('/') and not path.startswith('..')]
    return sorted(normalized_paths)
