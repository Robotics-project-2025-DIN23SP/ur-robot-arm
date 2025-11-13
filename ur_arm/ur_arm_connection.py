import socket
import time
from .ur_arm_config import ROBOT_IP, DASHBOARD_PORT, PRIMARY_PORT

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