# Constraint validation for robot commands
# Rules:
# - No LL or RR (no two consecutive identical turns)
# - No FB or BF (no immediate reverse movement)
# - Detect invalid command patterns

from shared import (CMD_START, CMD_STOP, CMD_FORWARD,
                    CMD_BACK, CMD_LEFT, CMD_RIGHT,
                    CMD_PICK, CMD_DROP, CMD_RECHARGE,
                    ALPHABET)  

class Constraints:
    def __init__(self):
        self.last_movement = None  # track last movement (forward/back)
        self.last_turn = None      # track last turn (left/right)
        self.left_turns = 0        # count left turns
        self.right_turns = 0       # count right turns

    def is_valid(self, command: str) -> bool:
        """Check if command violates constraints"""
        
        # Check reverse movement (FB or BF)
        if command in [CMD_FORWARD, CMD_BACK]:
            if self.last_movement:
                if (self.last_movement == CMD_FORWARD and command == CMD_BACK) or \
                   (self.last_movement == CMD_BACK and command == CMD_FORWARD):
                    return False
        
        # Check consecutive identical turns (LL or RR only)
        if command == CMD_LEFT:
            if self.last_turn == CMD_LEFT:
                return False
        elif command == CMD_RIGHT:
            if self.last_turn == CMD_RIGHT:
                return False
        
        return True

    def update(self, command: str):
        """Update constraint tracking after valid command"""
        if command in [CMD_FORWARD, CMD_BACK]:
            self.last_movement = command
        
        if command in [CMD_LEFT, CMD_RIGHT]:
            self.last_turn = command
            if command == CMD_LEFT:
                self.left_turns += 1
            elif command == CMD_RIGHT:
                self.right_turns += 1

    def reset(self):
        """Reset all constraints"""
        self.last_movement = None
        self.last_turn = None
        self.left_turns = 0
        self.right_turns = 0

    def get_status(self) -> dict:
        """Get constraint status"""
        return {
            "last_movement": self.last_movement,
            "last_turn": self.last_turn,
            "left_turns": self.left_turns,
            "right_turns": self.right_turns
        }