# tasks.py
# Pick/Drop task management
# Rules:
# - cannot pick twice without dropping first
# - cannot drop before picking
# - at least 3 complete pick-drop tasks must be done before STOP
# - pick only succeeds when the robot is standing on an item cell

from shared import CMD_PICK, CMD_DROP

MIN_TASKS = 3  # minimum pick-drop pairs required before STOP

ITEM_POSITIONS = [{"x": 1, "y": 6}, {"x": 5, "y": 2}, {"x": 6, "y": 6}]  # three fixed spawn points


class Tasks:
    def __init__(self):
        self.is_holding = False       # True = currently holding an item
        self.pick_drop_count = 0      # number of completed pick-drop pairs
        self.total_picked = 0         # lifetime pickup count, for HUD display
        self.items = [dict(pos) for pos in ITEM_POSITIONS]  # copy so reset works

    # ----- validation -----

    def can_pick(self) -> bool:
        """Pick is only valid when NOT already holding an item."""
        return not self.is_holding

    def can_drop(self) -> bool:
        """Drop is only valid when holding an item."""
        return self.is_holding

    def can_stop(self) -> bool:
        """STOP requires at least MIN_TASKS completed pick-drop pairs."""
        return self.pick_drop_count >= MIN_TASKS

    # ----- state updates -----

    def pick(self, robot_x: int, robot_y: int) -> dict | None:
        """
        Attempt to pick up an item at (robot_x, robot_y).
        Returns the matched item dict (which contains canvas_id) on success,
        or None if already holding or no item at the robot's position.
        """
        if not self.can_pick():
            return None
        for item in self.items:
            if item["x"] == robot_x and item["y"] == robot_y:
                self.is_holding = True
                self.items.remove(item)
                self.total_picked += 1
                return item
        return None  # not standing on an item

    def drop(self, robot_x: int, robot_y: int) -> dict | None:
        """
        Execute a drop at (robot_x, robot_y).
        Returns the new item dict (no canvas_id yet) on success,
        or None if not holding anything, or if a star already exists
        at this exact cell (prevents drawing a duplicate sprite).
        Increments the completed task counter on success either way.
        """
        if not self.can_drop():
            return None
        self.is_holding = False
        self.pick_drop_count += 1

        # avoid stacking two stars on the same cell
        for existing in self.items:
            if existing["x"] == robot_x and existing["y"] == robot_y:
                return None  # cell already has a star; don't draw a duplicate

        new_item = {"x": robot_x, "y": robot_y}
        self.items.append(new_item)
        return new_item

    def reset(self):
        """Reset to initial state and restore all items."""
        self.is_holding = False
        self.pick_drop_count = 0
        self.total_picked = 0
        self.items = [dict(pos) for pos in ITEM_POSITIONS]

    # ----- status -----

    def get_status(self) -> dict:
        return {
            "is_holding": self.is_holding,
            "pick_drop_count": self.pick_drop_count,
            "can_stop": self.can_stop(),
            "tasks_remaining": max(0, MIN_TASKS - self.pick_drop_count),
        }