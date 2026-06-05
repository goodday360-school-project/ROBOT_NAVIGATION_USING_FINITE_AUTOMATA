# tasks.py
# Pick/Drop task management
# Rules:
# - cannot pick twice without droping first
# - cannot drop before picking
# - at least 2 complete pick-drop tasks must be done before STOP

from shared import CMD_PICK, CMD_DROP

MIN_TAKS = 2 # minimum pick-drop pairs required before STOP


class Tasks:
    def __init__(self):
        self.is_holding = False # True = currently holding an item
        self.pick_drop_count = 0 # number of completed pick-drop pairs


# ----- validation -----

    def can_pick(self) -> bool:
        """Pick is only valid when NOT alredy holding an item."""
        return not self.is_holding
    
    def can_drop(self) -> bool:
        """Drop is only valid when holding an item."""
        return self.is_holding
    
    def can_stop(self) -> bool:
        """STOP requires at least MIN_TASKS completed pick-drop pairs."""
        return self.pick_drop_count >= MIN_TAKS
    
# ----- state updates -----

    def pick(self) -> bool:
        """Execute a pick. 
            Returns True if successful, False if already holding."""
        if not self.can_pick():
            return False
        self.is_holding = True
        return True
    
    def drop(self) -> bool:
        """Execute a drop. 
            Returns True if successful, False if not holding anything.
            Increments the completed task counter on success."""
        
        if not self.can_drop():
            return False
        self.is_holding = False
        self.pick_drop_count += 1
        return True
    
    def reset(self):
        """Reset to initial state."""
        self.is_holding = False
        self.pick_drop_count = 0


# ----- status -----
    def get_status(self) -> dict:
        return{
            "is_holding": self.is_holding,
            "pick_drop_count": self.pick_drop_count,
            "can_stop": self.can_stop(),
            "tasks_remaining": max(0, MIN_TAKS - self.pick_drop_count),
        }