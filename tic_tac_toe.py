def init_game(n) -> dict[str, any]:
    return {
        'board': init_board(n),
        'turn': 'X',
        'counter': 1
    }


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
        location: str = input(f"enter row number,column number for {game['turn']} separated by ',':")
        location_list =  location.split(',')
        if len(location_list) < 2 or not all([x != '' for x in location_list]):
            print("try again,invalid input")
            continue
        location_list=[int(x)-1 for x in location_list]
        if not 0 <= location_list[0] <= len(game['board']) or not 0 <= location_list[1] <= len(game['board']):
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
    # board = game['board']
    # player = game['turn']
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

    return all([board[i][i] == player for i in range(len(board))])


def check_tie():
    pass


def switch_player(game):
    game['turn']='O' if game['turn']=='X' else'X'



def play_tic_tac_toe():
    my_game = init_game(3)
    print(my_game)
    draw_board(my_game)
    while True:

        location = input_square(my_game)
        set_square(my_game, location)
        draw_board(my_game)
        if check_win(my_game):
            print("the winner is:",my_game['turn'])
            break
        switch_player(my_game)


if __name__ == "__main__":
    play_tic_tac_toe()
