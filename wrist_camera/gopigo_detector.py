import cv2

CAMERA_URL = "http://192.168.100.10:4242/current.jpg"

# create ORB detector (it extracts features from an image)
# "nfeatures=2000" means that it extracts up to 2000 features
orb = cv2.ORB_create(nfeatures=2000)

# load the reference images of GoPiGos that we compare the live camera feed to
# convert images to grayscale (which ORB uses)
ref_imgs = [
    cv2.imread("reference_pictures/gopigo_image_1.jpeg", cv2.IMREAD_GRAYSCALE),
    cv2.imread("reference_pictures/gopigo_image_2.jpeg", cv2.IMREAD_GRAYSCALE),
    cv2.imread("reference_pictures/gopigo_image_4.jpeg", cv2.IMREAD_GRAYSCALE),
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