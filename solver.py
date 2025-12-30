def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num:
            return False
    
    for x in range(9):
        if board[x][col] == num:
            return False
    
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    
    return True


def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None


def solve_sudoku(board):
    empty = find_empty_location(board)
    
    if not empty:
        return True
    
    row, col = empty
    
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            
            if solve_sudoku(board):
                return True
            
            board[row][col] = 0
    
    return False


def validate_board(board):
    if not isinstance(board, list):
        return False, "Board must be a list"
    
    if len(board) != 9:
        return False, "Board must have 9 rows"
    
    for i, row in enumerate(board):
        if not isinstance(row, list):
            return False, f"Row {i} must be a list"
        
        if len(row) != 9:
            return False, f"Row {i} must have 9 columns"
        
        for j, cell in enumerate(row):
            if not isinstance(cell, int):
                return False, f"Cell [{i}][{j}] must be an integer"
            
            if cell < 0 or cell > 9:
                return False, f"Cell [{i}][{j}] must be between 0 and 9"
    
    return True, None