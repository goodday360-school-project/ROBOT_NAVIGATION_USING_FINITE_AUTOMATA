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

    # Create robot at (0,0) bottom-left
    robot = Robot(canvas, origin, "robot.png")
    robot.x, robot.y = 0, 0
    robot.update_position()

    # -> Below code are testing code
    # Example controls
    def move_forward():
        robot.move("forward")

    def move_backward():
        robot.move("backward")

    def rotate_left():
        robot.rotate_left()

    def rotate_right():
        robot.rotate_right()

    # Buttons for testing
    tk.Button(root, text="Forward", command=move_forward).pack(side="left")
    tk.Button(root, text="Backward", command=move_backward).pack(side="left")
    tk.Button(root, text="Rotate Left", command=rotate_left).pack(side="left")
    tk.Button(root, text="Rotate Right", command=rotate_right).pack(side="left")
    # <-


    root.mainloop()

if __name__ == "__main__":
    main()
