import matplotlib.pyplot as plt


# FILENAME = 'minimize_height_scores'
FILENAME = 'random_strategy_scores'


def avg(l):
    if not l:
        return 0
    return sum(l) / len(l)


with open(FILENAME) as f:
    scores = [int(v) for v in f.read().split(',')]

# print(scores)
print('len:', len(scores))
print('avg:', avg(scores))

plt.hist(scores, bins=(max(scores) - min(scores) + 1))
plt.title('random strategy scores')
plt.show()
