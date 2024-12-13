import random


def init_game(n, game, is_rematch) -> dict[str, any]:
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


def get_player_icon(icons):
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
            icon = random.choice(icons)

        icons.remove(icon)
    else:
        icon = icons.pop()
    return icon


def get_players(game, is_rematch=False):
    players = game['players']
    if not is_rematch:
        players = {}
        icons = game['icons'].copy()
        count = 1
        while count < 3:
            name = input(f"player #{count}, please enter your name:").capitalize()

            icon=get_player_icon(icons)
            print(f"you will play the {icon} symbol in this game")
            players[f'{icon}'] = name
            count += 1
    print(players)
    game['players'] = players


def init_board(n: int):
    board_result: list[list[str]] = []
    for row in range(1, n + 1):
        board_result.append(['_'] * n)
    return board_result


def draw_board(game) -> None:
    print(' ', end=' ')
    for i in range(1, len(game['board']) + 1):
        print(i, end=" ")
    print()
    for index, row in enumerate(game['board']):
        print(index + 1, ' '.join(row))


def input_square(game):
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


def set_square(game, location):
    game['board'][location[0]][location[1]] = game['turn']
    game['counter'] += 1


def check_win(game):
    return check_win_rows(game) or check_win_columns(game) or check_win_diagonals(game)


def check_win_rows(game):
    board = game['board']
    player = game['turn']
    is_win = False
    for row in board:
        if all(cell == player for cell in row):
            is_win = True
    return is_win


def check_win_columns(game):
    board = game['board']
    player = game['turn']

    for col_index in range(len(board)):
        if all([board[index][col_index] == player for index in range(len(board))]):
            return True

    return False


def check_win_diagonals(game):
    board = game['board']
    player = game['turn']

    d1 = all([board[i][len(board) - 1 - i] == player for i in range(len(board))])
    d2 = all([board[i][i] == player for i in range(len(board))])
    return d1 or d2


def check_tie(game):
    return game['counter'] == len(game['board']) ** 2


def switch_player(game):
    game['turn'] = 'O' if game['turn'] == 'X' else 'X'


def play_tic_tac_toe():
    want2play = True;
    is_rematch = False
    my_game: dict[str, any] = {}

    while want2play or is_rematch:
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
        want2play = True if input("do you want to play a new game?(y/n)").lower() == 'y' else False
        if want2play:
            is_rematch = False
            continue
        else:
            is_rematch = True if input("do you want a rematch?(y/n)").lower() == 'y' else False

    else:
        print("goodbye!")


if __name__ == "__main__":
    play_tic_tac_toe()
