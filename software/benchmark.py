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

robot = placo.RobotWrapper("hardware/benchmark")
solver = placo.KinematicsSolver(robot)

# Timing belt system
gear_task = solver.add_gear_task()
gear_task.add_gear("knee_motor", "knee_joint", 1.0)
gear_task.add_gear("ankle_motor", "ankle_passive", 1.0)
gear_task.add_gear("ankle_passive", "ankle_joint", 1.0)

# Closing kinematic loop
solver.add_distance_task("closing_crank", "closing_foot", 0.0).configure("closing", "hard", 1.0)

solver.add_regularization_task(1e-6)

for i in range(10):
    solver.solve(True)
    robot.update_kinematics()

viz = robot_viz(robot)
viz.display(robot.state.q)

t = 0.0
while True:
    step_start = time.time()      

    robot.set_joint("ankle_motor", np.sin(2*t) * 0.5)
    solver.solve(True)
    robot.update_kinematics()
    
    viz.display(robot.state.q)

    t += DT
    time_until_next_step = DT - (time.time() - step_start)
    if time_until_next_step > 0:
        time.sleep(time_until_next_step)
