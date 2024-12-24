import pygame as pg
import sys
import time

# Initialize Pygame
pg.init()
screensize = 1200, 800
screen = pg.display.set_mode(screensize)
pg.display.set_caption("Sudoku Solver")
font = pg.font.SysFont("Arial", 50)
button_font = pg.font.SysFont("Arial", 30)

button_width, button_height = 100, 50
spacing = 20  # Space between buttons

# Hardcoded positions for buttons
solve_button = pg.Rect(900, 500, button_width * 1.75, button_height)
clear_button = pg.Rect(900, 575, button_width * 1.75, button_height)  # Clear button

selected = None  # Keep track of the selected cell
cell_values = [[None] * 9 for _ in range(9)]  # Grid values

# Hardcoded positions for number buttons (1-9) arranged in a 3x3 grid
number_buttons = [
    pg.Rect(800, 250, button_width, button_height),  # 1
    pg.Rect(920, 250, button_width, button_height),  # 2
    pg.Rect(1040, 250, button_width, button_height), # 3
    pg.Rect(800, 310, button_width, button_height),  # 4
    pg.Rect(920, 310, button_width, button_height),  # 5
    pg.Rect(1040, 310, button_width, button_height), # 6
    pg.Rect(800, 370, button_width, button_height),  # 7
    pg.Rect(920, 370, button_width, button_height),  # 8
    pg.Rect(1040, 370, button_width, button_height), # 9
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
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Hardcoded position for the delete button
delete_button = pg.Rect(1040, 430, button_width, button_height)

def draw_sudoku_grid():
    grid_size = 630  # Size of the grid area
    box_size = grid_size // 9  # Each small box size should be 630 / 9 = 70px
    start_x, start_y = 100, 100  # Position of the top-left corner of the Sudoku board

    # Draw the outer thick box with softer color
    pg.draw.rect(screen, pg.Color("#dcdcdc"), (start_x - 5, start_y - 5, grid_size + 10, grid_size + 10), 5)

    # Draw the outer thick lines for 3x3 sections with a darker line
    for i in range(1, 3):
        # Vertical lines for 3x3 sections
        pg.draw.line(screen, pg.Color("#707070"), (start_x + i * box_size * 3, start_y), 
                     (start_x + i * box_size * 3, start_y + grid_size), 5)
        # Horizontal lines for 3x3 sections
        pg.draw.line(screen, pg.Color("#707070"), (start_x, start_y + i * box_size * 3), 
                     (start_x + grid_size, start_y + i * box_size * 3), 5)

    # Draw the inner thinner lines for the 1x1 grid with lighter color
    for i in range(1, 9):
        # Vertical lines
        if i % 3 != 0:  # Skip every third line (to avoid the thicker 3x3 lines)
            pg.draw.line(screen, pg.Color("#dcdcdc"), (start_x + i * box_size, start_y), 
                         (start_x + i * box_size, start_y + grid_size), 1)
        # Horizontal lines
        if i % 3 != 0:  # Skip every third line (to avoid the thicker 3x3 lines)
            pg.draw.line(screen, pg.Color("#dcdcdc"), (start_x, start_y + i * box_size),
                         (start_x + grid_size, start_y + i * box_size), 1)

    # If a cell is selected, draw a blue circle centered in the selected box
    if selected is not None:
        selected_x = start_x + selected[1] * box_size + box_size // 2
        selected_y = start_y + selected[0] * box_size + box_size // 2
        pg.draw.circle(screen, pg.Color("lightblue"), (selected_x, selected_y), box_size // 3)

    # Draw numbers in the grid with bold font for better readability
    for r in range(9):
        for c in range(9):
            if cell_values[r][c] is not None:
                number_text = font.render(str(cell_values[r][c]), True, pg.Color("black"))
                screen.blit(number_text, (start_x + c * box_size + (box_size - number_text.get_width()) // 2,
                                          start_y + r * box_size + (box_size - number_text.get_height()) // 2))


def draw_buttons():
    # Solve button with rounded corners and hover effect
    pg.draw.rect(screen, pg.Color("#4CAF50"), solve_button, border_radius=10)
    solve_text = button_font.render("Solve", True, pg.Color("white"))
    screen.blit(solve_text, (solve_button.centerx - solve_text.get_width() // 2, solve_button.centery - solve_text.get_height() // 2))

    # Clear button with rounded corners
    pg.draw.rect(screen, pg.Color("#ffcc00"), clear_button, border_radius=10)
    clear_text = button_font.render("Clear", True, pg.Color("white"))
    screen.blit(clear_text, (clear_button.centerx - clear_text.get_width() // 2, clear_button.centery - clear_text.get_height() // 2))

    # Draw number buttons (1-9) in a 3x3 grid with soft colors
    for i in range(9):
        pg.draw.rect(screen, pg.Color("#e0e0e0"), number_buttons[i], border_radius=8)
        number_text = button_font.render(str(i + 1), True, pg.Color("black"))
        screen.blit(number_text, (number_buttons[i].centerx - number_text.get_width() // 2,
                                  number_buttons[i].centery - number_text.get_height() // 2))

    # Draw delete button with rounded corners
    pg.draw.rect(screen, pg.Color("#ff4d4d"), delete_button, border_radius=10)
    delete_text = button_font.render("Del", True, pg.Color("white"))
    screen.blit(delete_text, (delete_button.centerx - delete_text.get_width() // 2,
                              delete_button.centery - delete_text.get_height() // 2))

def update():
    screen.fill(pg.Color("#f4f4f4"))  # Soft light background color
    draw_sudoku_grid()  # Draw the Sudoku grid
    title_surface = font.render("Sudoku Solver", True, pg.Color("black"))
    screen.blit(title_surface, (screensize[0] // 2 - title_surface.get_width() // 2, 20))
    draw_buttons()

def handle_button(event):
    global selected, cell_values, board
    if event.type == pg.MOUSEBUTTONDOWN:
        if solve_button.collidepoint(event.pos):
            print("Solve button clicked!")
            solve(board)  # Solve the Sudoku with the step-by-step method
        elif clear_button.collidepoint(event.pos):  # Handle the Clear button
            print("Clear button clicked!")
            board = [[0] * 9 for _ in range(9)]  # Reset the board
            cell_values = [[None] * 9 for _ in range(9)]  # Clear cell values
            selected = None  # Deselect any selected cell
        elif delete_button.collidepoint(event.pos) and selected is not None:
            cell_values[selected[0]][selected[1]] = None  # Delete the number in the selected cell
            board[selected[0]][selected[1]] = 0
            print("Deleted number in selected cell.")
        elif 100 <= event.pos[0] <= 730 and 100 <= event.pos[1] <= 730:
            box_size = 630 // 9  # Adjusted cell size for the new grid size
            row = (event.pos[1] - 100) // box_size
            col = (event.pos[0] - 100) // box_size
            selected = (row, col)  # Update the selected cell
            print(f"Clicked on cell ({row}, {col})")
        elif selected is not None:  # Number button clicks
            for i in range(9):
                if number_buttons[i].collidepoint(event.pos):
                    cell_values[selected[0]][selected[1]] = i + 1  # Set the number in the selected cell
                    board[selected[0]][selected[1]] = i + 1
                    print(f"Set cell ({selected[0]}, {selected[1]}) to {i + 1}")

# Solver (remains unchanged)
# Solver functions like isSolved(), isFull(), isValid(), etc. go here...


#Solver
ideal = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}

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
    if first_empty == False:# Return the solved board as the last step
        return board
    row, col = first_empty
    for n in range(1, 10):
        if isValid(n, row, col, board):
            board[row][col] = n
            cell_values[row][col] = n
            update()  # Refresh the grid
            pg.display.flip()
            time.sleep(0.01)  # Slow down the recursion
            if solve(board):
                return board
            board[row][col] = 0  # Undo
            cell_values[row][col] = None
            update()
            pg.display.flip()
            time.sleep(0.01)
    return False

    
def loop():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        handle_button(event)
    update()
    pg.display.flip()

while True:
    loop()
