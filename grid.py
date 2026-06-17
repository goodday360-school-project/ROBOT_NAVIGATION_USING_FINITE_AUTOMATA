import tkinter as tk
from shared import CELL_SIZE, GRID_SIZE, PADDING, AXIS_OFFSET, BG_COLOR, CELL_EVEN, CELL_ODD, BORDER_COLOR, LABEL_COLOR, COORD_COLOR, ENERGY_COLOR, ITEM_COLOR


def create_grid(canvas):
    ox = PADDING + AXIS_OFFSET
    oy = PADDING

    # Row labels (y-axis, bottom to top)
    for row in range(GRID_SIZE):
        canvas.create_text(
            ox - 14, oy + (GRID_SIZE - 1 - row) * CELL_SIZE + CELL_SIZE // 2,
            text=str(row), fill=LABEL_COLOR, font=("Courier New", 11, "bold")
        )

    # Column labels (x-axis, left to right)
    for col in range(GRID_SIZE):
        canvas.create_text(
            ox + col * CELL_SIZE + CELL_SIZE // 2, oy + GRID_SIZE * CELL_SIZE + 16,
            text=str(col), fill=LABEL_COLOR, font=("Courier New", 11, "bold")
        )

    # Axis name labels
    canvas.create_text(
        ox - 26, oy + GRID_SIZE * CELL_SIZE // 2,
        text="y\n↑", fill=BORDER_COLOR, font=("Courier New", 10, "bold")
    )
    canvas.create_text(
        ox + GRID_SIZE * CELL_SIZE // 2, oy + GRID_SIZE * CELL_SIZE + 30,
        text="x →", fill=BORDER_COLOR, font=("Courier New", 10, "bold")
    )

    # Cells
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            actual_row = GRID_SIZE - 1 - row
            x1 = ox + col * CELL_SIZE
            y1 = oy + actual_row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            fill = CELL_EVEN if (row + col) % 2 == 0 else CELL_ODD
            canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=BORDER_COLOR, width=1)
            canvas.create_text(
                x1 + CELL_SIZE // 2, y1 + CELL_SIZE // 2,
                text=f"{col},{row}", fill=COORD_COLOR, font=("Courier New", 9)
            )


def create_energy_display(canvas, canvas_w, canvas_h):
    energy_text_id = canvas.create_text(
        canvas_w - PADDING - 35, PADDING - 12,
        text="Energy: 5/5", fill=ENERGY_COLOR, font=("Courier New", 12, "bold")
    )
    return energy_text_id


def update_energy_display(canvas, energy_text_id, current_energy, max_energy):
    canvas.itemconfig(energy_text_id, text=f"Energy: {current_energy}/{max_energy}")


def init_canvas(root):
    canvas_w = GRID_SIZE * CELL_SIZE + AXIS_OFFSET + PADDING * 2
    canvas_h = GRID_SIZE * CELL_SIZE + AXIS_OFFSET + PADDING * 2
    canvas = tk.Canvas(root, width=canvas_w, height=canvas_h, bg=BG_COLOR, highlightthickness=0)
    canvas.pack(padx=PADDING, pady=PADDING)
    return canvas, (PADDING + AXIS_OFFSET, PADDING), canvas_w, canvas_h


def create_text_display(root):
    message_label = tk.Label(
        root,
        text="",
        width=55,
        height=2,
        bg="#0f0f1e",
        fg="#00ff00",
        font=("Courier New", 10, "bold"),
        relief="solid",
        anchor="center",
        justify="center"
    )
    message_label.pack(pady=(20, 10))
    return message_label


def log_message(message_label, message):
    message_label.config(text=message)


def draw_items(canvas, items, origin):
    """Draw all items on the grid. Adds canvas_id to each item dict."""
    ox, oy = origin
    for item in items:
        x_pix = ox + item["x"] * CELL_SIZE + CELL_SIZE // 2
        y_pix = oy + (GRID_SIZE - 1 - item["y"]) * CELL_SIZE + CELL_SIZE // 2
        cid = canvas.create_text(
            x_pix, y_pix,
            text="★", fill=ITEM_COLOR,
            font=("Courier New", 22, "bold"),
            tags="item"
        )
        item["canvas_id"] = cid


def remove_item_from_canvas(canvas, canvas_id):
    """Remove a single item sprite from the canvas."""
    canvas.delete(canvas_id)


def flash_pickup(canvas, x, y, origin):
    """Show a brief green '+1' flash where an item was picked up."""
    ox, oy = origin
    x_pix = ox + x * CELL_SIZE + CELL_SIZE // 2
    y_pix = oy + (GRID_SIZE - 1 - y) * CELL_SIZE + CELL_SIZE // 2
    flash_id = canvas.create_text(
        x_pix, y_pix - 30,
        text="+1 ✓", fill="#00ff00",
        font=("Courier New", 14, "bold")
    )
    canvas.after(700, lambda: canvas.delete(flash_id))


def create_star_display(canvas, canvas_w, canvas_h):
    """Create a persistent 'Star x0' HUD counter, left of the energy display."""
    star_text_id = canvas.create_text(
        canvas_w - PADDING - 130, PADDING - 12,
        text="★ x0", fill=ITEM_COLOR, font=("Courier New", 12, "bold")
    )
    return star_text_id


def update_star_display(canvas, star_text_id, count):
    """Update the star HUD counter text."""
    canvas.itemconfig(star_text_id, text=f"★ x{count}")
