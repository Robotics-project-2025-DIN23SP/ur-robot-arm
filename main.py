from gripper.gripper import URGripperController
import importlib

def run_custom_sequence():
    """
    Executes the 12-step sequence by connecting the robot arm and gripper,
    initializing the gripper, and iterating through a defined list of actions.
    """
    try:
        # --- Safety Check and Initialization ---
        input("\n--- Initialization Sequence ---\n"
            "1. Ensure E-STOP is released and protective stop is cleared.\n"
            "2. Ensure robot is in Remote Control mode.\n"
            "3. Press **ENTER** to start initialization (Power On, Gripper Setup).\n")

        # Create instance of gripper and connect to gripper
        gr = URGripperController()
        gr.connect()
        
        # Init gripper (only run once when starting coding)
        gr.execute_gripper_script("init_gripper.script", call_function="init_gripper")
        
        # Choose which sequence to run
        sequence_name = input("Enter sequence to run (item_1, item_2, item_3, item_4): ").strip()
        module_name = f"item_movement_sequences.{sequence_name}"

        try:
            sequence_module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            print(f"Sequence '{sequence_name}' not found.")
            return
        
        print("\n--- Initialization Complete. Starting 12-Step Robot Sequence ---\n")
        
        sequence_steps = sequence_module.get_sequence(gr)
        
        # Execute each step in the sequence
        for step_num, description, action_func in sequence_steps:
            print(f"**[Step {step_num}]** {description}...")
            action_func() 
            print(f"Step {step_num} complete.\n")
            
        print("\n*** Full Sequence Complete. ***")

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        gr.disconnect()


if __name__ == "__main__":
    run_custom_sequence()