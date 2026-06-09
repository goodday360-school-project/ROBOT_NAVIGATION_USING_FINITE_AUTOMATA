# tasks.py
# Pick/Drop task management
# Rules:
# - cannot pick twice without dropping first
# - cannot drop before picking
# - at least 2 complete pick-drop tasks must be done before STOP
# - pick only succeeds when the robot is standing on an item cell

from shared import CMD_PICK, CMD_DROP

MIN_TASKS = 3  # minimum pick-drop pairs required before STOP

ITEM_POSITIONS = [{"x": 1, "y": 6}, {"x": 5, "y": 2}, {"x": 6, "y": 6}]  # two fixed spawn points


class Tasks:
    def __init__(self):
        self.is_holding = False       # True = currently holding an item
        self.pick_drop_count = 0      # number of completed pick-drop pairs
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
                return item
        return None  # not standing on an item

    def drop(self) -> bool:
        """
        Execute a drop.
        Returns True if successful, False if not holding anything.
        Increments the completed task counter on success.
        """
        if not self.can_drop():
            return False
        self.is_holding = False
        self.pick_drop_count += 1
        return True

    def reset(self):
        """Reset to initial state and restore all items."""
        self.is_holding = False
        self.pick_drop_count = 0
        self.items = [dict(pos) for pos in ITEM_POSITIONS]

    # ----- status -----

    def get_status(self) -> dict:
        return {
            "is_holding": self.is_holding,
            "pick_drop_count": self.pick_drop_count,
            "can_stop": self.can_stop(),
            "tasks_remaining": max(0, MIN_TASKS - self.pick_drop_count),
        }