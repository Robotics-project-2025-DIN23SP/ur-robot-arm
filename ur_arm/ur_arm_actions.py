import time
from .ur_arm_connection import send_dashboard_command, send_urscript
from .ur_arm_movement_scripts import generate_movej_script
from .ur_arm_config import *

POSITIONS = {
    "default_position": DEFAULT_POSITION,
    "position_1": POSITION_1,
    "position_2": POSITION_2,
    "position_approach_item_3": POSITION_APPROACH_ITEM_3,
    "position_grasp_item_3": POSITION_GRASP_ITEM_3,
    "position_gopigo_low": POSITION_GOPIGO_LOW,
    "position_gopigo_high": POSITION_GOPIGO_HIGH,
}

def move_to(name: str, sleep_time: float = 5.0):
    """Generic move function using a name from the POSITIONS dict."""
    pose = POSITIONS.get(name)
    if pose is None:
        raise ValueError(f"Unknown position: {name}")
    script = generate_movej_script(pose, name)
    send_urscript(script)
    time.sleep(sleep_time) 