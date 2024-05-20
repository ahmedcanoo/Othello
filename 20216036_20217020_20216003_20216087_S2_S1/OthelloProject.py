class Othello:
    def __init__(self):
        self.board = []  # Initialize an empty list to represent the game board
        for i in range(8):  # Create an 8x8 board
            row = []  # Initialize an empty row
            for j in range(8):  # Add 8 columns to each row
                row.append(None)  # Each cell starts as None (empty)
            self.board.append(row)  # Add the row to the board
        self.initialize_game()  # Set up the initial positions of the disks
        self.current_player = 'B'  # Set the starting player to 'B' (Black)
        self.BlackCount=32
        self.WhiteCount=32

    def initialize_game(self):
        # Place initial disks on the board
        self.board[3][3], self.board[4][4] = 'W', 'W'  # White disks
        self.board[3][4], self.board[4][3] = 'B', 'B'  # Black disks

    def print_board(self):
        possible_moves = self.get_possible_moves(self.current_player)  # Get possible moves for the current player
        valid_moves_set = set(possible_moves)  # Convert possible moves to a set for quick lookup
        print("  ", end="")  # Print column indices header
        for i in range(8):  # Print column indices from 0 to 7
            print(i, end=" ")
        print()  # New line after column indices 
        for i in range(8):  # Print each row of the board
            row = self.board[i]  # Get the current row
            row_display = []  # List to hold the display characters for the row
            for j in range(8):  # For each cell in the row
                cell = row[j]  # Get the cell value
                if cell is None:  # If the cell is empty
                    if (i, j) in valid_moves_set:  # If it's a valid move
                        row_display.append('*')  # Mark it with '*'
                    else:
                        row_display.append('.')  # Otherwise, mark it with '.'
                else:
                    row_display.append(cell)  # Add the player disk ('B' or 'W')
            print(i, ' '.join(row_display))  # Print the row index and the row contents

    def make_move(self, row, col, player):
        if self.is_valid_move(row, col, player):  # Check if the move is valid
            self.board[row][col] = player  # Place the player's disk
            self.outflank(row, col, player)  # Flip the opponent's disks
            self.BlackCount=self.BlackCount-1
            if (self.current_player == 'B'): # Switch the player
                self.current_player = 'W'
            else:
                self.current_player = 'B'    
            return True  # Return True indicating a successful move
        return False  # Return False if the move is invalid

    def is_valid_move(self, row, col, player):
        if self.board[row][col] is not None:  # Check if the cell is already occupied
            return False  # Invalid move if occupied
        if (player == 'B'): # Determine the opponent's disk
            opponent = 'W'
        else:
            opponent = 'B'    
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Possible directions: up, down, left, right
        for delta_row, delta_col in directions:  # Check each direction
            r, c = row + delta_row, col + delta_col  # Move to the adjacent cell
            if not (0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent):  # If it's not the opponent's disk
                continue  # Skip to the next direction
            while 0 <= r < 8 and 0 <= c < 8:  # Traverse in the current direction
                if self.board[r][c] is None:  # If an empty cell is found
                    break  # Not a valid move in this direction
                if self.board[r][c] == player:  # If a player's disk is found
                    return True  # It's a valid move
                r += delta_row  # Move to the next cell in the direction
                c += delta_col
        return False  # Return False if no valid move is found in any direction

    def outflank(self, row, col, player):
        if (player == 'B'): # Determine the opponent's disk
            opponent = 'W'
        else:
            opponent = 'B'   
             
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Possible directions: up, down, left, right
        for delta_row, delta_col in directions:  # For each direction
            disks_to_flip = []  # List to keep track of disks to flip
            r, c = row + delta_row, col + delta_col  # Move to the adjacent cell
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent:  # While there are opponent's disks
                disks_to_flip.append((r, c))  # Add the disk to the list
                r += delta_row  # Move to the next cell in the direction
                c += delta_col
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == player:  # If a player's disk is found
                for r, c in disks_to_flip:  # Flip all the opponent's disks
                    self.board[r][c] = player

    def get_possible_moves(self, player):
        possible_moves = []  # List to hold possible moves
        for r in range(8):  # Check each row
            for c in range(8):  # Check each column
                if self.is_valid_move(r, c, player):  # If it's a valid move
                    possible_moves.append((r, c))  # Add the move to the list
        return possible_moves  # Return the list of possible moves

    def game_over(self):
        if(self.current_player == 'B'):
            opponent = 'W'
        else:
            opponent = 'B'    
        return not (self.get_possible_moves(self.current_player) or self.get_possible_moves(opponent)) or not self.has_pieces_left  # Game over if no moves are possible or if a player runs out of pieces

    def has_pieces_left(self):
        return self.BlackCount > 0 and self.WhiteCount > 0  # Return True if both players have remaining pieces



    def utility(self):
        player_disks = 0  # Initialize counter for current player's disks
        opponent_disks = 0  # Initialize counter for opponent's disks
        for row in self.board:  # For each row
            for disk in row:  # For each cell
                if disk == self.current_player:  # If it's the current player's disk
                    player_disks += 1  # Increment the counter
                elif disk is not None:  # If it's an opponent's disk
                    opponent_disks += 1  # Increment the counter
        return player_disks - opponent_disks  # Return the difference between player's and opponent's disks

    
    def minimax(self, depth, alpha, beta, maximizing_player):  # _____ Hena hagat el lecture _____
        
        if depth == 0 or self.game_over():  # If the depth limit is reached or the game is over
            return self.utility()  # Return the utility of the current board
        if maximizing_player:  # If it's the maximizing player's turn
            max_eval = float('-inf')  # Initialize max evaluation to negative infinity
            for move in self.get_possible_moves(self.current_player):  # For each possible move
                eval = self.minimax(depth - 1, alpha, beta, False)  # Recursively call minimax
                max_eval = max(max_eval, eval)  # Update max evaluation
                alpha = max(alpha, eval)  # Update alpha
                if beta <= alpha:  # Alpha-beta pruning
                    break
            return max_eval  # Return max evaluation
        else:  # If it's the minimizing player's turn
            min_eval = float('inf')  # Initialize min evaluation to infinity
            for move in self.get_possible_moves(self.current_player):  # For each possible move
                eval = self.minimax(depth - 1, alpha, beta, True)  # Recursively call minimax
                min_eval = min(min_eval, eval)  # Update min evaluation
                beta = min(beta, eval)  # Update beta
                if beta <= alpha:  # Alpha-beta pruning
                    break
            return min_eval  # Return min evaluation

    def play(self):
        difficulty = input("Select difficulty level (Easy, Medium, Hard): ").strip().lower()  # Prompt the player to select a difficulty level
        depth = {"easy": 1, "medium": 3, "hard": 5}.get(difficulty, 3)  # Set the depth of the minimax algorithm based on the difficulty level

        while not self.game_over():  # Continue the game until it's over
            possible_moves = self.get_possible_moves(self.current_player)  # Get possible moves for the current player
            if not possible_moves:  # If there are no possible moves
                print(f"No possible moves for {self.current_player}. Skipping turn.")  # Notify the player
                if (self.current_player == 'B'): # Switch the player
                    self.current_player = 'W'
                else:
                    self.current_player = 'B'    
                continue  # Skip to the next iteration

            if self.current_player == 'B':  # If it's the human player's turn
                print("Your move:")
                self.print_board()  # Print the current board
                valid_move_made = False  # Flag to track if a valid move is made
                while not valid_move_made:  # Loop until a valid move is made
                    row = int(input("Enter the row number to place your disk: "))
                    col = int(input("Enter the column number to place your disk: ")) # Get the move input from the player
                    valid_move_made = self.make_move(row, col, 'B')  # Attempt to make the move
                    if not valid_move_made:  # If the move is invalid
                        print("Invalid move, try again.")  # Notify the player
            else:  # If it's the computer's turn _____ Hena hagat el lecture _____
                self.print_board()  # Print the current board
                print("Computer's move:")
                best_move = None  # Variable to store the best move
                best_score = float('-inf')  # Initialize best score to negative infinity
                for move in possible_moves:  # For each possible move
                    current_state = [row[:] for row in self.board]  # Save the current board state
                    self.make_move(*move, 'W')  # Make the move
                    score = self.minimax(depth, float('-inf'), float('inf'), False)  # Get the minimax score
                    self.board = current_state  # Restore the original board state
                    if score > best_score:  # If the score is better than the best score
                        best_score = score  # Update the best score
                        best_move = move  # Update the best move
                if best_move:  # If a best move is found
                    self.make_move(*best_move, 'W')  # Make the best move
                    print(f"Computer placed on {best_move}.")  # Notify the player
                    self.WhiteCount=self.WhiteCount-1
                    self.current_player = 'B'  # Switch back to the human player
                else:  # If no valid moves are available
                    print("No valid moves for the computer. Skipping turn.")  # Notify the player
                    self.current_player = 'B'  # Switch back to the human player
                

        if self.game_over():  # If the game is over
            self.print_board()  # Print the current board
            black_score = sum(row.count('B') for row in self.board)  # Count black pieces
            white_score = sum(row.count('W') for row in self.board)  # Count white pieces
            if(black_score>white_score): # Determine the winner
                winner = 'Black'
            elif(white_score>black_score):
                winner = 'White'
            else:
                print("Draw");
            if(black_score>white_score or white_score>black_score):
                print(f"Game over. {winner} wins with a score of {black_score}-{white_score}")  # Print the result

if __name__ == '__main__':
    game = Othello()  # Create a new game instance
    game.play()  # Start the game