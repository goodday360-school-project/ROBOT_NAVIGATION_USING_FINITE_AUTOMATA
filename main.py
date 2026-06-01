import tkinter as tk
from grid import create_energy_display, init_canvas, create_grid, update_energy_display
from robot import Robot
from energy import Energy
from constraint import Constraints

def main():
    root = tk.Tk()
    root.title("Grid + Robot")
    root.configure(bg="#1a1a2e")
    root.resizable(False, False)

    canvas, origin, canvas_w, canvas_h = init_canvas(root)
    create_grid(canvas)
    
    # energy system
    energy = Energy()
    # constraints system
    constraints = Constraints()
    
    energy_text_id = create_energy_display(canvas, canvas_w, canvas_h)
    update_energy_display(canvas, energy_text_id, energy.current, energy.max)
    
    # Create robot at (0,0) bottom-left
    robot = Robot(canvas, origin, "robot.png")
    robot.x, robot.y = 0, 0
    robot.update_position()

    # -> Below code are testing code
    # Example controls
    def move_forward():
        # Check constraint first (no reverse movement)
        if not constraints.is_valid("forward"):
            print("Cannot go forward! You just went backward. Do something else first.")
            return
        
        if energy.can_execute("forward"):
            robot.move("forward")
            constraints.update("forward")  # Remember this movement
            energy.consume("forward")
            update_energy_display(canvas, energy_text_id, energy.current, energy.max)
        else:
            print("Not enough energy!")

    def move_backward():
        # Check constraint first (no reverse movement)
        if not constraints.is_valid("back"):
            print("Cannot go backward! You just went forward. Do something else first.")
            return
        
        if energy.can_execute("back"):
            robot.move("backward")
            constraints.update("back")  # Remember this movement
            energy.consume("back")
            update_energy_display(canvas, energy_text_id, energy.current, energy.max)
        else:
            print("Not enough energy!")

    def rotate_left():
        # Check constraint (no consecutive left turns)
        if not constraints.is_valid("left"):
            print("Cannot turn left twice in a row!")
            return
        
        if energy.can_execute("left"):
            robot.rotate_left()
            constraints.update("left")  # Remember this turn
            energy.consume("left")
            update_energy_display(canvas, energy_text_id, energy.current, energy.max)
        else:
            print("Not enough energy!")

    def rotate_right():
        # Check constraint (no consecutive right turns)
        if not constraints.is_valid("right"):
            print("Cannot turn right twice in a row!")
            return
        
        if energy.can_execute("right"):
            robot.rotate_right()
            constraints.update("right")  # Remember this turn
            energy.consume("right")
            update_energy_display(canvas, energy_text_id, energy.current, energy.max)
        else:
            print("Not enough energy!")

    # recharge and reset energy
    def recharge():
        if energy.consume("recharge"):
            update_energy_display(canvas, energy_text_id, energy.current, energy.max)
            print("Recharged!")
        else:
            print("Can only recharge when energy = 0")

    def reset_energy():
        energy.reset()
        constraints.reset()  # Also reset constraints
        update_energy_display(canvas, energy_text_id, energy.current, energy.max)
        print("Energy and constraints reset")

    # Buttons for testing
    tk.Button(root, text="Forward", command=move_forward).pack(side="left")
    tk.Button(root, text="Backward", command=move_backward).pack(side="left")
    tk.Button(root, text="Rotate Left", command=rotate_left).pack(side="left")
    tk.Button(root, text="Rotate Right", command=rotate_right).pack(side="left")
    tk.Button(root, text="Recharge", command=recharge).pack(side="left")
    tk.Button(root, text="Reset Energy", command=reset_energy).pack(side="left")
    # <-

    root.mainloop()

if __name__ == "__main__":
    main()