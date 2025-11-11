from flask import Flask, render_template_string, jsonify, request
from threading import Thread
import socket, time, base64, urllib.request
import numpy as np
import cv2
from rtde_receive import RTDEReceiveInterface

ROBOT_IP = "192.168.100.20"
DASHBOARD_PORT = 29999
URSCRIPT_PORT = 30002
CAMERA_URL = f"http://{ROBOT_IP}:4242/current.jpg"
JOINT_STEP = 0.05

camera_mode = 'color'

app = Flask(__name__)
robot_status = {
    "tcp_pose": [0]*6,
    "joint_angles": [0]*6,
    "tcp_force": [0]*6,
    "digital_outs": [False]*8
}

last_command_reply = "System Ready."

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
    global camera_frame, camera_mode
    while True:
        try:
            resp = urllib.request.urlopen(CAMERA_URL, timeout=2)
            arr = np.array(bytearray(resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            if frame is None:
                raise ValueError("Failed to decode camera image.")
            if camera_mode == 'grayscale':
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            elif camera_mode == 'high_contrast':
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                enhanced = clahe.apply(gray)
                frame = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
            camera_frame = base64.b64encode(buffer).decode('utf-8')
        except:
            camera_frame = None
        time.sleep(0.1)

@app.route("/")
def index():
    html = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>UR5 Dashboard</title>
<style>
body { font-family: 'Segoe UI', sans-serif; margin: 0; background: #f4f7f6; color: #333; }
.container { max-width: 98%; margin: 10px auto; padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
h1,h2 { color:#007bff; border-bottom:2px solid #eee; padding-bottom:5px; margin-top:20px; }
.main-content { display:grid; grid-template-columns:3fr 1fr; gap:20px; margin-top:20px; }
@media(max-width:1200px){.main-content{grid-template-columns:1fr}}
.camera-feed { grid-column:1; text-align:center; position:relative; overflow:hidden; border:1px solid #ccc; border-radius:4px; }
.controls-status { grid-column:2; display:flex; flex-direction:column; gap:20px; }
button { margin:5px; padding:10px 18px; font-size:14px; cursor:pointer; border:none; border-radius:4px; transition:0.3s; color:white; background-color:#6c757d; }
button:hover{background-color:#5a6268;}
.dashboard-controls button{background-color:#007bff;}
.dashboard-controls button:hover{background-color:#0056b3;}
.move-btn{width:40px;}
pre#status{background:#e9ecef;padding:15px;border-radius:4px;white-space:pre-wrap;word-wrap:break-word;font-size:13px;border:1px solid #ddd;}
#log{background:#fff3cd;color:#856404;padding:10px;margin-top:10px;border-radius:4px;border:1px solid #ffeeba;font-weight:bold;}
.joint-row{display:grid;grid-template-columns:40px 1fr 1fr 1fr;align-items:center;margin-bottom:5px;}
.joint-row b{text-align:right;padding-right:10px;}
.joint-value{font-family:'Consolas','Courier New',monospace;font-size:14px;}
.copy-position-section{display:flex;flex-direction:column;margin-top:10px;}
.copy-position-section input{font-family:'Consolas',monospace;font-size:13px;padding:8px;border:1px solid #ccc;border-radius:4px;margin-bottom:5px;}
.copy-position-section button{background-color:#28a745;margin:0;}
.copy-position-section button:hover{background-color:#1e7e34;}
#gridCanvas{position:absolute;top:0;left:0;pointer-events:none;z-index:10;}
#cam{display:block;width:100%;height:auto;}
.camera-options{margin-top:10px;padding:10px;background-color:#e9ecef;border-radius:4px;display:flex;flex-wrap:wrap;gap:10px;justify-content:center;align-items:center;}
.camera-options label{margin-right:5px;font-weight:bold;}
</style>
</head>
<body>
<div class="container">
<h1>⚙️ UR5 Dashboard</h1>
<div id="log">System Ready.</div>
<div class="main-content">
<div class="camera-feed">
<h2>📸 Camera Feed</h2>
<img id="cam" src="" alt="Camera Feed"/>
<canvas id="gridCanvas"></canvas>
<div class="camera-options">
<label>Mode:</label>
<input type="radio" id="mode_color" name="image_mode" value="color" checked onchange="setImageMode(this.value)"><label for="mode_color">Color</label>
<input type="radio" id="mode_grayscale" name="image_mode" value="grayscale" onchange="setImageMode(this.value)"><label for="mode_grayscale">Grayscale</label>
<input type="radio" id="mode_high_contrast" name="image_mode" value="high_contrast" onchange="setImageMode(this.value)"><label for="mode_high_contrast">High Contrast</label>
<label style="margin-left:20px;">Grid:</label><button onclick="toggleGrid()">Toggle</button>
<label>Spacing(px):</label><input type="number" id="grid_spacing" value="50" min="10" step="10" style="width:60px;" onchange="drawGrid()">
</div>
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
<input type="text" id="position_output" readonly value="[0.000,0.000,0.000,0.000,0.000,0.000]">
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
const jointStep={{ step }};
const logElement=document.getElementById('log');
const positionOutput=document.getElementById('position_output');
const cameraImage=document.getElementById('cam');
const gridCanvas=document.getElementById('gridCanvas');
const gridCtx=gridCanvas.getContext('2d');
let isGridVisible=false;

function updateLog(msg){logElement.innerText=msg}
function sendCmd(cmd){updateLog('Sending: '+cmd+'...');fetch('/cmd/'+cmd).then(r=>r.text()).then(updateLog)}
function moveJoint(j,delta){updateLog('Moving J'+(j+1)+'...');fetch(`/move_joint?joint=${j}&delta=${delta}`).then(r=>r.text()).then(updateLog)}
function copyPosition(){positionOutput.select();positionOutput.setSelectionRange(0,99999);navigator.clipboard.writeText(positionOutput.value).then(()=>updateLog('Copied: '+positionOutput.value)).catch(e=>updateLog('Copy error: '+e))}
function createJointButtons(angles){let c=document.getElementById('joint_buttons');c.innerHTML="";for(let i=0;i<6;i++){let a=angles?angles[i].toFixed(4):'---';c.innerHTML+=`<div class="joint-row"><b>J${i+1}:</b><span class="joint-value">${a} rad</span><button class="move-btn" onclick="moveJoint(${i},${jointStep})">+</button><button class="move-btn" onclick="moveJoint(${i},-${jointStep})">-</button></div>`}}
function drawGrid(){gridCtx.clearRect(0,0,gridCanvas.width,gridCanvas.height);if(!isGridVisible)return;let s=parseInt(document.getElementById('grid_spacing').value);if(isNaN(s)||s<=0)return;gridCtx.strokeStyle='rgba(255,255,255,0.5)';gridCtx.lineWidth=1;for(let x=0;x<gridCanvas.width;x+=s){gridCtx.beginPath();gridCtx.moveTo(x,0);gridCtx.lineTo(x,gridCanvas.height);gridCtx.stroke()}for(let y=0;y<gridCanvas.height;y+=s){gridCtx.beginPath();gridCtx.moveTo(0,y);gridCtx.lineTo(gridCanvas.width,y);gridCtx.stroke()}}
function resizeGridCanvas(){
    gridCanvas.width=cameraImage.offsetWidth;
    gridCanvas.height=cameraImage.offsetHeight;
    drawGrid();
}
function toggleGrid(){isGridVisible=!isGridVisible;drawGrid()}
function setImageMode(mode){updateLog('Setting mode: '+mode);fetch('/set_camera_mode',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mode:mode})}).then(r=>r.json()).then(d=>updateLog('Mode: '+d.current_mode)).catch(e=>updateLog('Error: '+e))}
function updateStatus(){
    fetch('/status').then(r=>r.json()).then(d=>{
        createJointButtons(d.joint_angles);
        let j=d.joint_angles.map(v=>v.toFixed(3));
        let tcp=d.tcp_pose.map(v=>v.toFixed(3));
        let f=d.tcp_force.map(v=>v.toFixed(2));
        positionOutput.value='['+j.join(', ')+']';
        document.getElementById('status').innerText=`POSITION: [${j.join(', ')}]\nTCP Pose: [${tcp.join(', ')}]\nTCP Force: [${f.join(', ')}]\nDigital Outs: ${d.digital_outs}\nLast Command Log: ${d.last_command_reply||'N/A'}`;
        
        if(d.camera){
            let newSrc='data:image/jpeg;base64,'+d.camera;
            if(cameraImage.src!==newSrc){
                cameraImage.src=newSrc;
                // CRUCIAL FIX: Set onload to ensure the canvas is resized after the new image is rendered
                cameraImage.onload=resizeGridCanvas;
            } else {
                // If the src is the same, just refresh grid/size for safety
                resizeGridCanvas();
            }
        } else {
            cameraImage.src='';
            gridCtx.clearRect(0,0,gridCanvas.width,gridCanvas.height)
        }
    })
}
document.addEventListener('DOMContentLoaded',()=>{
    updateStatus();
    setInterval(updateStatus,200);
    document.getElementById('mode_color').checked=true;
    window.addEventListener('resize',resizeGridCanvas);
});
</script>
</body>
</html>
"""
    return render_template_string(html, step=JOINT_STEP)

@app.route("/status")
def status():
    return jsonify({**robot_status, "camera": camera_frame, "last_command_reply": last_command_reply})

@app.route("/set_camera_mode", methods=["POST"])
def set_camera_mode():
    global camera_mode
    data = request.get_json()
    if data.get('mode') in ['color','grayscale','high_contrast']:
        camera_mode = data['mode']
        return jsonify({"status":"success","current_mode":camera_mode})
    return jsonify({"status":"error","message":"Invalid mode"}),400

@app.route("/cmd/<command>")
def cmd(command):
    return send_dashboard_command(command)

@app.route("/move_joint")
def move_joint_route():
    joint_index = int(request.args.get("joint",0))
    delta = float(request.args.get("delta",0))
    return move_joint(joint_index, delta)

if __name__ == "__main__":
    Thread(target=rtde_loop, daemon=True).start()
    Thread(target=camera_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)