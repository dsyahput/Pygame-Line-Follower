from enum import Enum, auto

# --- Definisi State ---
class State(Enum):
    FORWARD = auto()
    TURN_LEFT = auto()
    TURN_RIGHT = auto()

# --- Definisi Event ---
class Event(Enum):
    LEFT_ON_LINE = auto()
    RIGHT_ON_LINE = auto()
    BOTH_ON_LINE = auto()
    NONE_ON_LINE = auto()

# --- Transition Function ---
def transition(current_state, event):
    if event == Event.BOTH_ON_LINE:
        return State.FORWARD
    elif event == Event.LEFT_ON_LINE:
        return State.TURN_LEFT
    elif event == Event.RIGHT_ON_LINE:
        return State.TURN_RIGHT
    elif event == Event.NONE_ON_LINE:
        return State.FORWARD
    return current_state
