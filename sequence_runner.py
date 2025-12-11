from gripper.gripper import URGripperController
import importlib
from wrist_camera.gopigo_detector import check_gopigo_in_detection_area
from ur_arm.ur_arm_actions import move_to
from threading import Thread
from wrist_camera.wrist_camera_feed import show_live_feed

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
            return False
        
        print("\n--- Initialization Complete. Starting Robot Sequence ---\n")
        
        sequence_steps = sequence_module.get_sequence(gr)
        # Start camera feed in background thread
        camera_thread = Thread(target=show_live_feed, daemon=True)
        camera_thread.start()
        
        # Map sequence names to item numbers and positions
        item_positions = {
            "item_1": {"approach": "position_approach_item_1", "grasp": "position_grasp_item_1"},
            "item_2": {"approach": "position_approach_item_2", "grasp": "position_grasp_item_2"},
            "item_3": {"approach": "position_approach_item_3", "grasp": "position_grasp_item_3"},
            "item_4": {"approach": "position_approach_item_4", "grasp": "position_grasp_item_4"},
        }
        
        # Get the correct positions for the current sequence being executed
        current_positions = item_positions.get(sequence_name, item_positions["item_1"])

        # Execute each step in the sequence
        for step_num, description, action_func in sequence_steps:
            print(f"**[Step {step_num}]** {description}...")
            action_func()
            print(f"Step {step_num} complete.\n")
            
            # Check if this is the detection step (step 7 - "Check for GoPiGo Car")
            if step_num == 7:
                # Check for GoPiGo presence with multiple checks for reliability
                gopigo_detected = check_gopigo_in_detection_area(wait_time=1, num_checks=3)
                
                if not gopigo_detected:
                    # GoPiGo not detected - return item to its original position
                    print(f">>> GoPiGo not detected! Returning {sequence_name} to pickup location...\n")
                    
                    # Move back to approach position
                    print("**[Return Step 1]** Move back to Approach Position...")
                    move_to(current_positions["approach"], 4)
                    print("Return Step 1 complete.\n")
                    
                    # Move to grasp position (original pickup)
                    print("**[Return Step 2]** Move back to Grasp Position (Original Pickup)...")
                    move_to(current_positions["grasp"], 4, "movel")
                    print("Return Step 2 complete.\n")
                    
                    # Open gripper to place item back
                    print("**[Return Step 3]** Open Gripper (Place Item Back)...")
                    gr.execute_gripper_script("open_gripper.script", call_function="gripper_open")
                    print("Return Step 3 complete.\n")
                    
                    # Move back to approach position
                    print("**[Return Step 4]** Move to Approach Position...")
                    move_to(current_positions["approach"], 2)
                    print("Return Step 4 complete.\n")

                    # Move back to default position
                    print("**[Return Step 5]** Move to Default Position...")
                    move_to("default_position", 2)
                    print("Return Step 5 complete.\n")
                    
                    print(f"\n*** {sequence_name.upper()} Returned. Sequence Aborted (GoPiGo Not Found). ***")
                    return True
            
        print("\n*** Full Sequence Complete. ***")
        return True

    except Exception as e:
        print(f"Error during sequence execution: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        gr.disconnect()
    
# This is for testing purposes only, so without needing to run the full websocket server
#if __name__ == "__main__":
#    run_custom_sequence("item_2")
