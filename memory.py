import random
import re
from random import choice
from typing import Any

RESTART_SENTINEL = 'R'
REMATCH_SENTINEL = 'M'


def init_game(game: dict[str, any], is_rematch: bool, cards_labels: tuple[str, str, str, str, str, str],
              rows_dimension: int) -> dict[
    str, any]:
    """
    Initialize the game: shuffle the cards, reset the board and the possible moves.
    if it's re-match, leave the players names from the previous game, but reset their scores,
    else reset the players dictionary too
    :param game:dict type: includes all game's properties (board,players and other game's information)
    :param is_rematch: boolean type - indicate if it's a new game or repeat game with the same players
    :param cards_labels: tuple contains 6 string, represent the display on the memory cards
    :param rows_dimension: int type: number of row in the board
    :return: dict type, a new game
    """
    cards: list[dict[str, any]] = init_cards(cards_labels)
    cols_dimension = int(len(cards) / rows_dimension)
    if not is_rematch:
        return {
            'board': init_board(cards, rows_dimension),
            'turn': '1',
            'rows_dimension': rows_dimension,
            'cols_dimension': cols_dimension,
            'players': {},
            'computer_mode': False,
            "moves": possible_moves(rows_dimension, cols_dimension)

        }
    else:
        return {
            'board': init_board(cards, rows_dimension),
            'turn': '1',
            'rows_dimension': rows_dimension,
            'cols_dimension': cols_dimension,
            'players': reset_players_score(game['players']),
            'computer_mode': game['computer_mode'],
            "moves": possible_moves(rows_dimension, cols_dimension)

        }


def reset_players_score(players:dict[str,dict[str,str|int]]):
    """
    reset for each player's score to zero
    :param players: dict type
    :return: the players dict after reset.
    """
    for key in players:
        players[key]['score'] = 0
    return players


def get_valid_boolean_response(message: str, options: list[str], true_option: str):
    """
    asks from the user the input message and expect that the answer will be 1 of the options.
    and compares with the true_options
    if the answer is not one of the options, you will be asked again, till it is.
    :param true_option: compared right answer
    :param message:message to display in the input
    :param options: list of options to answer from
    :return: True if the selection is 'y', else return False
    """
    while True:
        answer = input(message).lower()
        if not answer in options:
            print(f"invalid answer, the possibilities are: {'/'.join(options)}")
            continue
        break
    return answer == true_option


def get_valid_number_of_players()->int:
    """
    asks from the user a number bigger than 2
    and will repeat the question till you enter a valid number
    :return: int type - number of players
    """
    while True:
        try:
            num_of_players = int(input("how many players are you?"))
            if num_of_players < 2:
                raise ValueError
            return num_of_players
        except ValueError:
            print("you must enter a valid number of players")
            continue


def get_valid_player_name(message: str) -> str:
    """
    get from the player a valid name, must be A-Z or a-z letters, can't be 'computer'
    and will repeat the question till you enter a valid name
    :param message: display message to the player
    :return: str type, player's name
    """
    while True:
        name = input(message)
        is_match = re.match("^(?!computer$)[a-zA-Z]+$", name)
        if not is_match:
            print("invalid name,must contain letters only,try again")
            continue
        break
    return name.capitalize()


def get_players(game: dict[str, any], is_rematch=False) -> None:
    """
    if the game is NOT a re-match , asks if you want to play against the computer.
    if you don't want to play against the computer, you'll be asked how many players and must be at least 2 players
    after receiving the players names, the game will be reset with the players dict    :param game: type of the game
    :param game: dict type - represent the memory game will all its' properties
    :param is_rematch: a boolean flag, to indict a re-match game or a not one.
    """
    if not is_rematch:
        players = {}

        is_computer = get_valid_boolean_response("do you want to play against the computer (y/n)?", ['y', 'n'], 'y')

        if not is_computer:
            count = 1

            num_of_players = get_valid_number_of_players()
            while count <= num_of_players:
                name = get_valid_player_name(f"player #{count}, please enter your name:")

                print(f"you will play the {count} in turn")
                players[f'{count}'] = {
                    'name': name,
                    "score": 0
                }
                count += 1
        else:
            name = get_valid_player_name("please enter your name:")
            players['1'] = {"name": name, "score": 0}
            players['2'] = {"name": 'computer', "score": 0}
        game['players'] = players
        game['computer_mode'] = is_computer
        names = map(lambda player: player['name'], players.values())
        print("the players are: ", ' VS '.join(names))


def init_cards(card_labels: tuple = ('A', 'B', 'C', 'D', 'E', 'F')) -> list[dict[str, any]]:
    """
    creates and shuffle cards objects with the card's properties:
    display icon, is_flipped,is_matched,card id
    :param card_labels: tuple type,
    if not sent a required icons will Initialize with default tuple of 6 icons:('A', 'B', 'C', 'D', 'E', 'F')
    :return: a shuffled list of flipped cards
    """
    cards = []
    options_len = len(card_labels)
    for i, label in enumerate(card_labels * 2):
        # each card receive id= result of the card_index % length(card_labels), so you will have 2 of each icon
        card = {
            "id": i % options_len,
            "icon": label,
            "is_flipped": False,
            "is_matched": False
        }
        cards.append(card)
    random.shuffle(cards) #
    return cards


def possible_moves(rows_dimension: int, cols_dimension: int) -> set[tuple[int, int]]:
    """
    create and initiate the memory possible moves
    :param rows_dimension: diameter for the game's row number
    :param cols_dimension: diameter for the game's column number
    :return: a set of all possible moves by (row,col)
    """
    moves: set[tuple[int, int]] = set()
    for row in range(0, rows_dimension):
        for col in range(0, cols_dimension):
            moves.add((row, col))

    return moves


def draw_board(game: dict[str, any]) -> None:
    """
    display the memory board
    according to the game's cols_dimension and cols_dimension properties
    :param game: dictionary of the played game

    """
    print("---------------------------")
    print(' ', end=' ')
    for i in range(1, game['cols_dimension'] + 1):
        print(i, end=" ")
    print()
    board = game['board']

    col_count = 1
    for location, card in board.items():
        if location[1] == 0:
            print(col_count, end='')
            col_count += 1
        print(f" {'_' if not card['is_flipped'] and not card['is_matched'] else card['icon']}", end="")
        if location[1] == game['cols_dimension'] - 1:
            print()


def input_card_location(game: dict[str, any]) -> tuple[int, int] | str:
    """
    it's the computer's turn, the function will return a valid random location.
    else,get from the user cell location and validate its values:
    check the location limit within the game
    check if the cell is occupied
    if the user enter the letter M or m (indicate he wants a reset with same players)
    if the user enter the letter R or r, (indicate he wants a reset with NEW players)
    the function will return the letter as is.
    :param game: dictionary of the played game
    :return: tuple of 2 values, of the next played cell in the board
    """
    if game['computer_mode'] and game['turn'] == '2':
        print("The computer turn NOW")
        return get_random_location(game)
    while True:
        #display instructions to enter a value input of card location of reset game options
        print("enter row number,column number separated by ','")
        print(f"if you want to restart the game from scratch, press {RESTART_SENTINEL.lower()}/{RESTART_SENTINEL}")
        print(
            f"if you want to restart the game with the same players, press {REMATCH_SENTINEL.lower()}/{REMATCH_SENTINEL}")
        location: str = input(
            f"player #{game['turn']}, {game['players'][game['turn']]['name']}, your turn:")
        if location.upper() == RESTART_SENTINEL: # R value
            return RESTART_SENTINEL
        elif location.upper() == REMATCH_SENTINEL:# M value
            return REMATCH_SENTINEL
        location_list = location.split(',')
        # change if enter 2 parameters for row, column
        if len(location_list) < 2 or not all([x != '' for x in location_list]) or not all(
                [x.isdigit() for x in location_list]):
            print("try again,invalid input")
            continue
        #convert each value to int
        location_list = [int(x) - 1 for x in location_list]
        # check of the first parameter is within the row range and the second parameter is within the column range
        if not 0 <= location_list[0] < game['rows_dimension'] or not 0 <= location_list[1] < game['rows_dimension']:
            print("try again,out of range")
            continue
        # after checking valid values, get the card with this value and check if it's been flipped already
        card = game['board'][tuple(location_list)]
        if card['is_flipped']:
            print("already flipped,try again")
            continue
        break
    return tuple(location_list)


def get_random_location(game: dict[str, any]):
    """
    using random.choice function, select a random tuple of card's location(row,col) from a set of tuples
    :param game: dictionary of the played game
    :return: a random available location
    """
    return choice(list(game['moves']))


def flip_card(game: dict[str, any], location) -> None:
    """
    update the board with the received list and the current symbol turn
    :param game:dictionary of the played game
    :param location: a list of 2 integers
    """
    #convert the current card from flipped to un flipped and reverse according its current status
    game['board'][location]['is_flipped'] = not game['board'][location]['is_flipped']
    #if the card is flipped, it's location will be removed from the available moves
    if game['board'][location]['is_flipped']:
        game['moves'].discard(location)
    else:
        # if the card is un flipped, it will return to the available moves
        game['moves'].add(location)


def check_match(game, location1: tuple[int, int], location2: tuple[int, int]) -> bool:
    """
    compared 2 cards in the board, if their id is the same.
    :param location2: location of the 2end card on the board
    :param location1: location of the 1st card on the board
    :param game: dictionary of the  played game
    :return:True if there is a win, else return False
    """

    return game['board'][location1]['id'] == game['board'][location2]['id']


def check_end_of_game(game: dict[str, any]) -> bool:
    """
    check if there are not available moves left
    :param game:dictionary of the played game
    :return:True if there is a tie and the game is over, else return False
    """
    return len(game['moves']) == 0


def switch_player(game: dict[str, any]) -> None:
    """
    switch the current player and update the game
    if this player VS computer, will switch between them
    else will change to the next player inline or to the first player
    :param game:dictionary of the played game
    """
    if game['computer_mode']:
        game['turn'] = '1' if game['turn'] == '2' else '2'
    else:
        current_player = int(game['turn'])
        if int(current_player) < len(game['players'].keys()):
            game['turn'] = str(current_player + 1)
        else:
            game['turn'] = '1'


def get_winner(my_game:dict[str,any])->dict[str,str|int]:
    """
    find and return the player with the most score
    :param my_game: dictionary of the played game
    :return: dict type , with the player's information (name, score)
    """
    maxp = max(my_game['players'].values(), key=lambda player: player['score'])
    return maxp


def init_board(cards: list[dict[str, any]], rows_num:int) -> dict[tuple[int, int], dict[str, any]]:
    """
    build the board with given cards
    :param cards:  list of cards
    :param rows_num: int type, number of rows in the board
    :return: a dict of key=tuple(locations), value: dict type =card
    """
    cols_num = len(cards) // rows_num
    board = {}
    for row in range(rows_num):
        for col in range(cols_num):
            board[(row, col)] = cards.pop();

    return board


def set_match(my_game: dict[str, any], location1: tuple[int, int], location2: tuple[int, int]) -> None:
    """
    Update the game, after found match of 2 cards
    :param my_game: dict type, contains all game's properties
    :param location1:tuple type, includes 2 int, represent the card's location in the board
    :param location2:tuple type, includes 2 int, represent the card's location in the board
    :return:None
    """
    my_game['board'][location1]['is_matched'] = True
    my_game['board'][location2]['is_matched'] = True
    my_game['players'][my_game['turn']]['score'] += 1
    my_game['moves'].discard(location1)
    my_game['moves'].discard(location2)


def print_score_board(winner, my_game) -> None:
    """
    prints who are the winner and the full score board
    :param winner: dict type: includes the player's name and current score
    :param my_game:dict type: includes all game's properties (board,players and other game's information)

    """
    # filter all players that are not the winner
    other_scores = filter(lambda p: p['score'] != winner['score'], my_game['players'].values())
    print(f"the winner is: {winner['name']} with the score {winner['score']}:")
    print("SCORE BOARD:")
    print(f" name | score")
    print(f"{winner['name']} | {winner['score']}")
    for player in other_scores:
        print(f"{player['name']} | {player['score']}")


def play_memory_game() -> None:
    """
    Runs the main loop, creates the game handling create a new game or re-match,
    players' turns, guessing and score update

    """
    new_game = True;
    is_rematch = None
    my_game: dict[str, any] = {}

    while new_game or is_rematch:
        new_game = None
        print("Let play Memory game!!")

        # Initialize the game configurations
        card_labels = ('A', 'B', 'C', 'D', 'E', 'F')
        my_game = init_game(my_game, is_rematch, card_labels, len(card_labels))
        get_players(my_game, is_rematch)
        # start the game flow
        while True:
            draw_board(my_game)
            location1 = input_card_location(my_game)
            # handling case the user want to rematch the game
            if location1 == REMATCH_SENTINEL:# M value
                is_rematch = True
                break
            # handling case the user want to restart the game
            elif location1 == RESTART_SENTINEL: # R value
                new_game = True
                break
            # after receiving a valid first card location
            flip_card(my_game, location1)
            # display the board after flipping first card
            draw_board(my_game)
            location2 = input_card_location(my_game)
            # handling case the user want to rematch the game
            if location2 == REMATCH_SENTINEL:
                is_rematch = True
                break
            # handling case the user want to restart the game
            elif location2 == RESTART_SENTINEL:
                new_game = True
                break
            #after receiving a valid second card location
            flip_card(my_game, location2)
            # display board after flipped second card
            draw_board(my_game)
            if check_match(my_game, location1, location2):
                # the 2 cards are equal
                print("MATCH")
                set_match(my_game, location1, location2)
                if check_end_of_game(my_game):
                    winner = get_winner(my_game)
                    print_score_board(winner, my_game)
                    break;
            else: #2 cards are not equal
                print("NO MATCH")
                # flipping back first card
                flip_card(my_game, location1)
                # flipping back second card
                flip_card(my_game, location2)
                switch_player(my_game)
        #handling rematch use case, if the game over successfully
        if is_rematch is None and new_game is None:
            is_rematch = get_valid_boolean_response("do you want a rematch (y/n) ?", ['y', 'n'], 'y')
        if is_rematch:
            new_game = False
            continue
        else:
            #handling new game use case, if the game over successfully
            if new_game is None:
                new_game = get_valid_boolean_response("do you want to play a new game (y/n)?", ['y', 'n'], 'y')
    else:
        # handling neither rematch not new game use case, if the game over successfully
        print("goodbye!")


if __name__ == "__main__":
    play_memory_game()
