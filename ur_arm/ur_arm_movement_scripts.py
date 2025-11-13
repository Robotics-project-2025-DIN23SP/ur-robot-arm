from typing import List
from .ur_arm_config import DYNAMIC_ACCEL, DYNAMIC_VELOCITY

def generate_movej_script(pose: List[float], name: str) -> str:
    """Generates the URScript string for a joint movement command."""
    pose_str = str(pose)
    
    script = f"""
def move_arm_to_{name}():
    textmsg("Moving to {name}: {pose_str}")
    # Use movej to move to a joint position smoothly
    movej({pose_str}, a={DYNAMIC_ACCEL}, v={DYNAMIC_VELOCITY})
    textmsg("Movement to {name} complete.")
end
move_arm_to_{name}()
"""
    return script.strip()