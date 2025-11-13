import time
from .ur_arm_connection import send_dashboard_command, send_urscript
from .ur_arm_movement_scripts import generate_movej_script
from .ur_arm_config import *

# initialize robot
def initialize_robot():
    """Powers on, releases brakes, and starts the program."""
    print("\n--- Initializing Robot ---")
    send_dashboard_command("power on")
    time.sleep(2)
    send_dashboard_command("brake release")
    time.sleep(2)
    send_dashboard_command("unlock protective stop")
    time.sleep(1)
    send_dashboard_command("play") 
    print("--------------------------\n")

# start/end position
def move_to_default_position():
    """Moves the arm to the defined safe DEFAULT_POSITION."""
    script = generate_movej_script(DEFAULT_POSITION, "default_position")
    send_urscript(script)
    time.sleep(5) 

# positions for item_1
def move_to_position_1():
    """Moves the arm to the defined POSITION_1_POSE."""
    script = generate_movej_script(POSITION_1_POSE, "position_1")
    send_urscript(script)
    time.sleep(5) 

def move_to_position_2():
    """Moves the arm to the defined POSITION_2_POSE."""
    script = generate_movej_script(POSITION_2_POSE, "position_2")
    send_urscript(script)
    time.sleep(5) 

# positions above the GoPiGo
def move_to_gopigo_low_position():
    """Moves the arm to the defined safe POSITION_GOPIGO_LOW_POSE."""
    script = generate_movej_script(POSITION_GOPIGO_LOW_POSE, "position_gopigo_low_pose")
    send_urscript(script)
    time.sleep(5) 

def move_to_gopigo_high_position():
    """Moves the arm to the defined safe POSITION_GOPIGO_HIGH_POSE."""
    script = generate_movej_script(POSITION_GOPIGO_HIGH_POSE, "position_gopigo_high_pose")
    send_urscript(script)
    time.sleep(5) 

# positions for item_3
def move_to_approach_item_3_position():
    """Moves the arm to the defined safe POSITION_APPROACH_ITEM_3."""
    script = generate_movej_script(POSITION_APPROACH_ITEM_3, "position_approach_item_3")
    send_urscript(script)
    time.sleep(5) 

def move_to_grasp_item_3_position():
    """Moves the arm to the defined safe POSITION_GRASP_ITEM_3."""
    script = generate_movej_script(POSITION_GRASP_ITEM_3, "position_grasp_item_3")
    send_urscript(script)
    time.sleep(5) 