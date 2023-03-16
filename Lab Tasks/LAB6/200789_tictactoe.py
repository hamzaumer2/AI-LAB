def print_board(board):
    print("-------------")
    for i in range(3):
        print("|", end=" ")
        for j in range(3):
            print(board[i][j], "|", end=" ")
        print()
        print("-------------")

def print_state_space(state_space):
    print("State Space:")
    for i, state in enumerate(state_space):
        print(f"Move {i + 1}: {state}")
    print()

def get_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == "-":
                moves.append((i, j))
    return moves

def get_move(player, board, state_space):
    moves = get_moves(board)
    for i, move in enumerate(moves):
        row, col = move
        new_board = [row[:] for row in board]
        new_board[row][col] = player
        state_space.append(str(new_board))

    print(f"Player {player}'s turn.")
    print_board(board)
    print_state_space(state_space)

    while True:
        row = int(input("Enter row (1-3): ")) - 1
        col = int(input("Enter column (1-3): ")) - 1
        if (row, col) in moves:
            board[row][col] = player
            state_space.append(str(board))
            break
        else:
            print("That spot is already taken. Please try again.")
    
    print_board(board)
    print_state_space(state_space)


def check_win(board):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != "-":
            return board[row][0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "-":
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] != "-":
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] != "-":
        return board[0][2]

    for i in range(3):
        for j in range(3):
            if board[i][j] == "-":
                return None
    return "Tie"

def play_game():
    board = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]
    state_space = [str(board)]
    print_board(board)
    print_state_space(state_space)

    player = "X"
    while True:
        get_move(player, board, state_space)
        winner = check_win(board)
        if winner:
            if winner == "Tie":
                print("It's a tie!")
            else:
                print(f"Player {winner} wins!")
            break
        player = "O" if player == "X" else "X"

play_game()
