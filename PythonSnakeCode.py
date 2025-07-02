import tkinter as tk
import random
import math

class SnakeGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snake Game")
        self.geometry("800x800")
        self.resizable(False, False)

        self.width = 800
        self.height = 800
        self.cell_size = 20
        self.snake_direction = 'Right'
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = list() # food(x, y, type)

        self.update_interval = 100  # To control the speed of the snake
        
        self.time = -1
        self.time_running = True

        self.menu_frame = tk.Frame(self)
        self.menu_frame.pack(fill="both", expand=True)

        self.game_frame = tk.Frame(self)
        self.canvas = tk.Canvas(self.game_frame, bg='black', width=self.width, height=self.height)
        self.start_game()

    def draw_star(self,canvas, x, y, size, color="red"):
        """Draw a star centered at (x, y) with the given size and color."""
        points = []
        for i in range(5):
            angle = i * 144  # 144 degrees between star points
            outer_x = x + size * math.cos(math.radians(angle))
            outer_y = y - size * math.sin(math.radians(angle))
            points.append((outer_x, outer_y))
        # Flatten the points list for tkinter
        flat_points = [coord for point in points for coord in point]
        canvas.create_polygon(flat_points, fill=color, outline="black")

    def draw_circle(self,canvas, x, y, radius, color="yellow"):
        """Draw a circle centered at (x, y) with the given radius and color."""
        canvas.create_oval(
            x - radius, y - radius,  # Top-left corner
            x + radius, y + radius,  # Bottom-right corner
            fill=color, outline="black"
        )

    def generate_initial_food(self):
        for i in range(5):
            x = random.randint(0, (self.width // self.cell_size) - 1) * self.cell_size
            y = random.randint(0, (self.height // self.cell_size) - 1) * self.cell_size
            self.food.append((x, y, 1))
        for i in range(2):
            x = random.randint(0, (self.width // self.cell_size) - 1) * self.cell_size
            y = random.randint(0, (self.height // self.cell_size) - 1) * self.cell_size
            self.food.append((x, y, 2))
        
    def start_game(self):
        self.menu_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)
        self.canvas.pack()
        self.generate_initial_food()
        self.setup_ui()
        self.run_game()
        self.timer()  # Start the timer

    def timer(self):
        if self.time_running:
            self.time += 1
            self.update_interval = max(20, self.update_interval - 4)  # Increase speed over time
            self.after(1000, self.timer)

    def setup_ui(self):
        self.update_ui()
        self.bind("<KeyPress>", self.change_direction)

    def update_ui(self):
        self.canvas.delete('all')
        # Display current length
        self.canvas.create_text(50, 10, text=f"Length: {len(self.snake)}", font=("Arial",10), fill="white")
        # Display current time
        self.canvas.create_text(700, 10, text=f"Time: {self.time}s", font=("Arial",10), fill="white")
        # Draw food
        for food in self.food:
            x, y, food_type = food
            if food_type == 1:
                self.draw_circle(self.canvas, x + self.cell_size // 2, y + self.cell_size // 2, self.cell_size // 2)
            if food_type == 2:
                self.draw_star(self.canvas, x + self.cell_size // 2, y + self.cell_size // 2, self.cell_size // 2)
        # Draw snake
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill='green')

    def run_game(self):
        self.move_snake()
        self.after(self.update_interval, self.run_game)

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.snake_direction == 'Left':
            head_x -= self.cell_size
        elif self.snake_direction == 'Right':
            head_x += self.cell_size
        elif self.snake_direction == 'Up':
            head_y -= self.cell_size
        elif self.snake_direction == 'Down':
            head_y += self.cell_size

        # Check for game stop
        if head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height or (head_x, head_y) in self.snake:
            self.time_running = False  # Stop the timer
            self.canvas.create_text(
            self.width // 2, self.height // 2,
            text="Game Over!", font=("Arial", 24), fill="red"
            )
            self.canvas.create_text(
            self.width // 2, self.height // 2 + 30,
            text=f"Length: {len(self.snake)}", font=("Arial",18), fill="red"
            )
            self.canvas.create_text(
            self.width // 2, self.height // 2 + 60,
            text=f"Time used: {self.time}s", font=("Arial",18), fill="red"
            )
            self.after(5000, self.quit)  # Wait for 5 seconds before quitting
            return
        elif len(self.snake) >=8:
            self.time_running = False  # Stop the timer
            self.canvas.create_text(
            self.width // 2, self.height // 2,
            text="You Win!", font=("Arial", 24), fill="green"
            )
            self.canvas.create_text(
            self.width // 2, self.height // 2 + 30,
            text=f"Time used: {self.time}s", font=("Arial",18), fill="green"
            )
            self.after(5000, self.quit) # Wait for 5 seconds before quitting
            return
        
        # Check for food collision
        for food in self.food:
            x, y, food_type = food
            if head_x == x and head_y == y:
                if food_type == 1:
                    # Increase snake length
                    self.snake.append(self.snake[-1])
                elif food_type == 2:
                    pos1 = self.snake[-1]
                    pos2 = self.snake[-2]
                    if pos1[0] == pos2[0]:
                        self.snake.append((pos1[0], pos1[1] + (pos1[1] - pos2[1])))
                    else:
                        self.snake.append((pos1[0] + (pos1[0] - pos2[0]), pos1[1]))
                    self.snake.append(self.snake[-1])
                # Remove food from the list
                self.food.remove((x, y, food_type))
                # Generate new food
                x = random.randint(0, (self.width // self.cell_size) - 1) * self.cell_size
                y = random.randint(0, (self.height // self.cell_size) - 1) * self.cell_size
                self.food.append((x, y, food_type))
                break
        
        new_head = (head_x, head_y)
        self.snake = [new_head] + self.snake[:-1]
        self.update_ui()

    def change_direction(self, event):
        opposite_directions = {'Left': 'Right', 'Right': 'Left', 'Up': 'Down', 'Down': 'Up'}
        if event.keysym in ['Left', 'Right', 'Up', 'Down']:
            # Check if the new direction is opposite to the current direction
            if event.keysym != opposite_directions[self.snake_direction] and self.time_running:
                self.snake_direction = event.keysym


if __name__ == "__main__":
    game = SnakeGame()
    game.mainloop()
