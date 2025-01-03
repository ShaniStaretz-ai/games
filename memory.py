import random
import re
from random import choice


def init_game(game, is_rematch: bool, cards_labels: tuple[str, str, str, str, str, str], rows_dimension: int) -> dict[
    str, any]:
    cards = init_cards(cards_labels)
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
def reset_players_score(players):
    print(players)
    for key in players:
        players[key]['score']=0
    return players


def get_valid_boolean_response(message: str, options: list[str], true_option: str):
    """

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


def get_valid_player_name(message: str) -> str:
    """
    get from the player a valid name, must be A-Z or a-z letters, can't be 'computer'
    :param message: display message to the player
    :return: 's name
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
    get the players' names and symbols and update players property in the game
    :param game:dictionary of the game
    :param is_rematch: a boolean flag, to indict a re-match game or a not one.
    """
    if not is_rematch:
        players = {}

        is_computer = get_valid_boolean_response("do you want to play against the computer (y/n)?", ['y', 'n'], 'y')

        if not is_computer:
            count = 1
            num_of_players = int(input("how many players are you?"))
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


def init_cards(card_labels=('A', 'B', 'C', 'D', 'E', 'F')) -> list[dict[str, any]]:
    cards = []
    options_len = len(card_labels)
    for i, label in enumerate(card_labels * 2):
        card = {
            "id": i % options_len,
            "icon": label,
            "is_flipped": False,
            "is_matched": False
        }
        cards.append(card)
    random.shuffle(cards)
    return cards


def possible_moves(rows_dimension: int, cols_dimension: int) -> set[tuple[int, int]]:
    """
    build and initiate the memory possible moves
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
    :param game: dictionary of the played game
    print the memory board
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


def input_card_location(game: dict[str, any]) -> tuple[int, int]:
    """
    get from the user cell location and validate its values:
    check the location limit within the game
    check if the cell is occupied
    :param game: dictionary of the played game
    :return: list of 2 values, of the next played cell in the game
    """
    if game['computer_mode'] and game['turn'] == '2':
        print("The computer turn NOW")
        return get_random_location(game)
    while True:
        location: str = input(
            f"player #{game['turn']}, {game['players'][game['turn']]['name']}, enter row number,column number for  separated by ',':")
        location_list = location.split(',')
        if len(location_list) < 2 or not all([x != '' for x in location_list]) or not all(
                [x.isdigit() for x in location_list]):
            print("try again,invalid input")
            continue
        location_list = [int(x) - 1 for x in location_list]
        if not 0 <= location_list[0] < game['rows_dimension'] or not 0 <= location_list[1] < game['rows_dimension']:
            print("try again,out of range")
            continue
        card = game['board'][tuple(location_list)]
        if card['is_flipped']:
            print("already flipped,try again")
            continue
        break
    return tuple(location_list)


def get_random_location(game: dict[str, any]):
    """
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
    game['board'][location]['is_flipped'] = not game['board'][location]['is_flipped']
    if game['board'][location]['is_flipped']:
        game['moves'].discard(location)
    else:
        game['moves'].add(location)


def check_match(game, location1: tuple[int, int], location2: tuple[int, int]) -> bool:
    """
    check the current board for win
    :param location2: location of the 2end card on the board
    :param location1: location of the 1st card on the board
    :param game: dictionary of the  played game
    :return:True if there is a win, else return False
    """

    return game['board'][location1]['id'] == game['board'][location2]['id']


def check_end_of_game(game: dict[str, any]) -> bool:
    """
    :param game:dictionary of the played game
    :return:True if there is a tie and the game is over, else return False
    """
    return len(game['moves']) == 0


def switch_player(game: dict[str, any]) -> None:
    """
    switch the current player and update the game
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


def get_winner(my_game):
    maxp = max(my_game['players'].values(), key=lambda player: player['score'])
    return maxp


def play_memory_game() -> None:
    """
    manage the tic-tac-toe game flow
    """
    new_game = True;
    is_rematch = False
    my_game: dict[str, any] = {}

    while new_game or is_rematch:
        print("Let play Memory game!!")
        card_labels = ('A', 'B')

        my_game = init_game(my_game, is_rematch, card_labels, 2)
        get_players(my_game, is_rematch)

        while True:
            draw_board(my_game)
            location1 = input_card_location(my_game)
            flip_card(my_game, location1)
            draw_board(my_game)
            location2 = input_card_location(my_game)
            flip_card(my_game, location2)
            draw_board(my_game)
            if check_match(my_game, location1, location2):
                print("MATCH")
                set_match(my_game, location1, location2)
                if check_end_of_game(my_game):
                    winner = get_winner(my_game)
                    print(f"the winner is: {winner['name']} with the score {winner['score']}")
                    break;
            else:
                print("NO MATCH")
                flip_card(my_game, location1)
                flip_card(my_game, location2)
                switch_player(my_game)
        is_rematch = get_valid_boolean_response("do you want a rematch (y/n) ?", ['y', 'n'], 'y')
        if is_rematch:
            new_game = False
            continue
        else:
            new_game = get_valid_boolean_response("do you want to play a new game (y/n)?", ['y', 'n'], 'y')

        # my_game = init_game(3, my_game, is_rematch)
    #     get_players(my_game, is_rematch)
    #     print(f"the {my_game['turn']} starts first move")
    #     draw_board(my_game)
    #     while True:
    #         location = input_card_location(my_game)
    #         flip_card(my_game, location)
    #         draw_board(my_game)
    #         if check_match(my_game):
    #             print(f"the winner is:{my_game['players'][my_game['turn']]}!")
    #             break
    #         if check_tie(my_game):
    #             print("game over")
    #             break
    #         switch_player(my_game)
    #     is_rematch = get_valid_boolean_response("do you want a rematch (y/n) ?", ['y', 'n'], 'y')
    #
    #     if is_rematch:
    #         new_game = False
    #         continue
    #     else:
    #         new_game = get_valid_boolean_response("do you want to play a new game (y/n)?", ['y', 'n'], 'y')
    else:
        print("goodbye!")


def init_board(cards, rows_num):
    cols_num = len(cards) // rows_num
    board = {}
    for row in range(rows_num):
        for col in range(cols_num):
            board[(row, col)] = cards.pop();

    return board


def set_match(my_game, location1, location2):
    my_game['board'][location1]['is_matched'] = True
    my_game['board'][location2]['is_matched'] = True
    my_game['players'][my_game['turn']]['score'] += 1
    my_game['moves'].discard(location1)
    my_game['moves'].discard(location2)


if __name__ == "__main__":
    play_memory_game()
