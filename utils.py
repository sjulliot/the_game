import random as rd


def pick_random(l):
    value = rd.choice(l)
    l.remove(value)
    return value


def avg(l):
    if not l:
        return 0
    return sum(l) / len(l)
