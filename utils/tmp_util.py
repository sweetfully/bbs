import random


def get_random_by_len(length):
    result = []
    if type(length) == int:
        for i in range(length):
            result.append(str(random.randint(0, 9)))
        return "".join(result)
    return None
