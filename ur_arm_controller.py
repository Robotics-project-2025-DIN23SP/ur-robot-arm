import socket
import time
from typing import List

# =========================================================
# I. CONFIGURATION AND POSE DEFINITIONS
# =========================================================

# Robot Connection Settings
ROBOT_IP = "192.168.100.10"
DASHBOARD_PORT = 29999 # For commands like 'power on', 'play'
PRIMARY_PORT = 30001   # For streaming URScript commands (e.g., movej)

# Motion Parameters
DYNAMIC_ACCEL = 0.45   # Acceleration for joint moves (rad/s^2)
DYNAMIC_VELOCITY = 0.45 # Velocity for joint moves (rad/s)

# Joint Pose Definitions (in Radians)
# Format: [Base, Shoulder, Elbow, Wrist1, Wrist2, Wrist3]
# Note: Positions 1-4 use the user-provided joint values.

DEFAULT_POSITION: List[float] = [1.57, -1.57, 1.57, -1.57, -1.57, 0.00]
POSITION_1_POSE: List[float] = [1.28, -0.81, 1.60, -2.37, -1.57, -0.28]
POSITION_2_POSE: List[float] = [1.27, -0.65, 1.61, -2.54, -1.57, -0.28]
POSITION_3_POSE: List[float] = [1.28, -0.81, 1.60, -2.37, -1.57, 0.29]
POSITION_4_POSE: List[float] =  [1.57, -1.57, 1.57, -1.57, -1.57, 0.00]


# =========================================================
# II. CORE COMMUNICATION FUNCTIONS
# =========================================================

def send_dashboard_command(command: str) -> str:
    """Send a single command to the UR Dashboard server (port 29999)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as dash:
            dash.settimeout(5)
            dash.connect((ROBOT_IP, DASHBOARD_PORT))
            dash.recv(1024)  # Read initial welcome message
            
            full_command = (command + "\n").encode("utf-8")
            dash.sendall(full_command)
            
            response = dash.recv(1024).decode("utf-8").strip()
            print(f"Dashboard [{command}] -> {response}")
            return response
    except Exception as e:
        print(f"❌ Dashboard command failed ({command}): {e}")
        return ""


def send_urscript(script: str):
    """Send raw URScript to the UR Primary client (port 30001) for execution."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((ROBOT_IP, PRIMARY_PORT))
            s.sendall(script.encode("utf-8"))
            print("✅ URScript sent successfully.")
    except Exception as e:
        print(f"❌ URScript send failed: {e}")
    time.sleep(0.1) # Brief pause after sending script


def generate_movej_script(pose: List[float], name: str) -> str:
    """Generates the URScript string for a joint movement command."""
    pose_str = str(pose)
    
    script = f"""
def move_arm_to_{name}():
    textmsg("Moving to {name}: {pose_str}")
    # Use movej to move to a joint position smoothly
    movej({pose_str}, a={DYNAMIC_ACCEL}, v={DYNAMIC_VELOCITY})
    textmsg("Movement to {name} complete.")
end
move_arm_to_{name}()
"""
    return script.strip()


# =========================================================
# III. CALLABLE ROBOT FUNCTIONS
# =========================================================

def initialize_robot():
    """Powers on, releases brakes, and starts the program."""
    print("\n--- Initializing Robot ---")
    send_dashboard_command("power on")
    time.sleep(2)
    send_dashboard_command("brake release")
    time.sleep(2)
    send_dashboard_command("unlock protective stop")
    time.sleep(1)
    send_dashboard_command("play") 
    print("--------------------------\n")


def move_to_default_position():
    """Moves the arm to the defined safe DEFAULT_POSITION."""
    script = generate_movej_script(DEFAULT_POSITION, "default_position")
    send_urscript(script)
    time.sleep(5) 

def move_to_position_1():
    """Moves the arm to the defined POSITION_1_POSE."""
    script = generate_movej_script(POSITION_1_POSE, "position_1")
    send_urscript(script)
    time.sleep(5) 

def move_to_position_2():
    """Moves the arm to the defined POSITION_2_POSE."""
    script = generate_movej_script(POSITION_2_POSE, "position_2")
    send_urscript(script)
    time.sleep(5) 

def move_to_position_3():
    """Moves the arm to the defined POSITION_3_POSE."""
    script = generate_movej_script(POSITION_3_POSE, "position_3")
    send_urscript(script)
    time.sleep(5) 

def move_to_position_4():
    """Moves the arm to the defined POSITION_4_POSE."""
    script = generate_movej_script(POSITION_4_POSE, "position_4")
    send_urscript(script)
    time.sleep(5) 


# =========================================================
# IV. MAIN EXECUTION BLOCK (Example Usage)
# =========================================================

if __name__ == "__main__":
    
    input("\nEnsure E-STOP is released and robot is in Remote Control mode. Press ENTER to continue...\n")
    initialize_robot()
    print("\n--- Testing all 4 Positions ---")
    move_to_position_1()
    move_to_position_2()
    move_to_position_3()
    move_to_position_4()
    move_to_default_position()
    print("\nMovement Sequence Complete.")