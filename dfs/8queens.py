"""
Eight Queens Problem:
Place 8 queens on the board so that no queen attacks another.
Formulate the problem and use the depth-first search algorithm. 
The problem may receive the board from a database or with some queens already placed, 
as long as those queens are not attacking each other.
At the end, indicate how many nodes were created to find a board configuration with 
8 queens such that none attacks another, and display the attack-free board.

Boards to be tested:

Empty board;
Board with 1 queen of your choice;
Board with 2 queens of your choice;
Board with 3 queens of your choice.
"""
class EightQueens:
    def __init__(self, initial_queens=[]):
        self.initial_queens = initial_queens
        self.board = [-1] * 8
        self.node_counter = 0
        self.solution = None
        
        for row, col in self.initial_queens:
            if 0 <= col < 8:
                self.board[col] = row

    def is_safe(self, board, row, col):
        for c in range(col):
            if board[c] == row:
                return False
            if abs(board[c] - row) == abs(c - col):
                return False
        return True

    def solve(self):
        stack = []
        stack.append((list(self.board), 0))
        
        while stack:
            board, col = stack.pop()
            
            self.node_counter += 1

            if col >= 8:
                self.solution = board
                return self.solution

            if board[col] != -1:
                if self.is_safe(board, board[col], col):
                    stack.append((board, col + 1))
                continue

            for row in range(7, -1, -1):
                if self.is_safe(board, row, col):
                    new_board = list(board)
                    new_board[col] = row
                    
                    stack.append((new_board, col + 1))

        self.solution = None
        return self.solution

    def print_solution(self):
        if not self.solution:
            print("\nNo solution was found from this initial board.")
            return
            
        print("\nSolution found!")
        for row in range(8):
            line = ""
            for col in range(8):
                if self.solution[col] == row:
                    line += " Q "
                else:
                    line += " . "
            print(line)

    def run_test(self): 
        if self.initial_queens:
            print(f"Initial board with queens at (row, column): {self.initial_queens}")
        else:
            print("Starting with an empty board.")
        
        self.solve()
        self.print_solution()

        print(f"\nTotal nodes created/visited: {self.node_counter}")
        print("-" * 30 + "\n")


# --- Boards for testing ---

if __name__ == "__main__":
    
    # Empty Board
    teste1 = EightQueens()
    teste1.run_test()
    
    # 1 Queen
    teste2 = EightQueens(initial_queens=[(3, 0)])
    teste2.run_test()

    # 2 Queens
    teste3 = EightQueens(initial_queens=[(0, 0), (5, 1)])
    teste3.run_test()
    
    # 3 Queens
    teste4 = EightQueens(initial_queens=[(6, 0), (0, 3), (3, 7)])
    teste4.run_test()