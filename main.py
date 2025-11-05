# C:\Users\44745\Desktop\School Robot Arm\main.py

import ur_arm_controller # Assumed to contain move_to_position functions
import gripper # Assumed to contain the URGripperController class

def run_custom_sequence():
    """
    Executes the 12-step sequence by connecting the robot arm and gripper,
    initializing the gripper, and iterating through a defined list of actions.
    """
    
    # --- Step 0: Safety Check and Initialization ---
    input("\n--- Initialization Sequence ---\n"
          "1. Ensure E-STOP is released and protective stop is cleared.\n"
          "2. Ensure robot is in Remote Control mode.\n"
          "3. Press **ENTER** to start initialization (Power On, Gripper Setup).\n")
    
    # Initialize the UR Arm (Placeholder: Power on, play program, etc.)
    # NOTE: You'll need to implement this in ur_arm_controller.py
    # ur_arm_controller.initialize_robot() 
    
    # Create and connect the gripper controller
    gr = gripper.URGripperController()
    gr.connect()

    # Initialize the Gripper (Stream script, activate, etc.)
    # NOTE: "Gripper.script" must be in the same directory or have a valid path.
    # gr.initialize_gripper("Gripper.script")
    
    print("\n--- Initialization Complete. Starting 12-Step Robot Sequence ---\n")
    
    # Define the sequence of steps
    # NOTE: We pass the bound method reference (e.g., gr.open_gripper) 
    # and call it later (action_func()).
    # sequence_steps = [
    #     # (1, "Move to Default Position", ur_arm_controller.move_to_default_position),
    #     (1, "Open Gripper (Test)", gr.initialize_gripper("Gripper_Open.script")), 
    #     (2, "Open Gripper (Test)", gr.initialize_gripper("Gripper_Close.script")), 
    #     (4, "Open Gripper (Pre-Pick)", gr.open_gripper),
    #     (5, "Move to Position 1 (Approach)", ur_arm_controller.move_to_position_1),
    #     (6, "Move to Position 2 (Grasp)", ur_arm_controller.move_to_position_2),
    #     (7, "Close Gripper (Grab)", gr.close_gripper),
    #     (8, "Move to Default Position (Lift/Transfer)", ur_arm_controller.move_to_default_position),
    #     (9, "Move to Position 3 (Approach Release)", ur_arm_controller.move_to_position_3),
    #    
    #     (11, "Move to Position 4 (Clearance)", ur_arm_controller.move_to_position_4),
    #     (12, "Move to Default Position (Home)", ur_arm_controller.move_to_default_position),
    # ]
    sequence_steps = [
        # (1, "Move to Default Position (Lift/Transfer)", ur_arm_controller.move_to_default_position),
        # (2, "Move to Position 1 (Approach)", ur_arm_controller.move_to_position_1),
        # (3, "Move to Position 2 (Grasp)", ur_arm_controller.move_to_position_2),
        # (4, "Close Gripper", lambda: gr.execute_gripper_script("Gripper_Close.script")),
        # (5, "Move to Position 1 (Approach)", ur_arm_controller.move_to_position_1),
        # (6, "Move to Default Position (Lift/Transfer)", ur_arm_controller.move_to_default_position),
        (7, "Open Gripper", lambda: gr.execute_gripper_script("Gripper_Open.script")),
        # (4, "Close Gripper", lambda: gr.execute_gripper_script("Gripper_Close.script")),


        # (6, "Move to Position 3 (Approach Release)", ur_arm_controller.move_to_position_3),
        # (7, "Move to Position 4 (Clearance)", ur_arm_controller.move_to_position_4),
        # (8, "Move to Position 3 (Approach Release)", ur_arm_controller.move_to_position_3),
        # (9, "Move to Default Position (Home)", ur_arm_controller.move_to_default_position),
    ]

    # Execute each step in the sequence
    for step_num, description, action_func in sequence_steps:
        print(f"**[Step {step_num}]** {description}...")
        
        # Call the function reference. This executes the method/function.
        action_func() 
        
        print(f"Step {step_num} complete.\n")
        
    print("\n*** Full 12-Step Sequence Complete. ***")

    # Disconnect gripper safely
    gr.disconnect()


if __name__ == "__main__":
    try:
        run_custom_sequence()
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        # Optionally, try to disconnect the gripper even on failure
        try:
            gr.disconnect()
        except:
            pass # Ignore errors during cleanup