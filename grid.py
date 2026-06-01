import tkinter as tk

CELL_SIZE = 70
GRID_SIZE = 8
PADDING = 20
AXIS_OFFSET = 30

BG_COLOR = "#1a1a2e"
CELL_EVEN = "#1e2a45"
CELL_ODD = "#16213e"
BORDER_COLOR = "#e94560"
LABEL_COLOR = "#a8b2d8"
COORD_COLOR = "#64ffda"


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


def init_canvas(root):
    canvas_w = GRID_SIZE * CELL_SIZE + AXIS_OFFSET + PADDING * 2
    canvas_h = GRID_SIZE * CELL_SIZE + AXIS_OFFSET + PADDING * 2
    canvas = tk.Canvas(root, width=canvas_w, height=canvas_h, bg=BG_COLOR, highlightthickness=0)
    canvas.pack(padx=PADDING, pady=PADDING)
    return canvas, (PADDING + AXIS_OFFSET, PADDING)
