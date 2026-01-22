# Copyright 2026 Marc Duclusaud

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

#     http://www.apache.org/licenses/LICENSE-2.0

import placo
from placo_utils.visualization import robot_viz, frame_viz, point_viz, robot_frame_viz, arrow_viz, tf, contacts_viz

import numpy as np
import time

DT = 0.01
JOINT_GAINS = {"knee_motor": -1.0, "ankle_motor": 1.0}

robot = placo.RobotWrapper("hardware/benchmark")
solver = placo.KinematicsSolver(robot)

# Knee timing belt
knee_gear_task = solver.add_gear_task()
knee_gear_task.add_gear("knee_joint", "knee_motor", -48/24)
knee_gear_task.configure("knee", "hard", 1.0)

# Ankle timing belt
ankle_gear_task = solver.add_gear_task()
ankle_gear_task.add_gear("ankle_passive", "ankle_motor", 48/24)
ankle_gear_task.add_gear("ankle_passive", "knee_joint", -1.0)
ankle_gear_task.configure("ankle", "hard", 1.0)

# Closing crank kinematic loop
closing_task = solver.add_relative_position_task("closing_crank", "closing_foot", np.zeros(3))
closing_task.mask.set_axises("xz")
closing_task.configure("closing", "hard", 1.0)

# Controlling in joint space
joint_task = solver.add_joints_task()
joint_task.set_joints({"knee_joint": 0.0, "ankle_joint": 0.0})

solver.add_regularization_task(1e-6)

for i in range(10):
    solver.solve(True)
    robot.update_kinematics()

viz = robot_viz(robot)
viz.display(robot.state.q)

t = 0.0
while True:
    step_start = time.time()      

    # Knee oscillation
    knee_target = np.sin(2*t - np.pi/2) * 0.8 + 0.8
    ankle_target = 0.0

    # Ankle oscillation
    # knee_target = 0.0
    # ankle_target = np.sin(3*t) * 0.8

    joint_task.set_joints({
        "knee_joint": JOINT_GAINS["knee_motor"] * knee_target,
        "ankle_joint": JOINT_GAINS["ankle_motor"] * ankle_target
    })

    solver.solve(True)
    robot.update_kinematics()
    
    viz.display(robot.state.q)

    t += DT
    time_until_next_step = DT - (time.time() - step_start)
    if time_until_next_step > 0:
        time.sleep(time_until_next_step)
