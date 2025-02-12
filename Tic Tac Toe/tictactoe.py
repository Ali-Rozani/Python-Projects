import random
import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        master.title("Tic Tac Toe")
        master.geometry("300x400")

        # Game state
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        
        # Winning combinations
        self.winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]

        # Create buttons
        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    master, 
                    text=' ', 
                    font=('Arial', 20), 
                    width=5, 
                    height=2,
                    command=lambda row=i, col=j: self.on_click(row*3 + col)
                )
                button.grid(row=i, column=j, pady=5, padx=5)  # Corrected padding
                self.buttons.append(button)

        # Reset Button
        self.reset_button = tk.Button(
            master, 
            text='Reset Game', 
            font=('Arial', 12),
            command=self.reset_game
        )
        self.reset_button.grid(row=3, column=1, pady=10)

        # Score Label
        self.score_label = tk.Label(
            master, 
            text='Player X Turn', 
            font=('Arial', 12)
        )
        self.score_label.grid(row=4, column=1)

    def on_click(self, position):
        # Check if the position is empty
        if self.board[position] == ' ':
            # Player's move
            self.board[position] = self.current_player
            self.buttons[position].config(text=self.current_player, state=tk.DISABLED)
            
            # Check if player wins
            if self.check_winner(self.board, self.current_player):
                messagebox.showinfo("Game Over", f"{self.current_player} Wins!")
                self.disable_all_buttons()
                return

            # Check for draw
            if self.is_board_full():
                messagebox.showinfo("Game Over", "It's a Draw!")
                return

            # Switch to computer's turn
            self.current_player = 'O'
            self.score_label.config(text='Player O Turn')
            self.master.after(500, self.computer_move)

    def computer_move(self):
        # Strategic move selection
        move = self.get_best_move()
        
        # Make the move
        self.board[move] = 'O'
        self.buttons[move].config(text='O', state=tk.DISABLED)
        
        # Check if computer wins
        if self.check_winner(self.board, 'O'):
            messagebox.showinfo("Game Over", "Player O Wins!")
            self.disable_all_buttons()
            return

        # Check for draw
        if self.is_board_full():
            messagebox.showinfo("Game Over", "It's a Draw!")
            return

        # Switch back to player's turn
        self.current_player = 'X'
        self.score_label.config(text='Player X Turn')

    def get_best_move(self):
        # Try to win
        for move in self.available_moves():
            board_copy = self.board.copy()
            board_copy[move] = 'O'
            if self.check_winner(board_copy, 'O'):
                return move

        # Block player's winning move
        for move in self.available_moves():
            board_copy = self.board.copy()
            board_copy[move] = 'X'
            if self.check_winner(board_copy, 'X'):
                return move

        # Take center if available
        if 4 in self.available_moves():
            return 4

        # Take a random available move
        return random.choice(self.available_moves())

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def check_winner(self, board, player):
        for combo in self.winning_combinations:
            if all(board[i] == player for i in combo):
                return True
        return False

    def is_board_full(self):
        return ' ' not in self.board

    def disable_all_buttons(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)

    def reset_game(self):
        # Reset board
        self.board = [' ' for _ in range(10)]
        
        # Reset buttons
        for button in self.buttons:
            button.config(text=' ', state=tk.NORMAL)
        
        # Reset game state
        self.current_player = 'X'
        self.score_label.config(text='Player X Turn')

def main():
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()