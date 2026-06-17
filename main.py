import tkinter as tk
from grid import (create_energy_display, init_canvas, create_grid,
                  update_energy_display, create_text_display, log_message,
                  draw_items, remove_item_from_canvas)
from robot import Robot
from energy import Energy
from constraint import Constraints
from tasks import Tasks
from loop_detector import LoopDetector
from shared import CMD_BACK, CMD_BACK, CMD_DROP, CMD_FORWARD, CMD_LEFT, CMD_PICK, CMD_PICK, CMD_RECHARGE, CMD_RIGHT
                    


def main():
    root = tk.Tk()
    root.title("Robot Navigation Simulator")
    root.configure(bg="#1a1a2e")
    root.resizable(False, False)

    # Create text display at top middle
    text_output = create_text_display(root)
    log_message(text_output, "Press START to begin!")

    canvas, origin, canvas_w, canvas_h = init_canvas(root)
    create_grid(canvas)

    # energy system
    energy = Energy()
    # constraints system
    constraints = Constraints()

    tasks = Tasks()
    loop_det = LoopDetector()

    energy_text_id = create_energy_display(canvas, canvas_w, canvas_h)
    update_energy_display(canvas, energy_text_id, energy.current, energy.max)

    # Draw items on the grid
    draw_items(canvas, tasks.items, origin)

    # Create robot at center
    robot = Robot(canvas, origin, "robot.png")
    robot.x, robot.y = 0, 0
    robot.update_position()

    def move_forward():
        if not constraints.is_valid(CMD_FORWARD):
            log_message(text_output, "Cannot go forward! You just went backward.")
            return
        if energy.can_execute(CMD_FORWARD):
            if robot.move(CMD_FORWARD):
                loop_det.update(CMD_FORWARD)
                constraints.update(CMD_FORWARD)
                energy.consume(CMD_FORWARD)
                update_energy_display(canvas, energy_text_id, energy.current, energy.max)
                log_message(text_output, "Moved forward!")
            else:
                log_message(text_output, "Can't move forward! Wall ahead.")
        else:
            log_message(text_output, "Not enough energy!")

    def move_backward():
        if not constraints.is_valid(CMD_BACK):
            log_message(text_output, "Cannot go backward! You just went forward.")
            return
        if energy.can_execute(CMD_BACK):
            if robot.move(CMD_BACK):
                loop_det.update(CMD_BACK)
                constraints.update(CMD_BACK)
                energy.consume(CMD_BACK)
                update_energy_display(canvas, energy_text_id, energy.current, energy.max)
                log_message(text_output, "Moved backward!")
            else:
                log_message(text_output, "Can't move backward! Wall behind.")
        else:
            log_message(text_output, "Not enough energy!")

    def rotate_left():
        if not constraints.is_valid(CMD_LEFT):
            log_message(text_output, "Cannot turn left twice in a row!")
            return
        if energy.can_execute(CMD_LEFT):
            robot.rotate_left()
            loop_det.update(CMD_LEFT)
            constraints.update(CMD_LEFT)
            energy.consume(CMD_LEFT)
            update_energy_display(canvas, energy_text_id, energy.current, energy.max)
            log_message(text_output, "Rotated left!")
        else:
            log_message(text_output, "Not enough energy!")

    def rotate_right():
        if not constraints.is_valid(CMD_RIGHT):
            log_message(text_output, "Cannot turn right twice in a row!")
            return
        if energy.can_execute(CMD_RIGHT):
            robot.rotate_right()
            loop_det.update(CMD_RIGHT)
            constraints.update(CMD_RIGHT)
            energy.consume(CMD_RIGHT)
            update_energy_display(canvas, energy_text_id, energy.current, energy.max)
            log_message(text_output, "Rotated right!")
        else:
            log_message(text_output, "Not enough energy!")

    def do_pick():
        item = tasks.pick(robot.x, robot.y)
        if item is None:
            if tasks.is_holding:
                log_message(text_output, "Already holding! Drop first.")
            else:
                log_message(text_output, "No item here! Move to a ★ cell.")
            return
        remove_item_from_canvas(canvas, item["canvas_id"])
        loop_det.update(CMD_PICK)
        log_message(text_output, f"Picked up item! Tasks done: {tasks.pick_drop_count}/3")

    def do_drop():
        if not tasks.can_drop():
            log_message(text_output, "Nothing to drop! Pick first.")
            return
        tasks.drop()
        loop_det.update(CMD_DROP)
        remaining = max(0, 3 - tasks.pick_drop_count)
        if remaining == 0:
            log_message(text_output, "Dropped! All tasks done. You can now STOP.")
        else:
            log_message(text_output, f"Dropped! {remaining} more task(s) needed.")

    def do_stop():
        if not loop_det.has_ccw_loop():
            log_message(text_output, "Need 1 CCW loop first! (F L F L F L F L)")
        elif not tasks.can_stop():
            remaining = 3 - tasks.pick_drop_count
            log_message(text_output, f"Need {remaining} more pick-drop task(s).")
        else:
            log_message(text_output, "STOPPED! All rules satisfied. Well done!")
            _show_start()

    def recharge():
        if energy.consume(CMD_RECHARGE):
            update_energy_display(canvas, energy_text_id, energy.current, energy.max)
            log_message(text_output, "Recharged! Energy: 5/5")
        else:
            log_message(text_output, "Can only recharge when energy = 0")

    def reset_energy():
        energy.reset()
        constraints.reset()
        tasks.reset()
        loop_det.reset()
        robot.x, robot.y = 0, 0
        robot.direction_index = 0
        robot.update_position()
        robot._update_image()
        update_energy_display(canvas, energy_text_id, energy.current, energy.max)
        draw_items(canvas, tasks.items, origin)
        log_message(text_output, "Reset! Press START to begin again.")
        _show_start()

    # ── button frame ────────────────────────────────────────────────────────
    btn_frame = tk.Frame(root, bg="#1a1a2e")
    btn_frame.pack(pady=(0, 12))

    BTN_STYLE = dict(
        bg="#16213e", fg="#64ffda",
        activebackground="#0f3460", activeforeground="#e94560",
        font=("Courier New", 10, "bold"),
        relief="flat", bd=0, padx=10, pady=6, cursor="hand2"
    )
    START_STYLE = dict(
        bg="#e94560", fg="#ffffff",
        activebackground="#c73652", activeforeground="#ffffff",
        font=("Courier New", 11, "bold"),
        relief="flat", bd=0, padx=18, pady=8, cursor="hand2"
    )

    def _show_start():
        for w in action_widgets:
            w.pack_forget()
        btn_start.pack(in_=btn_frame, side="left", padx=4)

    def _show_actions():
        btn_start.pack_forget()
        for w in action_widgets:
            w.pack(in_=btn_frame, side="left", padx=3)

    def do_start():
        _show_actions()
        log_message(text_output, "Robot Navigation Simulator initialized!")

    btn_start = tk.Button(btn_frame, text="▶  START", command=do_start, **START_STYLE)

    action_widgets = [
        tk.Button(btn_frame, text="Forward",      command=move_forward,  **BTN_STYLE),
        tk.Button(btn_frame, text="Backward",     command=move_backward, **BTN_STYLE),
        tk.Button(btn_frame, text="Rotate Left",  command=rotate_left,   **BTN_STYLE),
        tk.Button(btn_frame, text="Rotate Right", command=rotate_right,  **BTN_STYLE),
        tk.Button(btn_frame, text="Recharge",     command=recharge,      **BTN_STYLE),
        tk.Button(btn_frame, text="Pick",         command=do_pick,       **BTN_STYLE),
        tk.Button(btn_frame, text="Drop",         command=do_drop,       **BTN_STYLE),
        tk.Button(btn_frame, text="Stop",         command=do_stop,
                  bg="#e94560", fg="#ffffff",
                  activebackground="#c73652", activeforeground="#ffffff",
                  font=("Courier New", 10, "bold"),
                  relief="flat", bd=0, padx=10, pady=6, cursor="hand2"),
        tk.Button(btn_frame, text="Reset",        command=reset_energy,
                  bg="#555577", fg="#ffffff",
                  activebackground="#333355", activeforeground="#ffffff",
                  font=("Courier New", 10, "bold"),
                  relief="flat", bd=0, padx=10, pady=6, cursor="hand2"),
    ]

    # Boot into Start-only view
    _show_start()

    root.mainloop()


if __name__ == "__main__":
    main()