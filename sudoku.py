import pygame
import sys
from sudoku_generator import generate_sudoku



class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = 0
        self.selected = False

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        cell_size = 60
        x = self.col * cell_size
        y = self.row * cell_size
        font = pygame.font.Font(None, 40)

        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, cell_size, cell_size), 3)

        if self.value != 0:
            num = font.render(str(self.value), True, (0, 0, 0))
            self.screen.blit(num, (x, y))
        elif self.sketched_value != 0:
            num = font.render(str(self.sketched_value), True, (150, 150, 150))
            self.screen.blit(num, (x, y))




class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.selected_row = 0
        self.selected_col = 0

        #make board
        self.board = generate_sudoku(9, difficulty)

        self.original = []
        for r in range(9):
            row = []
            for c in range(9):
                row.append(self.board[r][c])
            self.original.append(row)

        self.cells = []
        for r in range(9):
            row = []
            for c in range(9):
                row.append(Cell(self.board[r][c], r, c, screen))
            self.cells.append(row)

    def draw(self):
        cell_size = 60
        for r in range(9):
            for c in range(9):
                self.cells[r][c].draw()
        for i in range(10):
            if i % 3 == 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.screen, (0, 0, 0), (i * cell_size, 0), (i * cell_size, self.height), thick)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * cell_size), (self.width, i * cell_size), thick)

    def select(self, row, col):
        self.cells[self.selected_row][self.selected_col].selected = False
        self.selected_row = row
        self.selected_col = col
        self.cells[row][col].selected = True

    def click(self, x, y):
        cell_size = 60
        if 0 <= x <= self.width and 0 <= y <= self.height:
            row = y // cell_size
            col = x // cell_size
            return (row, col)
        return None

    def clear(self):
        r = self.selected_row
        c = self.selected_col
        if self.original[r][c] == 0:
            self.cells[r][c].set_cell_value(0)
            self.cells[r][c].set_sketched_value(0)

    def sketch(self, value):
        r = self.selected_row
        c = self.selected_col
        if self.original[r][c] == 0:
            self.cells[r][c].set_sketched_value(value)

    def place_number(self, value):
        r = self.selected_row
        c = self.selected_col
        if self.original[r][c] == 0:
            self.cells[r][c].set_cell_value(value)
            self.cells[r][c].set_sketched_value(0)

    def reset_to_original(self):
        for r in range(9):
            for c in range(9):
                self.cells[r][c].set_cell_value(self.original[r][c])
                self.cells[r][c].set_sketched_value(0)

    def is_full(self):
        for r in range(9):
            for c in range(9):
                if self.cells[r][c].value == 0:
                    return False
        return True

    def update_board(self):
        for r in range(9):
            for c in range(9):
                self.board[r][c] = self.cells[r][c].value

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.cells[r][c].value == 0:
                    return (r, c)
        return None

    def check_board(self):
        # 1. Check all rows
        for r in range(9):
            row_values = [self.cells[r][c].value for c in range(9)]
            if len(set(row_values)) != 9:
                return False

        #check all columns
        for c in range(9):
            col_values = [self.cells[r][c].value for r in range(9)]
            if len(set(col_values)) != 9:
                return False

        #check all 3x3 boxes
        for box_row in range(3):
            for box_col in range(3):
                box_values = []
                for r in range(3):
                    for c in range(3):
                        box_values.append(self.cells[box_row * 3 + r][box_col * 3 + c].value)
                
                if len(set(box_values)) != 9:
                    return False

        #if passes all checks, return true
        return True




pygame.init()
screen = pygame.display.set_mode((540, 600))


def main():
    state = "start"
    board = None
    font = pygame.font.Font(None, 40)

    while True:
        screen.fill((255, 255, 255))

        if state == "start":
            screen.blit(font.render("Welcome to Sudoku", True, (0, 0, 0)), (100, 150))
            screen.blit(font.render("Select Game Mode:", True, (0, 0, 0)), (130, 250))

            pygame.draw.rect(screen, (0, 0, 0), (60, 320, 120, 45), 2)
            pygame.draw.rect(screen, (0, 0, 0), (210, 320, 120, 45), 2)
            pygame.draw.rect(screen, (0, 0, 0), (360, 320, 120, 45), 2)

            screen.blit(font.render("EASY", True, (0, 0, 0)), (75, 330))
            screen.blit(font.render("MEDIUM", True, (0, 0, 0)), (215, 330))
            screen.blit(font.render("HARD", True, (0, 0, 0)), (375, 330))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 60 <= x <= 180 and 320 <= y <= 365:
                        board = Board(540, 540, screen, 30)
                        state = "game"
                    elif 210 <= x <= 330 and 320 <= y <= 365:
                        board = Board(540, 540, screen, 40)
                        state = "game"
                    elif 360 <= x <= 480 and 320 <= y <= 365:
                        board = Board(540, 540, screen, 50)
                        state = "game"

        elif state == "game":
            board.draw()

            pygame.draw.rect(screen, (0, 0, 0), (100, 555, 100, 35), 2)
            pygame.draw.rect(screen, (0, 0, 0), (220, 555, 100, 35), 2)
            pygame.draw.rect(screen, (0, 0, 0), (340, 555, 100, 35), 2)

            screen.blit(font.render("RESET", True, (0, 0, 0)), (110, 563))
            screen.blit(font.render("RESTART", True, (0, 0, 0)), (222, 563))
            screen.blit(font.render("EXIT", True, (0, 0, 0)), (355, 563))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 100 <= x <= 200 and 555 <= y <= 590:
                        board.reset_to_original()
                    elif 220 <= x <= 320 and 555 <= y <= 590:
                        board = None
                        state = "start"
                    elif 340 <= x <= 440 and 555 <= y <= 590:
                        pygame.quit()
                        sys.exit()
                    else:
                        cell = board.click(x, y)
                        if cell is not None:
                            board.select(cell[0], cell[1])
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        board.sketch(1)
                    elif event.key == pygame.K_2:
                        board.sketch(2)
                    elif event.key == pygame.K_3:
                        board.sketch(3)
                    elif event.key == pygame.K_4:
                        board.sketch(4)
                    elif event.key == pygame.K_5:
                        board.sketch(5)
                    elif event.key == pygame.K_6:
                        board.sketch(6)
                    elif event.key == pygame.K_7:
                        board.sketch(7)
                    elif event.key == pygame.K_8:
                        board.sketch(8)
                    elif event.key == pygame.K_9:
                        board.sketch(9)
                    elif event.key == pygame.K_RETURN:
                        r = board.selected_row
                        c = board.selected_col
                        val = board.cells[r][c].sketched_value
                        board.place_number(val)
                        board.update_board()
                        if board.is_full():
                            if board.check_board():
                                state = "win"
                            else:
                                state = "lose"
                    elif event.key == pygame.K_BACKSPACE:
                        board.clear()
                    elif event.key == pygame.K_UP:
                        if board.selected_row > 0:
                            board.select(board.selected_row - 1, board.selected_col)
                    elif event.key == pygame.K_DOWN:
                        if board.selected_row < 8:
                            board.select(board.selected_row + 1, board.selected_col)
                    elif event.key == pygame.K_LEFT:
                        if board.selected_col > 0:
                            board.select(board.selected_row, board.selected_col - 1)
                    elif event.key == pygame.K_RIGHT:
                        if board.selected_col < 8:
                            board.select(board.selected_row, board.selected_col + 1)

        elif state == "win":
            screen.blit(font.render("Game Won!", True, (0, 0, 0)), (100, 200))
            pygame.draw.rect(screen, (0, 0, 0), (200, 320, 120, 45), 2)
            screen.blit(font.render("EXIT", True, (0, 0, 0)), (225, 330))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 200 <= x <= 320 and 320 <= y <= 365:
                        pygame.quit()
                        sys.exit()

        elif state == "lose":
            screen.blit(font.render("Game Over :(", True, (0, 0, 0)), (100, 200))
            pygame.draw.rect(screen, (0, 0, 0), (200, 320, 120, 45), 2)
            screen.blit(font.render("RESTART", True, (0, 0, 0)), (205, 330))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 200 <= x <= 320 and 320 <= y <= 365:
                        board = None
                        state = "start"

        pygame.display.update()


main()