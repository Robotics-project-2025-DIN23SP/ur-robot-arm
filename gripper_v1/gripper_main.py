from gripper import URGripperController

# gripper needs to be initialized before running

def run_custom_sequence():
    try:
        input("\n--- Initialization ---\nPress ENTER to start.\n")

        gr = URGripperController()
        gr.connect()

        print("\n--- Executing Gripper Commands ---\n")

        # Open gripper
        gr.execute_gripper_script("open_gripper.script", call_function="gripper_open")

        # Close gripper
        gr.execute_gripper_script("close_gripper.script", call_function="gripper_close")

        # Open gripper
        gr.execute_gripper_script("open_gripper.script", call_function="gripper_open")

        # Close gripper
        gr.execute_gripper_script("close_gripper.script", call_function="gripper_close")

        print("Sequence complete.")

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        gr.disconnect()

if __name__ == "__main__":
    run_custom_sequence()