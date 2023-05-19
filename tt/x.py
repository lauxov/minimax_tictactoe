import tkinter as tk
import winsound
import tkinter.messagebox as messagebox

PLAYER_X = "X"
PLAYER_O = "O"
EMPTY = ""

class TicTacToe:
    def __init__(self):
        self.current_player = PLAYER_X
        self.board = [[EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY]]
        self.root = tk.Tk()
        self.buttons = [[None, None, None],
                        [None, None, None],
                        [None, None, None]]
        self.new_game_button = None
        self.create_ui()

    def create_ui(self):
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg="black")

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text="", font=("Arial", 50, "bold"), width=4, height=2,
                                              command=lambda row=i, col=j: self.button_click(row, col),
                                              relief=tk.RAISED, bd=4, bg="black", fg="white")
                self.buttons[i][j].grid(row=i, column=j)

        self.new_game_button = tk.Button(self.root, text="New Game", font=("Arial", 14), width=10, command=self.new_game,
                                         relief=tk.RAISED, bd=4, bg="black", fg="white")
        self.new_game_button.grid(row=3, column=1, pady=10)

        self.restart_button = tk.Button(self.root, text="Restart Game", font=("Arial", 14), width=12, command=self.restart_game,
                                         relief=tk.RAISED, bd=4, bg="black", fg="white")
        self.restart_button.grid(row=3, column=2, pady=10)

    def button_click(self, row, col):
        if self.board[row][col] == EMPTY:
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, state=tk.DISABLED)

            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.disable_buttons()
                self.play_sound("winsound.wav")
            elif self.check_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.disable_buttons()
            else:
                self.switch_player()
                self.play_sound("sounds/click.wav")

            if self.current_player == PLAYER_O:
                self.make_bot_move()

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != EMPTY:
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != EMPTY:
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != EMPTY:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != EMPTY:
            return True
        return False

    def check_draw(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    return False
        return True

    def switch_player(self):
        if self.current_player == PLAYER_X:
            self.current_player = PLAYER_O
        else:
            self.current_player = PLAYER_X

    def disable_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state=tk.DISABLED)

    def enable_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state=tk.NORMAL)

    def clear_board(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j] = EMPTY
                self.buttons[i][j].config(text="")

    def new_game(self):
        self.enable_buttons()
        self.clear_board()

    def restart_game(self):
        self.new_game()
        self.current_player = PLAYER_X

    def make_bot_move(self):
        best_score = float("-inf")
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    self.board[i][j] = PLAYER_O
                    score = self.minimax(self.board, 0, False, float("-inf"), float("inf"))
                    self.board[i][j] = EMPTY

                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            row, col = best_move
            self.board[row][col] = PLAYER_O
            self.buttons[row][col].config(text=PLAYER_O, state=tk.DISABLED)

            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {PLAYER_O} wins!")
                self.disable_buttons()
                self.play_sound("winsound.wav")
            elif self.check_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.disable_buttons()
            else:
                self.switch_player()
                self.play_sound("sounds/click.wav")

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        if self.check_winner():
            if is_maximizing:
                return -1
            else:
                return 1
        elif self.check_draw():
            return 0

        if is_maximizing:
            best_score = float("-inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == EMPTY:
                        board[i][j] = PLAYER_O
                        score = self.minimax(board, depth + 1, False, alpha, beta)
                        board[i][j] = EMPTY
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if alpha >= beta:
                            break
            return best_score
        else:
            best_score = float("inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == EMPTY:
                        board[i][j] = PLAYER_X
                        score = self.minimax(board, depth + 1, True, alpha, beta)
                        board[i][j] = EMPTY
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break 
            return best_score

    def play_sound(self, sound_file):
        winsound.PlaySound(sound_file, winsound.SND_ASYNC)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
