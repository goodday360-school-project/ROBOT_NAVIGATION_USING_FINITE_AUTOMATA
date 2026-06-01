import tkinter as tk
from PIL import Image, ImageTk   # Pillow for scaling + rotation
from grid import CELL_SIZE, GRID_SIZE

class Robot:
    def __init__(self, canvas, origin, image_path="robot.png"):
        self.canvas = canvas
        self.ox, self.oy = origin
        self.x, self.y = 0, 0  # start at bottom-left
        self.directions = ["north", "east", "south", "west"]
        self.direction_index = 0  # 0 = north by default

        # Load image with Pillow
        base_img = Image.open(image_path)

        # Scale image to fit inside a cell
        base_img = base_img.resize((CELL_SIZE - 10, CELL_SIZE - 10), Image.Resampling.LANCZOS)
        self.base_img = base_img

        # Default facing north (original faces down → rotate 180)
        self.image = ImageTk.PhotoImage(self.base_img.rotate(180))
        self.robot_id = self.canvas.create_image(0, 0, image=self.image)
        self.update_position()

    def update_position(self):
        # Convert grid coords to canvas coords (bottom-left origin)
        x_pix = self.ox + self.x * CELL_SIZE + CELL_SIZE // 2
        y_pix = self.oy + (GRID_SIZE - 1 - self.y) * CELL_SIZE + CELL_SIZE // 2
        self.canvas.coords(self.robot_id, x_pix, y_pix)

    def rotate_left(self):
        # Turn left (counter-clockwise)
        self.direction_index = (self.direction_index - 1) % 4
        self._update_image()

    def rotate_right(self):
        # Turn right (clockwise)
        self.direction_index = (self.direction_index + 1) % 4
        self._update_image()

    def _update_image(self):
        direction = self.directions[self.direction_index]
        if direction == "north":
            rotated = self.base_img.rotate(180)
        elif direction == "south":
            rotated = self.base_img.rotate(0)   # original faces down
        elif direction == "east":
            rotated = self.base_img.rotate(90)
        elif direction == "west":
            rotated = self.base_img.rotate(270)

        self.image = ImageTk.PhotoImage(rotated)
        self.canvas.itemconfig(self.robot_id, image=self.image)

    def move(self, method):
        dx, dy = 0, 0
        direction = self.directions[self.direction_index]

        if direction == "north":
            dy = 1 if method == "forward" else -1
        elif direction == "south":
            dy = -1 if method == "forward" else 1
        elif direction == "east":
            dx = 1 if method == "forward" else -1
        elif direction == "west":
            dx = -1 if method == "forward" else 1

        new_x = self.x + dx
        new_y = self.y + dy

        # Boundary check
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            self.x, self.y = new_x, new_y
            self.update_position()
