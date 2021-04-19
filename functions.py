def is_int(s: str):
    try:
        int(s)
        return True
    except ValueError:
        return False
