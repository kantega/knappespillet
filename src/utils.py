def clamp(min_value, value, max_value):
    return max(min_value, min(value, max_value))


def rotate(list_: list, n: int) -> list:
    return list_[n:] + list_[:n]
