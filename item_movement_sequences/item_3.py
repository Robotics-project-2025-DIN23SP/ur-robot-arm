from ur_arm.ur_arm_actions import *

def get_sequence(gr):
    return [
        (1, "Open Gripper", lambda: gr.execute_gripper_script("open_gripper.script", call_function="gripper_open")),
        (2, "Move to Default Position", lambda: move_to("default_position")),
        (3, "Move to Position (Approach)", lambda: move_to("position_approach_item_3", 4)),
        (4, "Move to Position (Grasp)", lambda: move_to("position_grasp_item_3", 3, "movel")),
        (5, "Close Gripper", lambda: gr.execute_gripper_script("close_gripper.script", call_function="gripper_close")),
        (6, "Move to Default Position via Approach Position", lambda: move_to("position_approach_item_3", 5, "movec", target="default_position")),
        (7, "Move to GoPiGo High Position", lambda: move_to("position_gopigo_high")),
        (8, "Move to GoPiGo Low Position", lambda: move_to("position_gopigo_low", 1, "movel")),
        (9, "Open Gripper", lambda: gr.execute_gripper_script("open_gripper.script", call_function="gripper_open")),
        (10, "Move to Default Position via GoPiGo High Position", lambda: move_to("position_gopigo_high", 5, "movec", target="default_position")),
    ]