import socket
import time
import sys

# ============================================================
# CONFIGURATION
# ============================================================

HOST = "192.168.100.10" # UR robot IP
PORT = 30002# UR Secondary Client Port

# ============================================================
# GRIPPER CONTROLLER CLASS
# ============================================================

class URGripperController:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.sock = None

    # --------------------------------------------------------
    # CONNECT TO ROBOT
    # --------------------------------------------------------
    def connect(self):
        """Establish persistent connection to UR robot."""
        try:
            print(f"🔌 Connecting to UR robot at {self.host}:{self.port} ...")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(10)
            self.sock.connect((self.host, self.port))
            print("✅ Connected to UR robot.")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            # Use sys.exit(1) only if you want the whole script to stop on failure.
            # For a class method, simply raising the error might be better in some cases.
            sys.exit(1)

    # --------------------------------------------------------
    # DISCONNECT FROM ROBOT
    # --------------------------------------------------------
    def disconnect(self):
        """Gracefully close connection."""
        if self.sock:
            self.sock.close()
            self.sock = None
            print("🔒 Connection closed.")

    # --------------------------------------------------------
    # HELPER: STREAM URSCRIPT FILE
    # --------------------------------------------------------
    def _stream_urs_file(self, script_filename):
        """Streams a generic URScript file to the robot for execution."""
        if not self.sock:
            print("❌ Not connected to robot. Call connect() first.")
            return False

        print(f"--- Streaming script: {script_filename} ---")
        try:
            with open(script_filename, "rb") as f:
                chunk = f.read(1024)
                while chunk:
                    self.sock.send(chunk)
                    chunk = f.read(1024)
            print(f"✅ Script '{script_filename}' streamed successfully.")
            return True
        except FileNotFoundError:
            print(f"❌ File not found: {script_filename}")
        except Exception as e:
            print(f"❌ Failed to stream script: {e}")
        finally:
            print("-----------------------------------------------------------\n")
        return False

    # --------------------------------------------------------
    # STREAM GRIPPER INITIALIZATION SCRIPT 
    # --------------------------------------------------------
    def initialize_gripper(self, script_filename="Gripper.script"):
        """
        Streams the full Robotiq gripper script. 
        This defines helper functions and initializes communication.
        """
        success = self._stream_urs_file(script_filename)
        # Give the robot extra time for initial full script parsing and activation
        if success:
            # IMPORTANT: Wait long enough for the robot controller to parse the file
            # and for activation functions (if called in the script) to complete.
            time.sleep(5) 

    # --------------------------------------------------------
    # SEND A SINGLE URSCRIPT COMMAND (with run_program wrapper)
    # --------------------------------------------------------
    def send_command(self, command):
        """Sends a URScript command (string) over the same socket, wrapped in run_program()."""
        if not self.sock:
            print("❌ Not connected to robot.")
            return

        try:
            # FIX: Use run_program() to ensure the globally defined function executes reliably.
            script = f"run_program({command})\n"
            self.sock.sendall(script.encode("utf-8"))
            print(f"➡️ Sent command: run_program({command.strip()})")
        except Exception as e:
            print(f"❌ Failed to send command: {e}")

    # --------------------------------------------------------
    # OPEN GRIPPER (Send function call)
    # --------------------------------------------------------
    def open_gripper(self):
        """Sends the URScript command to open the gripper (using the defined function)."""
        self.send_command("rq_open_and_wait()") # Assumes this is defined in Gripper.script

    # --------------------------------------------------------
    # CLOSE GRIPPER (Send function call) - FIX APPLIED HERE
    # --------------------------------------------------------
    def close_gripper(self, script_filename="Gripper_Close.script"):
        """
        Streams the full Robotiq gripper script. 
        This defines helper functions and initializes communication.
        """
        success = self._stream_urs_file(script_filename)
        # Give the robot extra time for initial full script parsing and activation
        if success:
            # IMPORTANT: Wait long enough for the robot controller to parse the file
            # and for activation functions (if called in the script) to complete.
            time.sleep(5) 

    def execute_gripper_script(self, script_filename):
        """
        Streams a specific Robotiq gripper URScript (open, close, etc.)
        to the robot. Handles timing automatically.
        """
        success = self._stream_urs_file(script_filename)
        if success:
            time.sleep(3)  # give robot time to parse and act
        else:
            print(f"⚠️ Failed to execute {script_filename}")



# ============================================================
# MAIN EXECUTION (for testing gripper independently)
# ============================================================

if __name__ == "__main__":
    gripper_ctrl = URGripperController()

    try:
        gripper_ctrl.connect()
        # 1. Load all function definitions and run initialization (activation)
        gripper_ctrl.initialize_gripper("Gripper.script")

        print("\nStarting independent test cycle (Sending function calls)...\n")
        
        # 2. Test Close
        print("ACTION: Closing gripper...")
        gripper_ctrl.close_gripper()
        time.sleep(3) 
        
        # 3. Test Open
        print("ACTION: Opening gripper...")
        gripper_ctrl.open_gripper()
        time.sleep(3)
        
        # 4. Test Close again
        print("ACTION: Closing gripper...")
        gripper_ctrl.close_gripper()

        print("\n✅ Test cycle complete.")

    except KeyboardInterrupt:
        print("\n⛔ Interrupted by user.")

    finally:
        gripper_ctrl.disconnect()