import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.width = 500
        self.height = 500
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg='black')
        self.canvas.pack()
        
        self.snake_size = 20
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.snake_direction = "Right"
        
        self.food_position = self.set_new_food_position()
        self.food = self.canvas.create_rectangle(*self.food_position, 
                                                 self.food_position[0] + self.snake_size, 
                                                 self.food_position[1] + self.snake_size, 
                                                 fill="red")
        
        self.snake_objects = []
        for x, y in self.snake:
            self.snake_objects.append(self.canvas.create_rectangle(x, y, x + self.snake_size, y + self.snake_size, fill="green"))
        
        self.is_game_over = False
        self.master.bind("<KeyPress>", self.change_direction)
        self.move_snake()
        
    def set_new_food_position(self):
        return (random.randint(0, (self.width - self.snake_size) // self.snake_size) * self.snake_size,
                random.randint(0, (self.height - self.snake_size) // self.snake_size) * self.snake_size)
        
    def move_snake(self):
        if self.is_game_over:
            return
        
        x, y = self.snake[0]
        
        if self.snake_direction == "Left":
            x -= self.snake_size
        elif self.snake_direction == "Right":
            x += self.snake_size
        elif self.snake_direction == "Up":
            y -= self.snake_size
        elif self.snake_direction == "Down":
            y += self.snake_size
        
        self.snake = [(x, y)] + self.snake[:-1]
        
        for i, (x, y) in enumerate(self.snake):
            self.canvas.coords(self.snake_objects[i], x, y, x + self.snake_size, y + self.snake_size)
        
        self.check_collisions()
        self.check_food_collision()
        
        if not self.is_game_over:
            self.master.after(100, self.move_snake)
        
    def change_direction(self, event):
        new_direction = event.keysym
        all_directions = ["Left", "Right", "Up", "Down"]
        opposites = ({"Left", "Right"}, {"Up", "Down"})
        
        if (new_direction in all_directions and 
            {new_direction, self.snake_direction} not in opposites):
            self.snake_direction = new_direction
    
    def check_collisions(self):
        x, y = self.snake[0]
        
        if (x < 0 or x >= self.width or
            y < 0 or y >= self.height or
            (x, y) in self.snake[1:]):
            self.is_game_over = True
            self.canvas.create_text(self.width/2, self.height/2, 
                                    text="GAME OVER", fill="white", font=("Arial", 24))
    
    def check_food_collision(self):
        if self.snake[0] == self.food_position:
            self.snake.append(self.snake[-1])
            x, y = self.snake[-1]
            self.snake_objects.append(self.canvas.create_rectangle(x, y, x + self.snake_size, y + self.snake_size, fill="green"))
            self.food_position = self.set_new_food_position()
            self.canvas.coords(self.food, self.food_position[0], self.food_position[1],
                               self.food_position[0] + self.snake_size, self.food_position[1] + self.snake_size)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
