import tkinter as tk
from grid import create_energy_display, init_canvas, create_grid, update_energy_display, create_text_display, log_message
from robot import Robot
from energy import Energy
from constraint import Constraints

def main():
    root = tk.Tk()
    root.title("Robot Navigation Simulator")
    root.configure(bg="#1a1a2e")
    root.resizable(False, False)

    # Create text display at top middle
    text_output = create_text_display(root)
    log_message(text_output, "Robot Navigation Simulator initialized!")

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
            log_message(text_output, "Cannot go forward! You just went backward.")
            return
        
        if energy.can_execute("forward"):
            robot.move("forward")
            constraints.update("forward")
            energy.consume("forward")
            update_energy_display(canvas, energy_text_id, energy.current, energy.max)
            log_message(text_output, f"Moved forward!")
        else:
            log_message(text_output, "Not enough energy!")

    def move_backward():
        # Check constraint first (no reverse movement)
        if not constraints.is_valid("back"):
            log_message(text_output, "Cannot go backward! You just went forward.")
            return
        
        if energy.can_execute("back"):
            robot.move("backward")
            constraints.update("back")
            energy.consume("back")
            update_energy_display(canvas, energy_text_id, energy.current, energy.max)
            log_message(text_output, f"Moved backward! ")
        else:
            log_message(text_output, "Not enough energy!")

    def rotate_left():
        # Check constraint (no consecutive left turns)
        if not constraints.is_valid("left"):
            log_message(text_output, "Cannot turn left twice in a row!")
            return
        
        if energy.can_execute("left"):
            robot.rotate_left()
            constraints.update("left")
            energy.consume("left")
            update_energy_display(canvas, energy_text_id, energy.current, energy.max)
            log_message(text_output, f"Rotated left! ")
        else:
            log_message(text_output, "Not enough energy!")

    def rotate_right():
        # Check constraint (no consecutive right turns)
        if not constraints.is_valid("right"):
            log_message(text_output, "Cannot turn right twice in a row!")
            return
        
        if energy.can_execute("right"):
            robot.rotate_right()
            constraints.update("right")
            energy.consume("right")
            update_energy_display(canvas, energy_text_id, energy.current, energy.max)
            log_message(text_output, f"Rotated right! ")
        else:
            log_message(text_output, "Not enough energy!")

    # recharge and reset energy
    def recharge():
        if energy.consume("recharge"):
            update_energy_display(canvas, energy_text_id, energy.current, energy.max)
            log_message(text_output, "Recharged! Energy: 5/5")
        else:
            log_message(text_output, "Can only recharge when energy = 0")

    def reset_energy():
        energy.reset()
        constraints.reset()
        update_energy_display(canvas, energy_text_id, energy.current, energy.max)
        log_message(text_output, "Energy and constraints reset!")

    # Buttons for testing
    tk.Button(root, text="Forward", command=move_forward).pack(side="left")
    tk.Button(root, text="Backward", command=move_backward).pack(side="left")
    tk.Button(root, text="Rotate Left", command=rotate_left).pack(side="left")
    tk.Button(root, text="Rotate Right", command=rotate_right).pack(side="left")
    tk.Button(root, text="Recharge", command=recharge).pack(side="left")
    tk.Button(root, text="Reset Energy", command=reset_energy).pack(side="left")

    root.mainloop()

if __name__ == "__main__":
    main()