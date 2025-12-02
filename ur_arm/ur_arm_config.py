from typing import List
from .degrees_to_radians import degrees_to_radians

# -- Robot Connection Settings --
ROBOT_IP = "192.168.100.10"
DASHBOARD_PORT = 29999 # For commands like 'power on', 'play'
PRIMARY_PORT = 30001   # For streaming URScript commands (e.g., movej)

# -- Joint Pose Definitions (in degrees now that we have conversion) --
# Format for movej: [Base, Shoulder, Elbow, Wrist1, Wrist2, Wrist3]

# starting/ending position
DEFAULT_POSITION: List[float] = degrees_to_radians([71.89, -92.67, 113.41, -112.82, -90.60, -198.77])

# position on top of the GoPiGo car
POSITION_GOPIGO_HIGH: List[float] =  degrees_to_radians([3.61, -64.32, 82.68, -109.95, -91.47, -176.72])
POSITION_GOPIGO_LOW: List[float] =  degrees_to_radians([3.60, -51.61, 97.22, -137.19, -91.46, -176.75])

# position for detecting the GoPiGo car
POSITION_GOPIGO_DETECT: List[float] =  degrees_to_radians([7.72, -68.96, 121.32, -143.92, -91.51, -175.61])

# positions for item_1
POSITION_APPROACH_ITEM_1: List[float] = degrees_to_radians([65.02, -73.07, 90.05, -106.94, -89.99, -205.01])
POSITION_GRASP_ITEM_1: List[float] = degrees_to_radians([65.02, -68.08, 100.17, -122.06, -89.99, -205.01])

# positions for item_2
POSITION_APPROACH_ITEM_2: List[float] = degrees_to_radians([72.17, -74.03, 91.38, -107.33, -89.99, -197.86])
POSITION_GRASP_ITEM_2: List[float] = degrees_to_radians([72.17, -68.94, 101.53, -122.57, -89.99, -197.86])

# positions for item_3 
POSITION_APPROACH_ITEM_3: List[float] = degrees_to_radians([79.47, -73.68, 90.91, -107.21, -89.99, -190.56])
POSITION_GRASP_ITEM_3: List[float] = degrees_to_radians([79.46, -68.63, 101.05, -122.39, -89.99, -190.57])

# positions for item_4
POSITION_APPROACH_ITEM_4: List[float] = degrees_to_radians([87.03, -72.25, 88.90, -106.64, -89.99, -183.00])
POSITION_GRASP_ITEM_4: List[float] = degrees_to_radians([87.03, -67.34, 99.01, -121.65, -89.99, -183.00])