boardString = [
    "790000260",
    "014700000",
    "000000000",
    "508400000",
    "000050038",
    "100089000",
    "040002093",
    "000090070",
    "000037005"
]

board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]


ideal = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}

def string_to_Board(s):
    for i in range(9):
        for j in range(9):
            board[i][j] = int(s[i][j])

def printBoard(board):
    for row in range(9):
        if row % 3 == 0 and row != 0:
            print("-----------")
        for col in range(9):
            if col % 3 == 0 and col != 0:
                print("|", end="")
            print(board[row][col], end="")
        print("")

def isSolved(board):

    if not isFull(board):
        print("not full")
        return False
    
    #check rows
    for row in range(9):
        tempRow = {}
        for col in range(9):
            if board[row][col] in tempRow:
                tempRow[board[row][col]] += 1
            else:
                tempRow[board[row][col]] = 1
        if tempRow != ideal:
            return False
    
    #check cols
    for col in range(9):
        tempCol = {}
        for row in range(9):
            if board[row][col] in tempCol:
                tempCol[board[row][col]] += 1
            else:
                tempCol[board[row][col]] = 1
        if tempCol != ideal:
            return False
    
    #check boxes
    for box in range(9):
        tempBox = {}
        rowStart = (box // 3) * 3
        colStart = (box % 3) * 3
        for row in range(3):
            for col in range(3):
                if board[rowStart + row][colStart + col] in tempBox:
                    tempBox[board[rowStart + row][colStart + col]] += 1
                else:
                    tempBox[board[rowStart + row][colStart + col]] = 1
        if tempBox != ideal:
            return False

    return True

def isFull(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return False
    return True

def isValid(value, row, col, board):
    for rowcol in range(9):
        
        if board[row][rowcol] == value and rowcol != col:
            return False

        if board[rowcol][col] == value and rowcol != row:
            return False
    
    rowStart = (row // 3) * 3
    colStart = (col // 3) * 3

    for r in range(3):
        for c in range(3):
            if board[rowStart + r][colStart + c] == value:
                if rowStart + r != row and colStart + c != col:
                    return False

    return True

def find_empty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return False

def solvable(board):
    # Check rows
    for row in range(9):
        tempRow = set()
        for col in range(9):
            if board[row][col] in tempRow:
                return False
            elif board[row][col] != 0:
                tempRow.add(board[row][col])

    # Check columns
    for col in range(9):
        tempCol = set()
        for row in range(9):
            if board[row][col] in tempCol:
                return False
            elif board[row][col] != 0:
                tempCol.add(board[row][col])

    # Check 3x3 boxes
    for box in range(9):
        tempBox = set()
        rowStart = (box // 3) * 3
        colStart = (box % 3) * 3
        for row in range(3):
            for col in range(3):
                value = board[rowStart + row][colStart + col]
                if value in tempBox:
                    return False
                elif value != 0:
                    tempBox.add(value)

    return True




def solve(board):
    if not solvable(board):
        return False
    first_empty = find_empty(board)
    if first_empty == False:
        yield board  # Return the solved board as the last step
        return
    row, col = first_empty
    for n in range(1, 10):
        if isValid(n, row, col, board):
            board[row][col] = n
            yield board  # Yield the current board state after placing a number
            if solve(board):
                return
            board[row][col] = 0
    return False
                        

def main():
    string_to_Board(boardString)
    print("solving")
    solve(board)
    printBoard(board)
    print(board)

if __name__ == '__main__':
    main()