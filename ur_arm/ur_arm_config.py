from typing import List

# -- Robot Connection Settings --
ROBOT_IP = "192.168.100.10"
DASHBOARD_PORT = 29999 # For commands like 'power on', 'play'
PRIMARY_PORT = 30001   # For streaming URScript commands (e.g., movej)

# -- Joint Pose Definitions (in Radians) --
# Format for movej: [Base, Shoulder, Elbow, Wrist1, Wrist2, Wrist3]

# starting/ending position
DEFAULT_POSITION: List[float] = [1.57, -1.57, 1.57, -1.57, -1.57, 0.00]

# position on top of the GoPiGo car
POSITION_GOPIGO_LOW: List[float] =  [0.13473, -0.987507, 1.9620991, -2.496868, -1.598372, -1.502553]
POSITION_GOPIGO_HIGH: List[float] =  [0.13473, -1.05, 1.9620991, -2.496868, -1.598372, -1.502553]

# positions for item_1
POSITION_APPROACH_ITEM_1: List[float] = [1.089783, -0.36913, 0.83095, -2.047795, -1.578127, -0.563741]
POSITION_GRASP_ITEM_1: List[float] = [1.089783, -0.34, 0.83095, -2.047795, -1.578127, -0.563741]

# positions for item_2
POSITION_APPROACH_ITEM_2: List[float] = [1.23255, -1.22732, 1.68145, -2.02458, -1.57080, -0.33859]  # base, shoulder, elbow, wrist1, wrist2, wrist3
POSITION_GRASP_ITEM_2: List[float] = [1.23255, -0.95086, 1.91044, -2.53003, -1.57080, -0.33912]  # base, shoulder, elbow, wrist1, wrist2, wrist3

# positions for item_3 
POSITION_APPROACH_ITEM_3: List[float] = [1.2547, -0.5639, 1.04231, -2.04779, -1.56940, -0.316428]
POSITION_GRASP_ITEM_3: List[float] = [1.2547, -0.43737, 1.06901, -2.201209, -1.56940, -0.316428]

# TODO: positions for item_4
#POSITION_APPROACH_ITEM_4: List[float] = []#base, shoulder, elbow, wrist1, wrist2, wrist3
#POSITION_GRASP_ITEM_4: List[float] = []#base, shoulder, elbow, wrist1, wrist2, wrist3