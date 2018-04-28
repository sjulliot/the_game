import doctest

from utils import avg

from game_mechanisms import init_min_cards_by_turn, \
                            create_stacks, \
                            init_hands_and_deck, \
                            finished, \
                            apply_strat, \
                            draw, \
                            rotate_hands, \
                            score

from strategies import random_strategy, \
                       minimize_height_strategy


AVERAGE_STRATEGY_ITERATIONS = 5 * (10 ** 1)
MP_CORES_TO_USE = 4


def test_strategy(strat):
    '''
    Play a game with every player using the given strategy,
    return the score.


    >>> from strategies import random_strategy
    >>> 0 <= test_strategy(random_strategy) <= 96
    True
    '''
    init_min_cards_by_turn()
    stacks = create_stacks()
    hands, deck = init_hands_and_deck()
    old_score = score(hands, deck)
    while not finished(hands, stacks):
        apply_strat(strat, hands[0], stacks)
        draw(hands, deck)
        rotate_hands(hands)
        tmp_score = score(hands, deck)
        assert old_score > tmp_score
        old_score = tmp_score
    return score(hands, deck)


def show_results(strat_name, scores, show_hist=True):
    print('Testing', strat_name)
    print('scores:', scores)
    print('avg:', avg(scores))
    print()

    if show_hist:
        import matplotlib.pyplot as plt
        plt.hist(scores)
        plt.title(strat_name, 'scores')
        plt.show()


def mp_test(strat, iterations=AVERAGE_STRATEGY_ITERATIONS):
    '''
    Call test_strategy on strat multiple times using the multiprocessing module.
    '''
    from multiprocessing import Pool
    with Pool(MP_CORES_TO_USE) as p:
        return p.map(test_strategy, [strat for _ in range(iterations)])


def multi_test(strat_name,
               strat,
               iterations=AVERAGE_STRATEGY_ITERATIONS,
               use_mp=True,
               show_hist=True):
    '''
    Call test_strategy on strat multiple times (`iterations`),
    then print the scores and their average.

    If use_mp is True, the multiprocessing module is used to divide the work.

    If show_hist is True, matplotlib.pyplot is imported to show a histogram
    of the scores.
    '''
    if use_mp:
        scores = mp_test(strat)
    else:
        scores = [test_strategy(strat) for _ in range(iterations)]
    show_results(strat_name, scores, show_hist)


if __name__ == '__main__':
    doctest.testmod()

    multi_test('random strategy',
               random_strategy,
               use_mp=False,
               show_hist=False)
    multi_test('minimizing height strategy',
               minimize_height_strategy,
               use_mp=False,
               show_hist=False)
