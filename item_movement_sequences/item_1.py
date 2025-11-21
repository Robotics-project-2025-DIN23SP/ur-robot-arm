from ur_arm.ur_arm_actions import *

def get_sequence(gr):
    return [
        (1, "Open Gripper", lambda: gr.execute_gripper_script("open_gripper.script", call_function="gripper_open")),
        (2, "Move to Default Position (Lift/Transfer)", lambda: move_to("default_position")),
        (3, "Move to Position 1 (Approach)", lambda: move_to("position_approach_item_1", 4)),
        (4, "Move to Position 2 (Grasp)", lambda: move_to("position_grasp_item_1", 3, "movel")),
        (5, "Close Gripper", lambda: gr.execute_gripper_script("close_gripper.script", call_function="gripper_close")),
        (6, "Move to Position 1 (Approach)", lambda: move_to("position_approach_item_1", 4)),
        (7, "Move to Default Position (Lift/Transfer)", lambda: move_to("default_position")),
        (9, "Move to GoPiGo High Position", lambda: move_to("position_gopigo_high", 4)),
        (8, "Move to GoPiGo Low Position", lambda: move_to("position_gopigo_low", 4)),
        (10, "Open Gripper", lambda: gr.execute_gripper_script("open_gripper.script", call_function="gripper_open")),
        (11, "Move to GoPiGo High Position", lambda: move_to("position_gopigo_high", 4)),
        (12, "Move to Default Position (Lift/Transfer)", lambda: move_to("default_position")),
    ]