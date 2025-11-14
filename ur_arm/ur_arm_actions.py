import time
from .ur_arm_connection import send_urscript
from .ur_arm_movement_scripts import generate_movej_script, generate_movel_script, generate_movec_script
from .ur_arm_config import *

POSITIONS = {
    "default_position": DEFAULT_POSITION,

    # positions above the GoPiGo
    "position_gopigo_low": POSITION_GOPIGO_LOW,
    "position_gopigo_high": POSITION_GOPIGO_HIGH,

    # positions for item 1
    "position_approach_item_1": POSITION_APPROACH_ITEM_1,
    "position_grasp_item_1": POSITION_GRASP_ITEM_1,

    # positions for item 3
    "position_approach_item_3": POSITION_APPROACH_ITEM_3,
    "position_grasp_item_3": POSITION_GRASP_ITEM_3,
}

MOVE_GENERATORS = {
    "movej": generate_movej_script,
    "movel": generate_movel_script,
    "movec": generate_movec_script
}

def move_to(
        name: str, 
        sleep_time: float = 5.0, 
        move_type: str = "movej", 
        target: str = None, 
        accel: float = 0.30, 
        vel: float = 0.45,
        final_decel: float = 2.0
    ):
    """
    Generic move function using a name from the POSITIONS dict.
    Args:
        name: The name of the position from the POSITIONS dict. In case of movec, the name of via pose.
        sleep_time: Seconds to wait after the movement completes.
        move_type: Type of movement command.
        target: Optional target position name for movec movement command
        accel: Acceleration for joint moves (rad/s^2)
        vel: Velocity for joint moves (rad/s)
        final_decel: Deceleration for movec movements
    """
    if move_type in ("movej", "movel"):
        pose = POSITIONS.get(name)
        if pose is None:
            raise ValueError(f"Unknown position: {name}")
        generator = MOVE_GENERATORS.get(move_type)
        script = generator(pose, name, accel=accel, vel=vel)

    elif move_type == "movec":
        if target is None:
            raise ValueError("movec requires a target position name")
        via_pose = POSITIONS.get(name)
        target_pose = POSITIONS.get(target)
        if via_pose is None or target_pose is None:
            raise ValueError(f"Unknown position(s) for movec: {name}, {target}")
        script = generate_movec_script(via_pose, target_pose, name, accel=accel, vel=vel, final_decel=final_decel)
    else:
        raise ValueError(f"Invalid move_type '{move_type}'")
    
    send_urscript(script)
    time.sleep(sleep_time) 