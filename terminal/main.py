import curses
import time
import random

GRID_WIDTH = 30
GRID_HEIGHT = 10
SNAKE_CHAR = '🐍'
FOOD_CHAR = '🍎'
EMPTY_CHAR = ' '
DELAY = 0.2

def initialize_game():
    snake = [(5, 5), (5, 6), (5, 7)]  
    direction = (0, 1)  
    food = generate_food(snake)
    game_over = False
    return snake, direction, food, game_over

def generate_food(snake):
    while True:
        food = (random.randint(0, GRID_HEIGHT - 1), random.randint(0, GRID_WIDTH - 1))
        if food not in snake:
            return food

def draw_game(snake, food, stdscr):
    stdscr.clear()
    grid = [[EMPTY_CHAR] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    for segment in snake:
        grid[segment[0]][segment[1]] = SNAKE_CHAR

    grid[food[0]][food[1]] = FOOD_CHAR

    for row in grid:
        stdscr.addstr(''.join(row) + '\n')
    
    stdscr.refresh()

def update_game(snake, direction, food):
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    if (new_head[0] < 0 or new_head[0] >= GRID_HEIGHT or
        new_head[1] < 0 or new_head[1] >= GRID_WIDTH or
        new_head in snake):
        return snake, food, True

    snake.insert(0, new_head)

    if new_head == food:
        food = generate_food(snake)
    else:
        snake.pop()

    return snake, food, False

def start_game_countdown(stdscr):
    for i in range(3, 0, -1):
        stdscr.clear()
        stdscr.addstr(0, 0, f"Game will start in {i} seconds...")
        stdscr.refresh()
        time.sleep(1)

def play_game(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)

    start_game_countdown(stdscr)
    snake, direction, food, game_over = initialize_game()

    while not game_over:
        draw_game(snake, food, stdscr)

        key = stdscr.getch()
        if key == curses.KEY_UP and direction != (1, 0):
            direction = (-1, 0)
        elif key == curses.KEY_DOWN and direction != (-1, 0):
            direction = (1, 0)
        elif key == curses.KEY_LEFT and direction != (0, 1):
            direction = (0, -1)
        elif key == curses.KEY_RIGHT and direction != (0, -1):
            direction = (0, 1)

        snake, food, game_over = update_game(snake, direction, food)
        time.sleep(DELAY)

    draw_game(snake, food, stdscr)
    stdscr.addstr(11, 0, "Game Over! Press Enter to play again or 'q' to quit.")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('\n') or key == 10:
            return True
        elif key == ord('q'):
            return False

def main(stdscr):
    while True:
        if not play_game(stdscr):
            break

if __name__ == "__main__":
    curses.wrapper(main)
