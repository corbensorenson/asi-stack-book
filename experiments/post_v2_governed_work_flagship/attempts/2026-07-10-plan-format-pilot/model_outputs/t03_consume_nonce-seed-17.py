def consume_nonce(nonce, used):
    # Check if the nonce is already in the set
    if nonce not in used:
        # If not, add it to the set and return (accepted, new_used)
        used.add(nonce)
        return True, used
    else:
        # If the nonce is already in the set, return (rejected, used)
        return False, used
