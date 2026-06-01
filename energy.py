# Energy system for robot
# Movement and turn consume energy
# Recharge only when energy = 0

from shared import (CMD_FORWARD, CMD_BACK, CMD_LEFT, CMD_RIGHT,
                    CMD_RECHARGE, MAX_ENERGY)

# Energy cost per command
ENERGY_COSTS = {
    CMD_FORWARD: 1,
    CMD_BACK: 1,
    CMD_LEFT: 1,    # turning also consumes energy
    CMD_RIGHT: 1,
    CMD_RECHARGE: 0,  # recharge gives energy, doesn't cost it
}

class Energy:
    def __init__(self, initial_energy=MAX_ENERGY):
        self.current = initial_energy
        self.max = MAX_ENERGY

    def can_execute(self, command: str) -> bool:
        """Check if robot has enough energy for command"""
        cost = ENERGY_COSTS.get(command, 0)
        return self.current >= cost

    def consume(self, command: str) -> bool:
        """Consume energy for command. Return True if successful"""
        if command == CMD_RECHARGE:
            # Recharge only works when energy = 0
            if self.current == 0:
                self.current = self.max
                return True
            return False
        
        if self.can_execute(command):
            cost = ENERGY_COSTS.get(command, 0)
            self.current -= cost
            return True
        return False

    def is_dead(self) -> bool:
        """Check if energy is 0 and cannot execute"""
        return self.current == 0

    def reset(self):
        """Reset energy to max"""
        self.current = self.max

    def get_status(self) -> dict:
        """Get energy status"""
        return {
            "current": self.current,
            "max": self.max,
            "is_dead": self.is_dead()
        }