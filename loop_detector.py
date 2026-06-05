# loop_detector.py
# Detects counter-clockwise (CCW) and clockwise (CW) loops
#
# CCW loop pattern: forward left forward left forward left forward left
#   = (forward -> left) repeated 4 times
#   This turns the robot 360° counter-clockwise while moving forward each step.
#
# CW loop pattern:  forward right forward right forward right forward right
#   = (forward -> right) repeated 4 times
#
# Detection uses a sliding command buffer and checks for the exact 8-command
# pattern at the tail each time a relevant command is added.

from shared import CMD_FORWARD, CMD_LEFT, CMD_RIGHT

# The 8-command sequences to detect
CCW_PATTERN = [CMD_FORWARD, CMD_LEFT,
               CMD_FORWARD, CMD_LEFT,
               CMD_FORWARD, CMD_LEFT,
               CMD_FORWARD, CMD_LEFT]

CW_PATTERN  = [CMD_FORWARD, CMD_RIGHT,
               CMD_FORWARD, CMD_RIGHT,
               CMD_FORWARD, CMD_RIGHT,
               CMD_FORWARD, CMD_RIGHT]

PATTERN_LEN = 8   # both patterns are 8 commands long


class LoopDetector:
    def __init__(self):
        # Rolling buffer: only keep the last PATTERN_LEN relevant commands
        self._buffer: list[str] = []
        self.ccw_loop_count = 0
        self.cw_loop_count  = 0

    # ── public API ───────────────────────────────────────────────────────────

    def update(self, command: str):
        """
        Feed one command into the detector.
        Only forward/left/right commands participate in loop patterns;
        other commands (pick, drop, back, recharge…) break the sequence,
        so the buffer is cleared when they appear.
        """
        if command in (CMD_FORWARD, CMD_LEFT, CMD_RIGHT):
            self._buffer.append(command)
            # Keep buffer trimmed to exactly PATTERN_LEN
            if len(self._buffer) > PATTERN_LEN:
                self._buffer.pop(0)
            self._check_patterns()
        else:
            # Any non-loop command resets the streak
            self._buffer.clear()

    def has_ccw_loop(self) -> bool:
        """True if at least one CCW loop has been completed."""
        return self.ccw_loop_count > 0

    def has_cw_loop(self) -> bool:
        """True if at least one CW loop has been completed."""
        return self.cw_loop_count > 0

    def reset(self):
        """Reset detector state."""
        self._buffer.clear()
        self.ccw_loop_count = 0
        self.cw_loop_count  = 0

    def get_status(self) -> dict:
        return {
            "ccw_loop_count": self.ccw_loop_count,
            "cw_loop_count":  self.cw_loop_count,
            "has_ccw_loop":   self.has_ccw_loop(),
            "has_cw_loop":    self.has_cw_loop(),
            "buffer":         list(self._buffer),   # current streak (debug)
        }

    # ── internal ─────────────────────────────────────────────────────────────

    def _check_patterns(self):
        """
        Called after every relevant command.
        If the tail of the buffer matches a full pattern, count it
        and clear the buffer so the same commands don't double-count.
        """
        if len(self._buffer) == PATTERN_LEN:
            if self._buffer == CCW_PATTERN:
                self.ccw_loop_count += 1
                self._buffer.clear()
            elif self._buffer == CW_PATTERN:
                self.cw_loop_count  += 1
                self._buffer.clear()