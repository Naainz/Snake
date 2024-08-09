import curses
import time
import sys
from random import randint

class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.icons = {
            0: ' ',   # Empty space
            1: 'O',   # Body of the snake
            2: '🐍',  # Head of the snake
            3: '🍎',  # Entity to eat
        }
        self.field = []
        self._generate_field()
        self.add_entity()

    def add_entity(self):
        while True:
            i = randint(1, self.height - 2)
            j = randint(1, self.width - 2)
            if self.field[i][j] == 0:  # Place apple where there's no snake
                self.field[i][j] = 3
                break

    def _generate_field(self):
        self.field = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def render(self, screen, snake_coords):
        # Clear the field before rendering
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                if self.field[i][j] != 3:  # Keep the apple
                    self.field[i][j] = 0  # Clear snake positions

        # Update snake positions on the field
        for coord in snake_coords[:-1]:
            self.field[coord[0]][coord[1]] = 1  # Body of the snake

        head = snake_coords[-1]
        self.field[head[0]][head[1]] = 2  # Head of the snake

        # Render the field with border
        for i in range(self.height):
            for j in range(self.width):
                if i == 0 or i == self.height - 1 or j == 0 or j == self.width - 1:
                    screen.addstr(i, j * 2, '█')  # Border
                else:
                    screen.addstr(i, j * 2, self.icons[self.field[i][j]])

class Snake:
    def __init__(self, field):
        self.direction = curses.KEY_RIGHT
        self.coords = [[1, 1], [1, 2], [1, 3], [1, 4]]
        self.field = field

    def set_direction(self, ch):
        opposite_directions = {curses.KEY_LEFT: curses.KEY_RIGHT, curses.KEY_RIGHT: curses.KEY_LEFT,
                               curses.KEY_UP: curses.KEY_DOWN, curses.KEY_DOWN: curses.KEY_UP}
        if ch != opposite_directions.get(self.direction, None):
            self.direction = ch

    def move(self):
        head = self.coords[-1][:]

        if self.direction == curses.KEY_UP:
            head[0] -= 1
        elif self.direction == curses.KEY_DOWN:
            head[0] += 1
        elif self.direction == curses.KEY_RIGHT:
            head[1] += 1
        elif self.direction == curses.KEY_LEFT:
            head[1] -= 1

        # Check for collisions with walls or self
        if head in self.coords or head[0] in (0, self.field.height - 1) or head[1] in (0, self.field.width - 1):
            return False  # Game over

        self.coords.append(head)

        # Check if apple is eaten
        if self.field.field[head[0]][head[1]] == 3:
            self.field.add_entity()  # Add a new apple
        else:
            self.coords.pop(0)  # Remove the tail

        return True

def main(screen):
    curses.curs_set(0)  # Hide the cursor
    screen.nodelay(1)  # Non-blocking input
    field = Field(25, 15)
    snake = Snake(field)

    while True:
        ch = screen.getch()
        if ch != -1:
            snake.set_direction(ch)

        if ch == ord('q'):
            sys.exit()

        if not snake.move():
            screen.addstr(0, 0, "Game Over! Press Enter to play again or 'q' to quit.")
            screen.refresh()
            while True:
                key = screen.getch()
                if key == ord('q'):
                    sys.exit()
                elif key == 10:  # Enter key
                    main(screen)  # Restart game
                    return

        field.render(screen, snake.coords)
        screen.refresh()
        time.sleep(0.1)

if __name__ == '__main__':
    curses.wrapper(main)
