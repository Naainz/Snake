import curses
import time
import sys
from random import randint

class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.icons = {
            0: """.""",  
            1: """🟩""",  
            2: """🟢""",  
            3: """🍎""",  
        }
        self.snake_coords = []
        self._generate_field()
        self.add_entity()

    def add_entity(self):
        while True:
            i = randint(0, self.height - 1)
            j = randint(0, self.width - 1)
            entity = [i, j]
            if entity not in self.snake_coords:
                self.field[i][j] = 3
                break

    def _generate_field(self):
        self.field = [[0 for j in range(self.width)] for i in range(self.height)]

    def _clear_field(self):
        self.field = [[j if j != 1 and j != 2 else 0 for j in i] for i in self.field]

    def render(self, screen):
        self._clear_field()

        for i, j in self.snake_coords:
            self.field[i][j] = 1

        head = self.snake_coords[-1]
        self.field[head[0]][head[1]] = 2

        for i in range(self.height):
            row = ''
            for j in range(self.width):
                row += self.icons[self.field[i][j]]
            
            
            screen.addstr(i, 0, row)

    def get_entity_pos(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.field[i][j] == 3:
                    return [i, j]
        return [-1, -1]

    def is_snake_eat_entity(self):
        entity = self.get_entity_pos()
        head = self.snake_coords[-1]
        return entity == head

class Snake:
    def __init__(self, name):
        self.name = name
        self.direction = curses.KEY_RIGHT
        self.coords = [[0, 0], [0, 1], [0, 2], [0, 3]]

    def set_direction(self, ch):
        if ch == curses.KEY_LEFT and self.direction == curses.KEY_RIGHT:
            return
        if ch == curses.KEY_RIGHT and self.direction == curses.KEY_LEFT:
            return
        if ch == curses.KEY_UP and self.direction == curses.KEY_DOWN:
            return
        if ch == curses.KEY_DOWN and self.direction == curses.KEY_UP:
            return
        self.direction = ch

    def level_up(self):
        a = self.coords[0]
        b = self.coords[1]
        tail = a[:]

        if a[0] < b[0]:
            tail[0] -= 1
        elif a[1] < b[1]:
            tail[1] -= 1
        elif a[0] > b[0]:
            tail[0] += 1
        elif a[1] > b[1]:
            tail[1] += 1

        self.coords.insert(0, tail)

    def is_alive(self):
        head = self.coords[-1]
        snake_body = self.coords[:-1]

        if head[0] < 0 or head[0] >= self.field.height or head[1] < 0 or head[1] >= self.field.width:
            print("Game Over! You hit a wall.")
            return False
        if head in snake_body:
            print("Game Over! You ran into yourself.")
            return False
        return True

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

        del self.coords[0]
        self.coords.append(head)
        self.field.snake_coords = self.coords

        if not self.is_alive():
            return False

        if self.field.is_snake_eat_entity():
            curses.beep()
            self.level_up()
            self.field.add_entity()

        return True

    def set_field(self, field):
        self.field = field

def main(screen):
    while True:
        screen.clear()
        field = Field(30, 20)
        snake = Snake("Hackclub Arcade")
        snake.set_field(field)
        screen.timeout(100)

        while True:
            ch = screen.getch()
            if ch != -1:
                snake.set_direction(ch)

            if ch == ord('q'):
                sys.exit()

            if not snake.move():
                break

            field.render(screen)
            screen.refresh()
            time.sleep(0.1)

        screen.addstr(0, 0, "Press Enter to play again or 'q' to quit.")
        screen.refresh()
        key = screen.getch()
        if key == ord('q'):
            sys.exit()
        elif key == 10:  
            continue

if __name__ == '__main__':
    curses.wrapper(main)
