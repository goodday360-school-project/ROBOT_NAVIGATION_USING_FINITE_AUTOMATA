import tkinter as tk
from grid import init_canvas, create_grid
from robot import Robot

def main():
    root = tk.Tk()
    root.title("Grid + Robot")
    root.configure(bg="#1a1a2e")
    root.resizable(False, False)

    canvas, origin = init_canvas(root)
    create_grid(canvas)

    # Create robot and explicitly set starting position at (0,0)
    robot = Robot(canvas, origin, "robot.png")
    robot.x, robot.y = 0, 0   # ensure bottom-left start
    robot.update_position()


    # -> Below are codes for testing

    # Example controls
    def move_forward():
        robot.move("forward")

    def move_backward():
        robot.move("backward")

    def turn_north():
        robot.change_direction("north")

    def turn_south():
        robot.change_direction("south")

    def turn_east():
        robot.change_direction("east")

    def turn_west():
        robot.change_direction("west")

    # Buttons for testing
    tk.Button(root, text="Forward", command=move_forward).pack(side="left")
    tk.Button(root, text="Backward", command=move_backward).pack(side="left")
    tk.Button(root, text="North", command=turn_north).pack(side="left")
    tk.Button(root, text="South", command=turn_south).pack(side="left")
    tk.Button(root, text="East", command=turn_east).pack(side="left")
    tk.Button(root, text="West", command=turn_west).pack(side="left")

    # <-

    root.mainloop()

if __name__ == "__main__":
    main()
