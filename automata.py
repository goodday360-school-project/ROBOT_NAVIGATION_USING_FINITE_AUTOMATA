# automata
# DFA and transition table
# for the robot command language
# must begin with "start" and end with "stop"
# at least one movement before stop
# pick before drop, no double-pick
# recharge is always syntactically allowed
# runtime use energy
# L/R are handled in constraints.py

from shared import (CMD_START, CMD_STOP, CMD_FORWARD,
                    CMD_BACK, CMD_LEFT, CMD_RIGHT,
                    CMD_PICK, CMD_DROP, CMD_RECHARGE,
                    ALPHABET, ENERGY_COSTS)

# states
S_INIT = "INIT" #before start
S_STARTED = "STARTED" #after start, before stop
S_MOVED = "MOVED" #after at least one movement
S_PICKED = "PICKED" #after pick, before drop
S_DROPPED = "DROPPED" #after drop
S_DEAD = "DEAD" #after energy runs out

# states where stop is legal
accept_states = {S_MOVED, S_DROPPED}

# transition table that use dict inside dict
TRANSITION_TABLE: dict[str, dict[str, str]] = {
    S_INIT: {
        CMD_START: S_STARTED,  
    },
    S_STARTED: {
        CMD_FORWARD: S_MOVED,
        CMD_BACK: S_MOVED,
        CMD_LEFT: S_STARTED,  # left doesn't change state
        CMD_RIGHT: S_STARTED,  # right doesn't change state
        CMD_PICK: S_STARTED,  # pick doesn't change state
        CMD_DROP: S_STARTED,  # drop doesn't change state
        CMD_RECHARGE: S_STARTED,  # recharge doesn't change state
    },
    S_MOVED: {
        CMD_FORWARD: S_MOVED,
        CMD_BACK: S_MOVED,
        CMD_LEFT: S_MOVED,  # left doesn't change state
        CMD_RIGHT: S_MOVED,  # right doesn't change state
        CMD_PICK: S_PICKED,
        CMD_RECHARGE: S_MOVED,  # recharge doesn't change state
        CMD_STOP: S_MOVED,  # stop is legal here
    },
    S_PICKED: {
        CMD_FORWARD: S_PICKED,  # movement doesn't change state
        CMD_BACK: S_PICKED,  # movement doesn't change state
        CMD_LEFT: S_PICKED,  # left doesn't change state
        CMD_RIGHT: S_PICKED,  # right doesn't change state
        CMD_DROP: S_DROPPED,
    },
    S_DROPPED: {
        CMD_FORWARD: S_DROPPED,  # movement doesn't change state
        CMD_BACK: S_DROPPED,  # movement doesn't change state
        CMD_LEFT: S_DROPPED,  # left doesn't change state
        CMD_RIGHT: S_DROPPED,  # right doesn't change state
        CMD_PICK: S_PICKED,
        CMD_RECHARGE: S_DROPPED,  # recharge doesn't change state
        CMD_STOP: S_DROPPED,  # stop is legal here
    },
    S_DEAD: {},
}

class DFA:
    def __init__(self):
        self.state = S_INIT
    def reset(self):
        self.state = S_INIT

    def step(self, command: str) -> str:
        if command not in ALPHABET:
            self.state = S_DEAD
            return self.state
        
        next_state = TRANSITION_TABLE.get(self.state, {}).get(command, S_DEAD)
        if command == CMD_STOP and self.state not in accept_states:
            next_state = S_DEAD
        
        self.state = next_state  #  Always assign state
        return self.state
        
    def is_alive(self) -> bool:
        return self.state != S_DEAD
    def can_stop(self) -> bool:
        return self.state in accept_states