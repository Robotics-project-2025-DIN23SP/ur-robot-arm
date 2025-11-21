from gripper.gripper import URGripperController
import importlib

def run_custom_sequence(sequence_name: str):
    """
    Executes a selected sequence of steps defined in item_movement_sequences
    Args:
        sequence_name: sequence to execute from item_movement_sequences
    """
    try:
        # Create instance of gripper and connect to gripper
        gr = URGripperController()
        gr.connect()
        
        # Init gripper (only run once when starting coding)
        gr.execute_gripper_script("init_gripper.script", call_function="init_gripper")
        
        # Choose which sequence to run from item_movement_sequences
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
        return "True"

    except Exception as e:
        print(f"ERROR: {e}")
        return "False"
    finally:
        gr.disconnect()