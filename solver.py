board = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 0],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 0, 0, 0, 0],
]
#6719


ideal = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}

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
            print("row problem")
            return False

        if board[rowcol][col] == value and rowcol != row:
            print("col problem")
            return False
    
    rowStart = (row // 3) * 3
    colStart = (col // 3) * 3

    for r in range(3):
        for c in range(3):
            if board[rowStart + r][colStart + c] == value:
                if rowStart + r != row and colStart + c != col:
                    print("box problem")
                    return False

    return True

def main():
    print(isSolved(board))
    print(isValid(6, 8, 8, board))

if __name__ == '__main__':
    main()