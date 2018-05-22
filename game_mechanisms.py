import doctest

import random as rd

PLAYERS_NB = 4
CARDS_BY_HAND = 6

min_cards_by_turn = 2


def init_min_cards_by_turn():
    global min_cards_by_turn
    min_cards_by_turn = 2


def create_stacks():
    return [
        {'direction': 'up', 'values': [1]},
        {'direction': 'up', 'values': [1]},
        {'direction': 'down', 'values': [100]},
        {'direction': 'down', 'values': [100]},
    ]


def init_hands_and_deck():
    cards = list(range(2, 100))
    rd.shuffle(cards)
    hands = [[cards.pop(0) for card in range(CARDS_BY_HAND)]
             for hand in range(PLAYERS_NB)]
    return hands, cards


def apply_action(hand, action):
    for card, stack in action:
        hand.remove(card)
        stack['values'].append(card)


def undo_action(hand, action):
    for card, stack in action:
        hand.append(card)
        stack['values'].remove(card)


def can_place(card, stack):
    '''
    Test if the card can be placed on the stack.

    >>> can_place(37, {'direction': 'up', 'values': [1, 74]})
    False
    >>> can_place(87, {'direction': 'up', 'values': [1, 74]})
    True
    >>> can_place(64, {'direction': 'up', 'values': [1, 74]})
    True
    >>> can_place(37, {'direction': 'down', 'values': [1, 24]})
    False
    >>> can_place(22, {'direction': 'down', 'values': [1, 24]})
    True
    >>> can_place(34, {'direction': 'down', 'values': [1, 24]})
    True
    '''
    return (stack['direction'] == 'up' and card > stack['values'][-1]) \
        or (stack['direction'] == 'up' and card == stack['values'][-1] - 10) \
        or (stack['direction'] == 'down' and card < stack['values'][-1]) \
        or (stack['direction'] == 'down' and card == stack['values'][-1] + 10)


def hand_allowed_placements(hand, stacks):
    '''
    Given a hand content and a list of stacks,
    return all pairs (card, stack) where card can be placed on stack.
    '''
    res = []
    for card in hand:
        for stack in stacks:
            if can_place(card, stack):
                res.append((card, stack))
    return res


def hand_all_actions(hand, stacks, min_cards=min_cards_by_turn, max_rec_lvl=6):
    '''
    given a hand and the current state of the stacks, return
    the list of all possible actions.

    min_cards_by_turn is a global variable indicating how many
    cards at least one player has to play in order to complete
    his turn. In the original game, this value starts at 2, then
    lowers to 1 when all cards have been picked from the deck.

    min_cards is a local variable indicating how many cards
    at least should be placed in order to complete the turn.
    This value is decreased when the function calls recursively.
    '''
    if not hand or max_rec_lvl == 0:
        return []
    actions = []
    allowed_placements = hand_allowed_placements(hand, stacks)
    if min_cards <= 1 and allowed_placements:
        # when only zero or one card left to add, all actions are valid
        actions += [[placement] for placement in allowed_placements]
    for placement in allowed_placements:
        apply_action(hand, [placement])
        for action_end in hand_all_actions(hand, stacks, min_cards - 1, max_rec_lvl - 1):
            actions.append([placement] + action_end)
        undo_action(hand, [placement])
    return actions


def finished(hands, stacks):
    hand = hands[0]
    return ([] in hands) or not len(hand_all_actions(hand, stacks))


def apply_strat(strat, hand, stacks):
    '''
    apply_strat does not need deck nor more than one hand,
    and should not be given this information.
    '''
    chosen_action = strat(hand[:], stacks[:])
    apply_action(hand, chosen_action)
    return chosen_action


def draw(hands, deck):
    '''
    Draw as many cards in deck as needed to reach CARDS_BY_HAND card in hand.
    If the deck is empty, min_cards_by_turn is set to 1 as stated by the rules.
    >>> CARDS_BY_HAND = 6
    >>> hands = [[3, 4, 5]]
    >>> draw(hands, [37, 25, 1, 9, 44, 90])
    >>> hands
    [[3, 4, 5, 90, 44, 9]]
    '''
    global min_cards_by_turn
    hand = hands[0]
    while deck and len(hand) < CARDS_BY_HAND:
        hand.append(deck.pop(-1))
    if not deck:
        min_cards_by_turn = 1


def rotate_hands(hands):
    hand = hands.pop(0)
    hands.append(hand)


def score(hands, deck):
    return sum(len(hand) for hand in hands) + len(deck)


if __name__ == '__main__':
    doctest.testmod()
