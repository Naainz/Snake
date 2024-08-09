import tkinter as tk
import random
import time

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")

        # Set up the frames for the stock chart and the snake game
        self.left_frame = tk.Frame(master, width=500, height=500, bg="black")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.separator_line = tk.Frame(master, width=2, height=500, bg="grey")
        self.separator_line.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(master, width=500, height=500, bg="black")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Initialize the canvas for the snake game
        self.width = 500
        self.height = 500
        self.canvas = tk.Canvas(self.right_frame, width=self.width, height=self.height, bg='black')
        self.canvas.pack()

        # Initialize the stock chart
        self.stock_canvas = tk.Canvas(self.left_frame, width=500, height=500, bg='black')
        self.stock_canvas.pack()

        self.elapsed_time = 0
        self.stopwatch = self.stock_canvas.create_text(450, 20, text="Time: 0s", fill="white", font=("Arial", 12))

        self.stock_value = 100
        self.previous_stock_values = [self.stock_value]
        self.max_price = 100

        # Draw the chart axes
        self.draw_axes()

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
        self.master.bind("<KeyPress>", self.key_press_handler)
        self.update_stock_chart()
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
        
    def key_press_handler(self, event):
        new_direction = event.keysym
        
        if new_direction in ["Left", "Right", "Up", "Down"]:
            self.change_direction(new_direction)
        elif new_direction == "q":
            self.master.quit()
        elif new_direction == "Return" and self.is_game_over:
            self.restart_game()

    def change_direction(self, new_direction):
        all_directions = ["Left", "Right", "Up", "Down"]
        opposites = ({"Left", "Right"}, {"Up", "Down"})
        
        if (new_direction in all_directions and 
            {new_direction, self.snake_direction} not in opposites):
            self.snake_direction = new_direction
    
    def check_collisions(self):
        x, y = self.snake[0]
        
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            self.game_over("You hit the wall!")
        elif (x, y) in self.snake[1:]:
            self.game_over("You collided with yourself!")
    
    def check_food_collision(self):
        if self.snake[0] == self.food_position:
            self.snake.append(self.snake[-1])
            x, y = self.snake[-1]
            self.snake_objects.append(self.canvas.create_rectangle(x, y, x + self.snake_size, y + self.snake_size, fill="green"))
            self.food_position = self.set_new_food_position()
            self.canvas.coords(self.food, self.food_position[0], self.food_position[1],
                               self.food_position[0] + self.snake_size, self.food_position[1] + self.snake_size)
            self.update_stock_value(10)  # Increase stock value by $10

    def game_over(self, reason):
        self.is_game_over = True
        self.canvas.create_text(self.width/2, self.height/2, 
                                text=f"GAME OVER\n{reason}\nPress Enter to Play Again", fill="white", font=("Arial", 24))

    def restart_game(self):
        self.canvas.delete("all")
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
        self.stock_value = 100  # Reset stock value
        self.elapsed_time = 0  # Reset timer
        self.previous_stock_values = [self.stock_value]
        self.stock_canvas.delete("chart_line")
        self.stock_canvas.delete("x_axis_label")
        self.draw_axes()  # Redraw axes
        self.update_stock_chart()  # Reset stock chart
        self.move_snake()

    def update_stock_chart(self):
        if self.is_game_over:
            return
        
        self.elapsed_time += 1
        self.stock_canvas.itemconfig(self.stopwatch, text=f"Time: {self.elapsed_time}s")
        
        self.previous_stock_values.append(self.stock_value)
        self.stock_value -= 5  # Decrease stock value by $5 each second
        
        if self.stock_value <= 0:
            self.stock_value = 0
            self.game_over("Stock value reached $0!")

        self.extend_chart_line()

        if not self.is_game_over:
            self.master.after(1000, self.update_stock_chart)
        
    def update_stock_value(self, value):
        self.previous_stock_values[-1] = self.stock_value
        self.stock_value += value
        self.stock_value = min(self.stock_value, 100)  # Cap the stock value at $100

    def draw_axes(self):
        # Draw y-axis (price) with labels
        for i in range(0, self.max_price + 1, 20):
            y = 490 - (i * 490 / self.max_price)
            self.stock_canvas.create_line(50, y, 55, y, fill="white")
            self.stock_canvas.create_text(40, y, text=f"${i}", anchor=tk.E, fill="white", font=("Arial", 8))

        # Draw the main y-axis
        self.stock_canvas.create_line(50, 490, 50, 10, fill="white", width=2)

    def extend_chart_line(self):
        # Determine how many segments to draw based on elapsed time
        segments = self.elapsed_time
        segment_width = 400 / segments

        self.stock_canvas.delete("chart_line")
        for i in range(1, segments + 1):
            x1 = 50 + (i - 1) * segment_width
            y1 = 490 - (self.previous_stock_values[i - 1] * 490 / self.max_price)
            x2 = 50 + i * segment_width
            y2 = 490 - (self.previous_stock_values[i] * 490 / self.max_price)
            line_color = "green" if y2 < y1 else "red"
            self.stock_canvas.create_line(x1, y1, x2, y2, fill=line_color, width=2, tags="chart_line")

        # Update the x-axis label for the current time
        self.stock_canvas.delete("x_axis_label")
        self.stock_canvas.create_text(450, 495, text=f"{self.elapsed_time}s", anchor=tk.N, fill="white", font=("Arial", 8), tags="x_axis_label")

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
