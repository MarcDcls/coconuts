# Copyright 2026 Marc Duclusaud

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

#     http://www.apache.org/licenses/LICENSE-2.0

import placo
from placo_utils.visualization import robot_viz
import numpy as np
import matplotlib.pyplot as plt
import time
import argparse

DT = 0.02  # Not working under 0.02 with motors
JOINT_SIGNS = {"knee_joint": -1.0, "ankle_joint": 1.0}
MOTOR_SIGNS = {"knee_motor": -1.0, "ankle_motor": -1.0}
MOTOR_IDS = {"knee_motor": 1, "ankle_motor": 2}

parser = argparse.ArgumentParser(description="Benchmark robot simulation.")
parser.add_argument("--plot", action="store_true", help="Plot the results instead of running the simulation.")
parser.add_argument("--send", action="store_true", help="Send commands to real motors instead of running the simulation.")
parser.add_argument("--duration", type=float, default=4*np.pi, help="Duration of the benchmark in seconds.")
parser.add_argument("--knee_only", action="store_true", help="Control only the knee motor.")
parser.add_argument("--ankle_only", action="store_true", help="Control only the ankle motor.")
parser.add_argument("--zero", action="store_true", help="Set current position as zero for all motors.")
args = parser.parse_args()

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

if not args.send and not args.plot:
    print("Simulation mode. Not sending commands to real motors.")
    viz = robot_viz(robot)
    viz.display(robot.state.q)

t = 0.0
motor_traj = [(0.0, 0.0, 0.0)]
while t < args.duration:
    t += DT
    step_start = time.perf_counter()

    knee_target = np.sin(2*t - np.pi/2) * 0.85 + 0.85
    ankle_target = np.sin(2*t) * 0.7

    if args.knee_only:
        ankle_target = 0.0
    elif args.ankle_only:
        knee_target = 0.0
    elif args.zero:
        knee_target = 0.0
        ankle_target = 0.0

    joint_task.set_joints({
        "knee_joint": JOINT_SIGNS["knee_joint"] * knee_target,
        "ankle_joint": JOINT_SIGNS["ankle_joint"] * ankle_target
    })

    solver.solve(True)
    robot.update_kinematics()
    motor_traj.append((t, robot.get_joint("knee_motor") * 180 / np.pi, robot.get_joint("ankle_motor") * 180 / np.pi))

    # If in simulation mode, update visualization and wait to maintain real-time pace
    if not args.send and not args.plot:
        viz.display(robot.state.q)

        time_until_next_step = DT - (time.perf_counter() - step_start)
        if time_until_next_step > 0:
            time.sleep(time_until_next_step)

# Plot results
if args.plot:
    motor_traj = np.array(motor_traj)
    plt.figure()
    plt.title("Motor Positions")
    plt.plot(motor_traj[:,0], motor_traj[:,1], label="Knee Motor Position")
    plt.plot(motor_traj[:,0], motor_traj[:,2], label="Ankle Motor Position")
    plt.xlabel("Time (s)")
    plt.ylabel("Position (rad)")
    plt.grid()
    plt.legend()
    plt.show()

# Send commands to real motors
if args.send:
    print("Sending commands to real motors...")
    import can
    import can.interfaces.canalystii as canalystii
    from rmd_motor import BITRATE, RMDMotor, RMDListener

    with canalystii.CANalystIIBus(channel=0, bitrate=BITRATE, receive_own_messages=False) as bus:
        motors = {}
        for id in MOTOR_IDS.values():
            motors[id] = RMDMotor(bus, id)

        listener = RMDListener(motors)
        with can.Notifier(bus, [listener]):

            states = {}
            for id, motor in motors.items():
                for _ in range(3):
                    motor.set_position(0, max_speed_dps=500)
                    states[id] = []
                    time.sleep(0.3)
            time.sleep(3)
            
            i = 0
            while i < len(motor_traj):
                step_start = time.perf_counter()

                motors[MOTOR_IDS["knee_motor"]].set_position(MOTOR_SIGNS["knee_motor"] * motor_traj[i][1])
                time.sleep(0.002)
                motors[MOTOR_IDS["ankle_motor"]].set_position(MOTOR_SIGNS["ankle_motor"] * motor_traj[i][2])
                time.sleep(0.002)
                states[MOTOR_IDS["knee_motor"]].append((motor_traj[i][0], motor_traj[i][1], MOTOR_SIGNS["knee_motor"] * motors[MOTOR_IDS["knee_motor"]].get_position()))
                states[MOTOR_IDS["ankle_motor"]].append((motor_traj[i][0], motor_traj[i][2], MOTOR_SIGNS["ankle_motor"] * motors[MOTOR_IDS["ankle_motor"]].get_position()))
                
                i += 1

                while time.perf_counter() - step_start < DT:
                    pass
            
            for id, motor in motors.items():
                motor.stop_motor()
                time.sleep(0.3)

            # Plot results
            for id, state in states.items():
                state = np.array(state)
                state[np.abs(state[:, 1]) < 1e-3, 1] = 0 # Remove noise around zero
                plt.figure()
                plt.title(f"Motor ID {id} Position Tracking")
                plt.plot(state[:,0], state[:,1], label="Target Position", linestyle='--')
                plt.plot(state[:,0], state[:,2], label="Actual Position")
                plt.xlabel("Time (s)")
                plt.ylabel("Position (degrees)")
                plt.legend()
                plt.grid()
                plt.show() 