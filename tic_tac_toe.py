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
            'counter': 0,
            'players': {},
            "icons": ['X', 'O']

        }
    return {
        'board': init_board(n),
        'turn': 'X',
        'counter': 0,
        'players': game['players'],
        "icons": ['X', 'O']
    }


def get_player_icon(icons: list[str]) -> str:
    """
    according to the user selection, we return the player's symbol for the game
    :param icons: a list of possible icons
    :return: the value of the selected icon
    """
    if len(icons) > 1:
        is_select_icon = True if input("do you want to select symbol?(y/n)").lower() == 'y' else False
        if is_select_icon:
            while True:
                icon = input("select icon X/O:").upper()
                if not icon in icons:
                    print(f"invalid icon, the positions are: {'/'.join(icons)}")
                    continue
                break
        else:
            icon = choice(icons)

        icons.remove(icon)
    else:
        icon = icons.pop()
    return icon


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
        count = 1
        while count < 3:
            name = input(f"player #{count}, please enter your name:").capitalize()

            icon = get_player_icon(icons)
            print(f"you will play the {icon} symbol in this game")
            players[f'{icon}'] = name
            count += 1
    print(players)
    game['players'] = players


def init_board(n: int) -> list[list[str]]:
    """
    build and initiate the Tic - Tac - Toe board
    :param n: diameter for the game's size nxn
    :return: a nested list of string in size of nxn
    """
    board_result: list[list[str]] = []
    for row in range(1, n + 1):
        board_result.append(['_'] * n)
    return board_result


def draw_board(game:dict[str, any]) -> None:
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
        if game['board'][location_list[0]][location_list[1]] != '_':
            print("occupied,try again")
            continue
        break

    return location_list


def set_square(game: dict[str, any], location: list[int]) -> None:
    """
    :param game:dictionary of the played game
    :param location: a list of 2 integers
    update the board with the received list and the current symbol turn
    """
    game['board'][location[0]][location[1]] = game['turn']
    game['counter'] += 1


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
    return game['counter'] == len(game['board']) ** 2


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
    want_to_play = True;
    is_rematch = False
    my_game: dict[str, any] = {}

    while want_to_play or is_rematch:
        print("Let play Tic - Tac - Toe!!")
        my_game = init_game(3, my_game, is_rematch)
        get_players(my_game, is_rematch)
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
        want_to_play = True if input("do you want to play a new game?(y/n)").lower() == 'y' else False
        if want_to_play:
            is_rematch = False
            continue
        else:
            is_rematch = True if input("do you want a rematch?(y/n)").lower() == 'y' else False

    else:
        print("goodbye!")


if __name__ == "__main__":
    play_tic_tac_toe()
