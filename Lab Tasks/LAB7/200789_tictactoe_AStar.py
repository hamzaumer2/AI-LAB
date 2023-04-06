from queue import PriorityQueue

class TicTacToe:
    def __init__(self):
        self.board = {i: ' ' for i in range(1, 10)}
        self.player = 'X'
        self.bot = 'O'
        self.winning_positions = [
            [1, 2, 3], [4, 5, 6], [7, 8, 9],
            [1, 4, 7], [2, 5, 8], [3, 6, 9],
            [1, 5, 9], [3, 5, 7]
        ]

    def print_board(self):
        print(f"{self.board[1]}|{self.board[2]}|{self.board[3]}")
        print("-|-|-")
        print(f"{self.board[4]}|{self.board[5]}|{self.board[6]}")
        print("-|-|-")
        print(f"{self.board[7]}|{self.board[8]}|{self.board[9]}")

    def get_moves(self, player):
        return [k for k, v in self.board.items() if v == ' ']

    def is_winner(self, player):
        player_positions = [k for k, v in self.board.items() if v == player]
        for positions in self.winning_positions:
            if all(p in player_positions for p in positions):
                return True
        return False

    def is_full(self):
        return ' ' not in self.board.values()

    def make_move(self, position, player):
        self.board[position] = player

    def undo_move(self, position):
        self.board[position] = ' '

        if self.is_winner(player):
            return 0
        elif self.is_winner(self.bot if player == self.player else self.player):
            return 2
        else:
            score = 0
            for positions in self.winning_positions:
                count_player = 0
                count_bot = 0
                for p in positions:
                    if self.board[p] == self.player:
                        count_player += 1
                    elif self.board[p] == self.bot:
                        count_bot += 1
                if count_player == 0 and count_bot > 0:
                    score += count_bot ** 2
                elif count_bot == 0 and count_player > 0:
                    score -= count_player ** 2
            return score

    def get_path_cost(self, current_state):
        return current_state.depth + self.heuristic(current_state.player)

    def get_successors(self, player):
        moves = self.get_moves(player)
        successors = []
        for move in moves:
            self.make_move(move, player)
            if self.is_winner(player):
                state = GameState(self.board.copy(), player, True, move)
                successors.append(state)
            elif self.is_full():
                state = GameState(self.board.copy(), player, True, move)
                successors.append(state)
            else:
                next_player = self.bot if player == self.player else self.player
                state = GameState(self.board.copy(), next_player, False, move)
                successors.append(state)
            self.undo_move(move)
        return successors

    def a_star_search(self):
        start_state = GameState(self.board.copy(), self.bot, False, None)
        pq = PriorityQueue()
        visited = set()
        pq.put((self.get_path_cost(start_state), start_state))
        while not pq.empty():
            current_cost, current_state = pq.get
    def a_star_search(self):
        start_state = GameState(self.board.copy(), self.bot, False, None)

        start_state.h = self.heuristic(start_state.player)

        pq = PriorityQueue()
        pq.put(start_state)

        while not pq.empty():
            current_state = pq.get()

            if self.is_winner(current_state.player):
                return current_state

            for move in self.get_moves(current_state.player):
                next_state = GameState(current_state.board.copy(),  self.bot if current_state.player == self.player else self.player, not current_state.is_maximizing_player, move)

                next_state.make_move(move, next_state.player)

                # Calculate the heuristic value for the next state
                next_state.h = self.heuristic(next_state.player)

                # Calculate the g value for the next state
                next_state.g = current_state.g + 1

                # Calculate the f value for the next state
                next_state.f = next_state.g + next_state.h

                # Add the next state to the priority queue
                pq.put(next_state)

        # No solution found
        return None

    def get_best_move(self):
        # Run the A* search algorithm
        goal_state = self.a_star_search()

        # Find the move that led to the goal state
        while goal_state.parent_state.parent_state is not None:
            goal_state = goal_state.parent_state

        return goal_state.last_move

    def play(self):
        print("Welcome to Tic Tac Toe!")
        first_player = input("Do you want to go first? (y/n) ").lower() == 'y'
        if not first_player:
            self.player, self.bot = self.bot, self.player

        while True:
            self.print_board()

            if self.is_winner(self.bot):
                print("Sorry, you lose!")
                break
            elif self.is_winner(self.player):
                print("Congratulations, you win!")
                break
            elif self.is_full():
                print("It's a tie!")
                break

            if first_player:
                position = int(input("Enter a position (1-9): "))
                while position not in self.get_moves(self.player):
                    position = int(input("Invalid move. Enter a position (1-9): "))
                self.make_move(position, self.player)
                first_player = False
            else:
                print("Bot is making a move...")
                position = self.get_best_move()
                self.make_move(position, self.bot)
                first_player = True

        self.print_board()

if __name__ == "__main__":
    game = TicTacToe()
    game.play()
