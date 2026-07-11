def consume_nonce(nonce, used):
    """
    Consumes a nonce and updates the set of used nonces.

    Parameters:
    nonce (str): The nonce to be consumed.
    used (set): A set of nonces that have been used.

    Returns:
    tuple: A tuple containing a boolean indicating whether the nonce was accepted and the updated set of used nonces.
    """
    # Check if the nonce is already in the set
    if nonce in used:
        return (False, used)
    
    # Add the nonce to the set of used nonces
