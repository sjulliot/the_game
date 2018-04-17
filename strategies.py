import random as rd
from math import inf

from game_mechanisms import hand_all_actions, \
                            apply_action, \
                            undo_action


VERBOSE = False


def print_strategy_choice(hand, stacks, choice):
    if VERBOSE:
        print('My hand :', hand)
        print('The stack :', stacks)
        print('I choose :', choice)
        print()


def random_strategy(hand, stacks):
    possible_actions = hand_all_actions(hand, stacks)
    choice = rd.choice(possible_actions)
    print_strategy_choice(hand, stacks, choice)
    return choice


def height(stacks):
    return sum(abs(st['values'][0] - st['values'][-1]) for st in stacks)


def minimize_height_strategy(hand, stacks):
    possible_actions = hand_all_actions(hand, stacks)
    best_height, best_action = inf, []
    for action in possible_actions:
        apply_action(hand, action)
        if height(stacks) < best_height:
            best_height, best_action = height(stacks), action
        undo_action(hand, action)
    print_strategy_choice(hand, stacks, best_action)
    return best_action
