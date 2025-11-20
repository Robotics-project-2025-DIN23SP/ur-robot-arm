import cv2
import urllib.request
import numpy as np
import time


# ##Arm 1
# CAMERA_URL = "http://192.168.100.10:4242/current.jpg"
##Arm 2
CAMERA_URL = "http://192.168.100.20:4242/current.jpg"

def show_live_feed(poll_interval=0.1):
    print("Starting Robotiq Wrist Camera feed... (Press ESC to quit)")
    while True:
        try:
            # Fetch current frame
            with urllib.request.urlopen(CAMERA_URL, timeout=2) as resp:
                img_array = np.asarray(bytearray(resp.read()), dtype=np.uint8)
                frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            # Display
            cv2.imshow("Robotiq Wrist Camera", frame)

            # Exit if ESC pressed
            if cv2.waitKey(1) & 0xFF == 27:
                break

            # Wait before next poll (adjust for smoother/faster feed)
            time.sleep(poll_interval)

        except Exception as e:
            print(f"[Camera error] {e}")
            time.sleep(1)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    show_live_feed(poll_interval=0.15)
