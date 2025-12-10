import cv2
import urllib.request
import numpy as np
from .gopigo_detector import detect_gopigo

CAMERA_URL = "http://192.168.100.10:4242/current.jpg"

def get_processed_frame():
    """
    Fetches ONE processed wrist-camera frame with
    GoPiGo detection and text drawn.
    """
    try:
        # fetch image
        with urllib.request.urlopen(CAMERA_URL, timeout=2) as resp:
            img_array = np.asarray(bytearray(resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if frame is None:
            return None

        # convert to grayscale for ORB processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # handling gopigo detection
        detected, matches, kp = detect_gopigo(gray)

        if detected:
            status = "GoPiGo DETECTED"
            color = (0, 255, 0)
        else:
            status = "GoPiGo NOT FOUND"
            color = (0, 0, 255)

        # draw status text
        cv2.putText(frame, status, (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # draw matches if detected (ORB keypoints)
        if detected:
            frame = cv2.drawKeypoints(frame, kp, None, color=(0, 255, 0))

        # return singular frame
        return frame

    except Exception as e:
        print("[Camera error]", e)
        return None