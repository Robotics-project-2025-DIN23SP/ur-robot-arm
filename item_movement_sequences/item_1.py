import ur_arm_controller

def get_sequence(gr):
    return [
        (1, "Open Gripper", lambda: gr.execute_gripper_script("open_gripper.script", call_function="gripper_open")),
        (2, "Move to Default Position (Lift/Transfer)", ur_arm_controller.move_to_default_position),
        (3, "Move to Position 1 (Approach)", ur_arm_controller.move_to_position_1),
        (4, "Move to Position 2 (Grasp)", ur_arm_controller.move_to_position_2),
        (5, "Close Gripper", lambda: gr.execute_gripper_script("close_gripper.script", call_function="gripper_close")),
        (6, "Move to Position 1 (Approach)", ur_arm_controller.move_to_position_1),
        (7, "Move to Default Position (Lift/Transfer)", ur_arm_controller.move_to_default_position),
        (8, "Move to GoPiGo Low Position", ur_arm_controller.move_to_gopigo_low_position),
        (9, "Open Gripper", lambda: gr.execute_gripper_script("open_gripper.script", call_function="gripper_open")),
        (8, "Move to GoPiGo High Position", ur_arm_controller.move_to_gopigo_high_position),
        (9, "Move to Default Position (Lift/Transfer)", ur_arm_controller.move_to_default_position),
    ]