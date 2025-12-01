import cv2
import os
import urllib.request
import numpy as np
import time

CAMERA_URL = "http://192.168.100.10:4242/current.jpg"

# create ORB detector (it extracts features from an image)
# "nfeatures=2000" means that it extracts up to 2000 features
orb = cv2.ORB_create(nfeatures=2000)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

REF_IMG_DIR = os.path.join(BASE_DIR, "reference_pictures")

# load the reference images of GoPiGos that we compare the live camera feed to
# convert images to grayscale (which ORB uses)
ref_imgs = [
    cv2.imread(os.path.join(REF_IMG_DIR, "gopigo_image_1.jpeg"), cv2.IMREAD_GRAYSCALE),
    cv2.imread(os.path.join(REF_IMG_DIR, "gopigo_image_2.jpeg"), cv2.IMREAD_GRAYSCALE),
    cv2.imread(os.path.join(REF_IMG_DIR, "gopigo_image_4.jpeg"), cv2.IMREAD_GRAYSCALE),
]

ref_features = []

# kp is a list of interesting spots on the GoPiGo (that we use to detect a GoPiGo)
# des has numeric vectors describing each spot
for img in ref_imgs:
    ref_kp, ref_des = orb.detectAndCompute(img, None)

    if ref_des is not None:
        ref_features.append((ref_kp, ref_des))

# creates a matching engine that compares the spots to the live gopigo on the camera feed
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# minimum matches required for detection
# might be necessary to change to 55 or something later
MATCH_THRESHOLD = 60

def detect_gopigo(frame_gray):
    try:
        # get interesting spots and their numeric vectors from the current camera feed
        kp_frame, des_frame = orb.detectAndCompute(frame_gray, None)

        # if no features are found at all, return
        if des_frame is None:
            return False, [], kp_frame

        best_good_matches = 0

        for (ref_kp, ref_des) in ref_features:
            # match current camera feed to reference images
            matches = bf.match(ref_des, des_frame)

            # sort by quality (how similar the freatures are in references and current feed)
            # distance = how similar the features are
            matches = sorted(matches, key=lambda x: x.distance)

            good_matches = [m for m in matches if m.distance < 50]

            # keep track of the best match count among all reference images
            best_good_matches = max(best_good_matches, len(good_matches))

            if len(good_matches) >= MATCH_THRESHOLD:
                return True, good_matches, kp_frame

        return False, [], kp_frame

        best_good_matches = 0

        for (ref_kp, ref_des) in ref_features:
            # match current camera feed to reference images
            matches = bf.match(ref_des, des_frame)

            # sort by quality (how similar the freatures are in references and current feed)
            # distance = how similar the features are
            matches = sorted(matches, key=lambda x: x.distance)

            good_matches = [m for m in matches if m.distance < 50]

            # keep track of the best match count among all reference images
            best_good_matches = max(best_good_matches, len(good_matches))

            if len(good_matches) >= MATCH_THRESHOLD:
                return True, good_matches, kp_frame

        return False, [], kp_frame


        def capture_frame_from_camera():
            """
            Captures a single frame from the robot's wrist camera.
            Returns the frame in BGR format, or None if capture fails.
            """
            try:
                with urllib.request.urlopen(CAMERA_URL, timeout=2) as resp:
                    img_array = np.asarray(bytearray(resp.read()), dtype=np.uint8)
                    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                return frame
            except Exception as e:
                print(f"[Camera capture error] {e}")
                return None


        def check_gopigo_in_detection_area(wait_time=2, num_checks=3):
            """
            Checks if GoPiGo car is present in the detection area.
            
            Args:
                wait_time: Seconds to wait between checks
                num_checks: Number of checks to perform (for reliability)
            
            Returns:
                True if GoPiGo detected, False otherwise
            """
            detection_results = []
            
            print(f"Checking for GoPiGo... (performing {num_checks} checks)")
            
            for check_num in range(num_checks):
                try:
                    frame = capture_frame_from_camera()
                    if frame is None:
                        print(f"Check {check_num + 1}/{num_checks}: Failed to capture frame")
                        detection_results.append(False)
                    else:
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        detected, _, _ = detect_gopigo(gray)
                        status = "DETECTED" if detected else "NOT FOUND"
                        print(f" Check {check_num + 1}/{num_checks}: {status}")
                        detection_results.append(detected)
                    
                    # Wait before next check (except on last check)
                    if check_num < num_checks - 1:
                        time.sleep(wait_time)
                
                except Exception as e:
                    print(f"Check {check_num + 1}/{num_checks}: Error - {e}")
                    detection_results.append(False)
            
            # Return True if majority of checks detected GoPiGo
            detected_count = sum(detection_results)
            gopigo_found = detected_count >= (num_checks / 2)
            
            print(f"\nDetection Result: {'GoPiGo FOUND' if gopigo_found else 'GoPiGo NOT FOUND'} ({detected_count}/{num_checks} checks)\n")
            
            return gopigo_found
    
    except Exception as e:
        print(f"GoPiGo Detection ERROR: {e}")
