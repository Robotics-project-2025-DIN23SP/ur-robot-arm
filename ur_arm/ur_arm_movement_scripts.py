from typing import List

def generate_movej_script(
        pose: List[float], 
        name: str,  
        accel: float = 0.30, 
        vel: float = 0.45
    ) -> str:
    """Generates the URScript string for a joint movement command.
    Args:
        pose: movement pose
        name: Name of the movement for logging
        accel: acceleration for joint moves (rad/s^2)
        vel: velocity for joint moves (rad/s)
    """
    pose_str = str(pose)
    
    script = f"""
def move_arm_to_{name}():
    textmsg("Moving to {name}: {pose_str}")
    # Use movej to move to a joint position smoothly
    movej({pose_str}, a={accel}, v={vel})
    textmsg("Movement to {name} complete.")
end
move_arm_to_{name}()
"""
    return script.strip()

def generate_movel_script(
        pose: List[float], 
        name: str, 
        accel: float = 0.30, 
        vel: float = 0.45
    ) -> str:
    """Generates the URScript string for a linear movement command.
    Args:
        pose: movement pose
        name: Name of the movement for logging
        accel: acceleration for joint moves (rad/s^2)
        vel: velocity for joint moves (rad/s)
    """
    pose_str = str(pose)
    
    script = f"""
def move_arm_linearly_to_{name}():
    textmsg("Moving linearly to {name}: {pose_str}")
    # Use movel to move in a straight line in Cartesian space
    movel({pose_str}, a={accel}, v={vel})
    textmsg("Linear movement to {name} complete.")
end
move_arm_linearly_to_{name}()
"""
    return script.strip()

def generate_movec_script(
        via_pose: List[float], 
        target_pose: List[float], 
        name: str, 
        accel: float = 0.30, 
        vel: float = 0.45, 
        final_decel: float = 2.0
    ) -> str:
    """
    Generates the URScript string for a circular movement (movec) command.
    
    Args:
        via_pose: Intermediate waypoint (joint or Cartesian pose)
        target_pose: Final destination pose
        name: Name of the movement for logging
        accel: acceleration for joint moves (rad/s^2)
        vel: velocity for joint moves (rad/s)
        final_decel: deceleration to slow down at the end of the movement
    """
    via_str = str(via_pose)
    target_str = str(target_pose)

    # decel_line will cause the arm to overshoot the target
    # the smaller the value, the more overshoot
    # if no decel is given, the arm will jerk
    decel_line = f"\n    stopj({final_decel})" if final_decel is not None else "" 

    script = f"""
def move_arm_circular_to_{name}():
    textmsg("Moving circularly to {name} via {via_str} -> {target_str}")
    # Use movec to move through a circular arc
    movec({via_str}, {target_str}, a={accel}, v={vel}){decel_line}
    textmsg("Circular movement to {name} complete.")
end
move_arm_circular_to_{name}()
"""
    return script.strip()