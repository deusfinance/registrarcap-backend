def get_api_key(keys: list, last_key=None):
    try:
        if not last_key:
            return keys[0]
        return keys[keys.index(last_key) + 1]
    except IndexError:
        return None
