# C:\Users\44745\Desktop\School Robot Arm\main.py

import ur_arm_controller 
from gripper import URGripperController

def run_custom_sequence():
    """
    Executes the 12-step sequence by connecting the robot arm and gripper,
    initializing the gripper, and iterating through a defined list of actions.
    """
    try:
        # --- Step 0: Safety Check and Initialization ---
        input("\n--- Initialization Sequence ---\n"
            "1. Ensure E-STOP is released and protective stop is cleared.\n"
            "2. Ensure robot is in Remote Control mode.\n"
            "3. Press **ENTER** to start initialization (Power On, Gripper Setup).\n")
        
        # TODO: is this part needed? I never ran this but for some reason everything still works
        # Initialize the UR Arm (Placeholder: Power on, play program, etc.)
        # ur_arm_controller.initialize_robot() 

        # Create instance of gripper and connect to gripper
        gr = URGripperController()
        gr.connect()
        
        # Init gripper (only run once when starting coding)
        # gr.execute_gripper_script("init_gripper.script", call_function="init_gripper")
        
        print("\n--- Initialization Complete. Starting 12-Step Robot Sequence ---\n")
        
        sequence_steps = [
            (1, "Open Gripper", lambda: gr.execute_gripper_script("open_gripper.script", call_function="gripper_open")),
            (2, "Move to Default Position (Lift/Transfer)", ur_arm_controller.move_to_default_position),
            (3, "Move to Position 1 (Approach)", ur_arm_controller.move_to_position_1),
            (4, "Move to Position 2 (Grasp)", ur_arm_controller.move_to_position_2),
            (5, "Close Gripper", lambda: gr.execute_gripper_script("close_gripper.script", call_function="gripper_close")),
            (6, "Move to Position 1 (Approach)", ur_arm_controller.move_to_position_1),
            (7, "Move to Default Position (Lift/Transfer)", ur_arm_controller.move_to_default_position),
            # (8, "Open Gripper", lambda: gr.execute_gripper_script("Gripper_Open.script")),
            # (9, "Close Gripper", lambda: gr.execute_gripper_script("Gripper_Close.script")),
            # (10, "Move to Position 3 (Approach Release)", ur_arm_controller.move_to_position_3),
            # (11, "Move to Position 4 (Clearance)", ur_arm_controller.move_to_position_4),
            # (12, "Move to Position 3 (Approach Release)", ur_arm_controller.move_to_position_3),
            # (13, "Move to Default Position (Home)", ur_arm_controller.move_to_default_position),
        ]

        # Execute each step in the sequence
        for step_num, description, action_func in sequence_steps:
            print(f"**[Step {step_num}]** {description}...")
            action_func() 
            print(f"Step {step_num} complete.\n")
            
        print("\n*** Full 12-Step Sequence Complete. ***")

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        gr.disconnect()


if __name__ == "__main__":
    run_custom_sequence()