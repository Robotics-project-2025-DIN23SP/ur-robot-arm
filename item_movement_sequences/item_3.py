from ur_arm.ur_arm_actions import *

def get_sequence(gr):
    return [
        (1, "Open Gripper", lambda: gr.execute_gripper_script("open_gripper.script", call_function="gripper_open")),
        (2, "Move to Default Position", move_to_default_position),
        (3, "Move to Position (Approach)", move_to_approach_item_3_position),
        (4, "Move to Position (Grasp)", move_to_grasp_item_3_position),
        (5, "Close Gripper", lambda: gr.execute_gripper_script("close_gripper.script", call_function="gripper_close")),
        (3, "Move to Position (Approach)", move_to_approach_item_3_position),
        (7, "Move to Default Position", move_to_default_position),
        (8, "Move to GoPiGo Low Position", move_to_gopigo_low_position),
        (9, "Open Gripper", lambda: gr.execute_gripper_script("open_gripper.script", call_function="gripper_open")),
        (8, "Move to GoPiGo High Position", move_to_gopigo_high_position),
        (9, "Move to Default Position", move_to_default_position),
    ]