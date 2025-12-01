import cv2
import urllib.request
import numpy as np
import time
from .gopigo_detector import detect_gopigo


CAMERA_URL = "http://192.168.100.10:4242/current.jpg"

detection_state = {
    "Detected": False
    }

def show_live_feed(poll_interval=0.1):
    """
    Gets the live wrist camera feed with
    GoPiGo detection and text drawn.
    """
    print("Starting feed... (Press ESC to quit)")
    global detection_state

    while True:
        try:
            # fetch current frame
            with urllib.request.urlopen(CAMERA_URL, timeout=2) as resp:
                img_array = np.asarray(bytearray(resp.read()), dtype=np.uint8)
                frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            # convert to grayscale for ORB processing
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # handling gopigo detection
            detected, matches, kp = detect_gopigo(gray)

            detection_state["Detected"] = detected

            if detected:
                status = "GoPiGo DETECTED"
                color = (0, 255, 0)
            else:
                status = "GoPiGo NOT FOUND"
                color = (0, 0, 255)

            # draw status text
            cv2.putText(frame, status, (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            # draw matches if detected
            if detected:
                frame = cv2.drawKeypoints(frame, kp, None, color=(0, 255, 0))

            # display live video
            cv2.imshow("Wrist Camera", frame)

            # exit if ESC pressed
            if cv2.waitKey(1) & 0xFF == 27:
                break

            # wait for next poll
            time.sleep(poll_interval)

        except Exception as e:
            print(f"[Camera error] {e}")
            time.sleep(1)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    show_live_feed(poll_interval=0.15)