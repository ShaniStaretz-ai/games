def init_game(n) -> dict[str, any]:
    return {
        'board': init_board(n),
        'turn': 'X',
        'counter': 1
    }


def init_board(n: int):
    board_result: list[list[str]] = []
    for row in range(n):
        board_result.append(['_'] * n)
    return board_result


def draw_board(game) -> None:
    print(' ', end=' ')
    for i in range(len(game['board'])):
        print(i, end=" ")
    print()
    for index, row in enumerate(game['board']):
        print(index, ' '.join(row))


def input_square():
    pass


def set_square():
    pass


def check_win():
    pass


def check_tie():
    pass


def switch_player():
    pass


def play_tic_tac_toe():
    my_game = init_game(3)
    print(my_game)
    draw_board(my_game)


if __name__ == "__main__":
    play_tic_tac_toe()
