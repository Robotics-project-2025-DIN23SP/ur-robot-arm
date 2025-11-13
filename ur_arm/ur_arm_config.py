from typing import List

# -- Robot Connection Settings --
ROBOT_IP = "192.168.100.10"
DASHBOARD_PORT = 29999 # For commands like 'power on', 'play'
PRIMARY_PORT = 30001   # For streaming URScript commands (e.g., movej)

# -- Motion Parameters --
DYNAMIC_ACCEL = 0.30   # Acceleration for joint moves (rad/s^2)
DYNAMIC_VELOCITY = 0.45 # Velocity for joint moves (rad/s)

# -- Joint Pose Definitions (in Radians) --
# Format for movej: [Base, Shoulder, Elbow, Wrist1, Wrist2, Wrist3]
# Format for movel: [x, y, z, rx, ry, rz] (in meters and radians)

# starting/ending position
DEFAULT_POSITION: List[float] = [1.57, -1.57, 1.57, -1.57, -1.57, 0.00]

# currently unused/redundant(?) positions
POSITION_3_POSE: List[float] = [1.28, -0.81, 1.60, -2.37, -1.57, 0.29]
POSITION_4_POSE: List[float] =  [1.57, -1.57, 1.57, -1.57, -1.57, 0.00]

# position on top of the GoPiGo car
POSITION_GOPIGO_LOW_POSE: List[float] =  [0.13473, -0.987507, 1.9620991, -2.496868, -1.598372, -1.502553]
POSITION_GOPIGO_HIGH_POSE: List[float] =  [0.13473, -1.05, 1.9620991, -2.496868, -1.598372, -1.502553]

# positions for item_1
POSITION_1_POSE: List[float] = [1.089783, -0.36913, 0.83095, -2.047795, -1.578127, -0.563741]
POSITION_2_POSE: List[float] = [1.089783, -0.34, 0.83095, -2.047795, -1.578127, -0.563741]

# TODO: positions for item_2

# positions for item_3 
POSITION_APPROACH_ITEM_3: List[float] = [1.2547, -0.5639, 1.04231, -2.04779, -1.56940, -0.316428]
# POSITION_GRASP_ITEM_3: List[float] = [-0.09292, -0.85299, -0.4081, 0.008, -3.151, -0.021]
POSITION_GRASP_ITEM_3: List[float] = [1.2547, -0.43737, 1.06901, -2.201209, -1.56940, -0.316428]

# TODO: positions for item_4