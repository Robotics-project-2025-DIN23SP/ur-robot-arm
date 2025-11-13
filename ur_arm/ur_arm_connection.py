import socket
import time
from .ur_arm_config import ROBOT_IP, DASHBOARD_PORT, PRIMARY_PORT

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