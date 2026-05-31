# this file shares the command definitions
# track the robot state

# commands
CMD_START = "start"
CMD_STOP = "stop"
CMD_FORWARD = "forward"
CMD_BACK = "back"
CMD_LEFT = "left"
CMD_RIGHT = "right"
CMD_PICK = "pick"
CMD_DROP = "drop"
CMD_RECHARGE = "recharge"

# alphabet 
ALPHABET = {CMD_START, CMD_STOP, CMD_FORWARD, CMD_BACK,
            CMD_LEFT, CMD_RIGHT, CMD_PICK, CMD_DROP, CMD_RECHARGE}

MOVEMENT_CMD = {CMD_FORWARD, CMD_BACK}
TURN_CMD = {CMD_LEFT, CMD_RIGHT}

# grid and constants
GRID_SIZE = 8 # 8x8 grid
MAX_ENERGY = 5
START_X = 0
START_Y = 0
START_DIR = "N"

# order matters for turning
DIRECTIONS = ["N", "E", "S", "W"] 

# robot state
def make_robot() -> dict:
    return {
        "x": START_X,
        "y": START_Y,
        "dir": START_DIR,
        "energy": MAX_ENERGY,
        "holding": False,
        "left_turns": 0,
        "right_turns": 0,
        "pick_drop_count": 0,
        "last_movement": None,
        "last_turn": None,

        # numbers of COUNTERCLOCKWISE and CLOCKWISE loops completed
        "ccw_loop_count": 0,
        "cw_loop_count": 0,
    }