import socket
import time
import sys
import os

HOST = "192.168.100.10" # UR robot IP
PORT = 30002 # UR Secondary Client Port

class URGripperController:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.sock = None

    # -- connect to robot --
    def connect(self):
        """Establish persistent connection to UR robot."""
        try:
            print(f"Connecting to UR robot at {self.host}:{self.port} ...")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(10)
            self.sock.connect((self.host, self.port))
            print("Connected to UR robot.")

        except Exception as e:
            print(f"Connection failed: {e}")
            sys.exit(1)

    # -- disconnect from robot --
    def disconnect(self):
        """Gracefully close connection."""
        if self.sock:
            self.sock.close()
            self.sock = None
            print("Connection closed.")

    # -- execute gripper script with optional function call --
    def execute_gripper_script(self, script_filename, call_function=None):
        """
        Streams a URScript file to the robot.
        Optionally executes a function defined inside the script immediately.
        """
        if not self.sock:
            print("Not connected to robot. Call connect() first.")
            return False

        # Resolve file path relative to this Python file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(base_dir, "gripper_scripts", script_filename)

        print(f"--- Streaming script: {script_filename} ---")

        try:
            with open(script_path, "r", encoding="utf-8") as f:
                script = f.read()

            # Append a function call if provided
            if call_function:
                script += f"\n{call_function}()\n"

            # Send script to robot
            self.sock.sendall(script.encode("utf-8"))
            print(f"Script '{script_filename}' streamed successfully.")
            if call_function:
                print(f"Executed function '{call_function}()' on robot.")
            print("-----------------------------------------------------------\n")

            time.sleep(0.6)  # don't remove or change this time higher or lower!
            return True

        except FileNotFoundError:
            print(f"File not found: {script_path}")
        except Exception as e:
            print(f"Failed to stream script: {e}")
        return False