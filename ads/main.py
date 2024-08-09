import tkinter as tk
import random
import time
import threading
from tkinter import messagebox
from tkinter import Toplevel
from PIL import Image, ImageTk
import os

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
        self.master.bind("<KeyPress>", self.key_press_handler)
        
        self.ad_popup_label = None
        self.ad_popup_timer = None
        
        self.snake_speed = 135  
        self.ad_timer = 10
        self.next_ad_time = self.get_next_ad_time()
        self.ad_thread = threading.Thread(target=self.play_ads)
        self.ad_thread.start()
        
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
            self.master.after(self.snake_speed, self.move_snake)
        
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
        self.move_snake()

    def get_next_ad_time(self):
        return time.time() + random.randint(5, 10)
    
    def play_ads(self):
        while not self.is_game_over:
            time_until_ad = self.next_ad_time - time.time()
            if time_until_ad <= 5 and self.ad_popup_label is None:
                self.ad_popup_timer = int(time_until_ad)
                self.show_ad_popup()
            
            if time_until_ad <= 0:
                self.show_ad()
                self.next_ad_time = self.get_next_ad_time()
                
            time.sleep(0.1)

    def show_ad_popup(self):
        if self.ad_popup_timer > 0:
            if self.ad_popup_label is None:
                self.ad_popup_label = tk.Label(self.master, text=f"Ad in {self.ad_popup_timer} seconds", fg="white", bg="red")
                self.ad_popup_label.place(x=self.width-150, y=self.height-30)
            else:
                self.ad_popup_label.config(text=f"Ad in {self.ad_popup_timer} seconds")
            
            self.ad_popup_timer -= 1
            self.master.after(1000, self.show_ad_popup)
        else:
            self.ad_popup_label.place_forget()
            self.ad_popup_label = None

    def show_ad(self):
        ad_window = Toplevel(self.master)
        ad_window.geometry("400x300+100+100")
        ad_window.overrideredirect(True)
        ad_window.attributes("-topmost", True)

        video_file = random.choice(os.listdir("./db"))
        video_path = os.path.join("./db", video_file)

        
        video_image = Image.open("ad_preview.jpg")  
        video_image = video_image.resize((400, 300), Image.ANTIALIAS)
        video_photo = ImageTk.PhotoImage(video_image)

        label = tk.Label(ad_window, image=video_photo)
        label.image = video_photo
        label.pack()

        
        self.master.after(4000, ad_window.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
