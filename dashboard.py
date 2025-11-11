from flask import Flask, render_template_string, jsonify, request
from threading import Thread
import socket
import time
import base64
import urllib.request
import numpy as np
import cv2
from rtde_receive import RTDEReceiveInterface 

# ---------- CONFIG ----------
#ARM 1
# ROBOT_IP = "192.168.100.10"
#ARM 2
ROBOT_IP = "192.168.100.20"
DASHBOARD_PORT = 29999
URSCRIPT_PORT = 30002
CAMERA_URL = f"http://{ROBOT_IP}:4242/current.jpg"
JOINT_STEP = 0.05

# ---------- FLASK SETUP ----------
app = Flask(__name__)
robot_status = {
    "tcp_pose": [0]*6,
    "joint_angles": [0]*6,
    "tcp_force": [0]*6,
    "digital_outs": [False]*8
}

last_command_reply = "System Ready."

# ---------- ROBOT CONTROL ----------
def send_dashboard_command(cmd):
    global last_command_reply
    try:
        with socket.create_connection((ROBOT_IP, DASHBOARD_PORT), timeout=2) as s:
            s.sendall((cmd + "\n").encode())
            reply = s.recv(1024).decode().strip()
            last_command_reply = f"Dashboard Command '{cmd}': {reply}"
            return reply
    except Exception as e:
        last_command_reply = f"Error sending '{cmd}': {e}"
        return f"Error: {e}"

def move_joint(joint_index: int, delta: float):
    global last_command_reply
    q = robot_status["joint_angles"].copy()
    
    if not any(q):
        last_command_reply = "Warning: Robot position is all zeros. Ensure robot is connected/initialized."
        return last_command_reply

    q[joint_index] += delta
    urscript = f"movej({q}, a=1.2, v=0.25)"
    try:
        with socket.create_connection((ROBOT_IP, URSCRIPT_PORT), timeout=2) as s:
            s.sendall((urscript + "\n").encode())
        last_command_reply = f"Moved J{joint_index+1} by {delta:.3f} rad"
        return last_command_reply
    except Exception as e:
        last_command_reply = f"Error moving J{joint_index+1}: {e}"
        return last_command_reply


def rtde_loop():
    rtde_r = RTDEReceiveInterface(ROBOT_IP)
    while True:
        try:
            robot_status["tcp_pose"] = rtde_r.getActualTCPPose()
            robot_status["joint_angles"] = rtde_r.getActualQ()
            robot_status["tcp_force"] = rtde_r.getActualTCPForce()
            robot_status["digital_outs"] = [rtde_r.getDigitalOutState(i) for i in range(8)]
        except:
            pass
        time.sleep(0.1)

camera_frame = None
def camera_loop():
    global camera_frame
    while True:
        try:
            resp = urllib.request.urlopen(CAMERA_URL, timeout=2)
            arr = np.array(bytearray(resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            _, buffer = cv2.imencode('.jpg', frame)
            camera_frame = base64.b64encode(buffer).decode('utf-8')
        except:
            pass
        time.sleep(0.1)

@app.route("/")
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>UR5 Dashboard</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background: #f4f7f6; color: #333; }
            .container { max-width: 1200px; margin: 20px auto; padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
            h1, h2 { color: #007bff; border-bottom: 2px solid #eee; padding-bottom: 5px; margin-top: 20px; }
            
            .main-content { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-top: 20px; }
            .camera-feed { grid-column: 1; text-align: center; }
            .controls-status { grid-column: 2; display: flex; flex-direction: column; gap: 20px; }
            
            button { 
                margin: 5px; padding: 10px 18px; font-size: 14px; cursor: pointer; 
                border: none; border-radius: 4px; transition: background-color 0.3s;
                background-color: #6c757d; color: white;
            }
            button:hover { background-color: #5a6268; }
            .dashboard-controls button { background-color: #007bff; }
            .dashboard-controls button:hover { background-color: #0056b3; }
            .move-btn { width: 40px; } 
            
            pre#status { background: #e9ecef; padding: 15px; border-radius: 4px; white-space: pre-wrap; word-wrap: break-word; font-size: 13px; border: 1px solid #ddd; }
            #log { background: #fff3cd; color: #856404; padding: 10px; margin-top: 10px; border-radius: 4px; border: 1px solid #ffeeba; font-weight: bold; }
            
            .joint-row { display: grid; grid-template-columns: 40px 1fr 1fr 1fr; align-items: center; margin-bottom: 5px; }
            .joint-row b { text-align: right; padding-right: 10px; }
            .joint-value { font-family: 'Consolas', 'Courier New', monospace; font-size: 14px; }

            .copy-position-section { display: flex; flex-direction: column; margin-top: 10px; }
            .copy-position-section input { font-family: 'Consolas', monospace; font-size: 13px; padding: 8px; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 5px; }
            .copy-position-section button { background-color: #28a745; margin: 0; }
            .copy-position-section button:hover { background-color: #1e7e34; }

        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚙️ UR5 Dashboard</h1>
            
            <div id="log">System Ready.</div>
            
            <div class="main-content">
                
                <div class="camera-feed">
                    <h2>📸 Camera Feed</h2>
                    <img id="cam" src="" width="100%" height="auto" style="max-width: 640px; border: 1px solid #ccc;"/>
                </div>
                
                <div class="controls-status">
                    
                    <div class="dashboard-controls">
                        <h2>🛠 Robot Control</h2>
                        <button onclick="sendCmd('power on')">Power On</button>
                        <button onclick="sendCmd('brake release')">Brake Release</button><br>
                        <button onclick="sendCmd('play')">Play</button>
                        <button onclick="sendCmd('pause')">Pause</button>
                        <button onclick="sendCmd('stop')">Stop</button>
                    </div>

                    <div>
                        <h2>🧭 Joint Control (Step: {{ step }} rad)</h2>
                        <div id="joint_buttons"></div>
                    </div>
                    
                    <div class="copy-position-section">
                        <h2>📋 Copy Joint Position</h2>
                        <input type="text" id="position_output" readonly value="[0.000, 0.000, 0.000, 0.000, 0.000, 0.000]">
                        <button onclick="copyPosition()">Copy to Clipboard</button>
                    </div>

                    <div>
                        <h2>📊 Robot Status</h2>
                        <pre id="status"></pre>
                    </div>
                </div>
                
            </div>
            
        </div>

        <script>
            const jointStep = {{ step }};
            const logElement = document.getElementById('log');
            const positionOutput = document.getElementById('position_output');

            function updateLog(message) {
                logElement.innerText = message;
            }

            function sendCmd(cmd){
                updateLog('Sending command: ' + cmd + '...');
                fetch('/cmd/' + cmd).then(r=>r.text()).then(updateLog)
            }

            function moveJoint(j, delta){
                updateLog('Moving J' + (j+1) + '...');
                fetch(`/move_joint?joint=${j}&delta=${delta}`).then(r=>r.text()).then(updateLog)
            }
            
            function copyPosition() {
                positionOutput.select();
                positionOutput.setSelectionRange(0, 99999); 
                navigator.clipboard.writeText(positionOutput.value).then(() => {
                    updateLog('Joint Position Copied: ' + positionOutput.value);
                }).catch(err => {
                    updateLog('Error copying position: ' + err);
                });
            }

            function createJointButtons(joint_angles){
                let container = document.getElementById('joint_buttons')
                container.innerHTML = ""
                for(let i=0;i<6;i++){
                    const angle = joint_angles ? joint_angles[i].toFixed(4) : '---';
                    container.innerHTML += `
                        <div class="joint-row">
                            <b>J${i+1}:</b> 
                            <span class="joint-value">${angle} rad</span>
                            <button class="move-btn" onclick="moveJoint(${i}, ${jointStep})">+</button>
                            <button class="move-btn" onclick="moveJoint(${i}, -${jointStep})">-</button>
                        </div>
                    `
                }
            }

            function updateStatus(){
                fetch('/status').then(r=>r.json()).then(data=>{
                    
                    createJointButtons(data.joint_angles);
                    
                    let joints_list = data.joint_angles.map(v=>v.toFixed(3));
                    let tcp_pose_list = data.tcp_pose.map(v=>v.toFixed(3));
                    let tcp_force_list = data.tcp_force.map(v=>v.toFixed(2));
                    
                    // Update copy-paste text field
                    positionOutput.value = '[' + joints_list.join(", ") + ']';

                    document.getElementById('status').innerText =
                        `POSITION: [${joints_list.join(", ")}]

TCP Pose (x, y, z, rx, ry, rz): [${tcp_pose_list.join(", ")}]
TCP Force (fx, fy, fz, tx, ty, tz): [${tcp_force_list.join(", ")}]

Digital Outs: ${data.digital_outs}
Last Command Log: ${data.last_command_reply || 'N/A'}`;

                    if(data.camera) {
                        document.getElementById('cam').src = 'data:image/jpeg;base64,' + data.camera;
                    } else {
                         document.getElementById('cam').src = '';
                    }
                })
            }

            updateStatus();
            setInterval(updateStatus, 200);
            
        </script>
    </body>
    </html>
    """
    return render_template_string(html, step=JOINT_STEP)

@app.route("/status")
def status():
    return jsonify({
        **robot_status, 
        "camera": camera_frame,
        "last_command_reply": last_command_reply
    })

@app.route("/cmd/<command>")
def cmd(command):
    reply = send_dashboard_command(command)
    return reply

@app.route("/move_joint")
def move_joint_route():
    joint_index = int(request.args.get("joint", 0))
    delta = float(request.args.get("delta", 0))
    reply = move_joint(joint_index, delta)
    return reply

# ---------- MAIN ----------
if __name__ == "__main__":
    Thread(target=rtde_loop, daemon=True).start()
    Thread(target=camera_loop, daemon=True).start()
    print("Starting UR5 Dashboard on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000)