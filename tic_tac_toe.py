import re
from random import choice


def init_game(n: int, game: dict[str, any], is_rematch: bool) -> dict[str, any]:
    """
    initiate the Tic- Tac-toe game
    :param n: diameter for the game nxn
    :param game: dictionary of the previous played game
    :param is_rematch: a boolean flag, to indict a re-match game or a not one.
    :return:a dictionary of the new game
    """
    if not is_rematch:
        return {
            'board': init_board(n),
            'turn': 'X',
            'players': {},
            "icons": ['X', 'O'],
            "moves": possible_moves(n),
            "computer_mode": False

        }
    return {
        'board': init_board(n),
        'turn': 'X',
        'players': game['players'],
        "icons": ['X', 'O'],
        "moves": possible_moves(n),
        "computer_mode": True
    }


def get_player_icon(icons: list[str]) -> str:
    """
    according to the user selection, we return the player's symbol for the game
    :param icons: a list of possible icons
    :return: the value of the selected icon
    """
    if len(icons) > 1:
        is_select_icon = get_valid_boolean_response("do you want to select symbol?(y/n)", ['y', 'n'], 'y')
        if is_select_icon:
            while True:
                icon = input("select icon X/O:").upper()
                if not icon in icons:
                    print(f"invalid icon, the possibilities are: {'/'.join(icons)}")
                    continue
                break
        else:
            icon = choice(icons)

        icons.remove(icon)
    else:
        icon = icons.pop()
    return icon


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


def get_valid_players_name(message: str) -> str:
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
    players = game['players']
    if not is_rematch:
        players = {}
        icons = game['icons'].copy()
        is_computer = get_valid_boolean_response("do you want to play against the computer?(y/n)", ['y', 'n'], 'y')

        if not is_computer:
            count = 1
            while count < 3:
                name = get_valid_players_name(f"player #{count}, please enter your name:")
                icon = get_player_icon(icons)
                print(f"you will play the {icon} symbol in this game")
                players[f'{icon}'] = name
                count += 1
        else:
            name = get_valid_players_name("please enter your name:")
            icon = get_player_icon(icons)
            print(f"you will play the '{icon}' symbol in this game")
            players[f'{icon}'] = name
            icon = get_player_icon(icons)
            players[f'{icon}'] = 'computer'
        game['players'] = players
        game['computer_mode'] = is_computer


def init_board(n: int) -> list[list[str]]:
    """
    build and initiate the Tic - Tac - Toe board
    :param n: diameter for the game's size nxn
    :return: a nested list of string in size of nxn
    """
    return [['_'] * n for _ in range(1, n + 1)]


def possible_moves(n: int) -> set[tuple[int, int]]:
    """
    build and initiate the Tic - Tac - Toe possible moves
    :param n: diameter for the game's size nxn
    :return: a set of all possible moves by (row,col)
    """
    moves: set[tuple[int, int]] = set()
    for row in range(0, n):
        for col in range(0, n):
            moves.add((row, col))

    return moves


def draw_board(game: dict[str, any]) -> None:
    """
    :param game: dictionary of the played game
    print the Tic Tac toe board
    """
    print(' ', end=' ')
    for i in range(1, len(game['board']) + 1):
        print(i, end=" ")
    print()
    for index, row in enumerate(game['board']):
        print(index + 1, ' '.join(row))


def input_square(game: dict[str, any]) -> list[int]:
    """
    get from the user cell location and validate its values:
    check the location limit within the game
    check if the cell is occupied
    :param game: dictionary of the played game
    :return: list of 2 values, of the next played cell in the game
    """
    if game['computer_mode'] and game['players'][game['turn']] == 'computer':
        return get_random_location(game)
    while True:
        location: str = input(
            f"enter row number,column number for {game['players'][game['turn']]}({game['turn']}) separated by ',':")
        location_list = location.split(',')
        if len(location_list) < 2 or not all([x != '' for x in location_list]) or not all(
                [x.isdigit() for x in location_list]):
            print("try again,invalid input")
            continue
        location_list = [int(x) - 1 for x in location_list]
        if not 0 <= location_list[0] < len(game['board']) or not 0 <= location_list[1] < len(game['board']):
            print("try again,out of range")
            continue
        if game['board'][location_list[0]][location_list[1]] != '_':  # o(1)
            print("occupied,try again")
            continue
        break

    return location_list


def get_random_location(game: dict[str, any]):
    return choice(list(game['moves']))


def set_square(game: dict[str, any], location: list[int]) -> None:
    """
    update the board with the received list and the current symbol turn
    :param game:dictionary of the played game
    :param location: a list of 2 integers
    """
    game['board'][location[0]][location[1]] = game['turn']
    game['moves'].discard(tuple(location))


def check_win(game: dict[str, any]) -> bool:
    """
    check the current board for win
    :param game: dictionary of the  played game
    :return:True if there is a win, else return False
    """
    return check_win_rows(game) or check_win_columns(game) or check_win_diagonals(game)


def check_win_rows(game: dict[str, any]) -> bool:
    """
    :param game: dictionary of the played game
    :return:True if there is a win in one of the boards' rows, else return False
    """
    board = game['board']
    player = game['turn']
    is_win = False
    for row in board:
        if all(cell == player for cell in row):
            is_win = True
    return is_win


def check_win_columns(game: dict[str, any]) -> bool:
    """
       :param game: dictionary of the played game
       :return:True if there is a win in one of the boards' columns, else return False
    """
    board = game['board']
    player = game['turn']

    for col_index in range(len(board)):
        if all([board[index][col_index] == player for index in range(len(board))]):
            return True

    return False


def check_win_diagonals(game: dict[str, any]) -> bool:
    """
       :param game: dictionary of the played game
       :return:True if there is a win in one of the boards' diagonals, else return False
    """
    board = game['board']
    player = game['turn']

    d1 = all([board[i][len(board) - 1 - i] == player for i in range(len(board))])
    d2 = all([board[i][i] == player for i in range(len(board))])
    return d1 or d2


def check_tie(game: dict[str, any]) -> bool:
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
    game['turn'] = 'O' if game['turn'] == 'X' else 'X'


def play_tic_tac_toe() -> None:
    """
    manage the tic-tac-toe game flow
    """
    new_game = True;
    is_rematch = False
    my_game: dict[str, any] = {}

    while new_game or is_rematch:
        print("Let play Tic - Tac - Toe!!")
        my_game = init_game(3, my_game, is_rematch)
        get_players(my_game, is_rematch)
        print(f"the {my_game['turn']} starts first move")
        draw_board(my_game)
        while True:
            location = input_square(my_game)
            set_square(my_game, location)
            draw_board(my_game)
            if check_win(my_game):
                print(f"the winner is:{my_game['players'][my_game['turn']]}!")
                break
            if check_tie(my_game):
                print("game over")
                break
            switch_player(my_game)
        is_rematch = get_valid_boolean_response("do you want a rematch?(y/n)", ['y', 'n'], 'y')

        if is_rematch:
            new_game = False
            continue
        else:
            new_game = get_valid_boolean_response("do you want to play a new game?(y/n)", ['y', 'n'], 'y')
    else:
        print("goodbye!")


if __name__ == "__main__":
    play_tic_tac_toe()
