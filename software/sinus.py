# Copyright 2026 Marc Duclusaud

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

#     http://www.apache.org/licenses/LICENSE-2.0

import can
import can.interfaces.canalystii as canalystii
from software.rmd_motor import BITRATE, RMDMotor, RMDListener
import numpy as np
import matplotlib.pyplot as plt
import time
import sys

DT = 0.01

if len(sys.argv) <= 1:
    print("Usage: python sinus.py [IDS]")
    print("Example: python sinus.py 1 2 3")
    sys.exit(1)

ids = [int(arg) for arg in sys.argv[1:]]

with canalystii.CANalystIIBus(channel=0, bitrate=BITRATE, receive_own_messages=False) as bus:
    motors = {}
    for id in ids:
        motors[id] = RMDMotor(bus, id)

    listener = RMDListener(motors)
    with can.Notifier(bus, [listener]):

        states = {}
        for id, motor in motors.items():
            motor.set_position(0, max_speed_dps=200)
            states[id] = []
        time.sleep(2)
        
        t = 0
        while t < 10:
            step_start = time.perf_counter()

            # pos = 0
            pos = np.sin(t) * 100

            for id, motor in motors.items():
                motor.set_position(pos)
                states[id].append((t, pos, motor.get_position(), motor.get_last_update_time()))
            
            t += DT
            while time.perf_counter() - step_start < DT:
                pass
        
        for id, motor in motors.items():
            motor.stop_motor()

        # Plot results
        for id, state in states.items():
            state = np.array(state)
            plt.figure()
            plt.title(f"Motor ID {id} Position Tracking")
            plt.plot(state[:,0], state[:,1], label="Target Position", linestyle='--')
            plt.plot(state[:,0], state[:,2], label="Actual Position")
            plt.xlabel("Time (s)")
            plt.ylabel("Position (degrees)")
            plt.legend()
            plt.grid()
        plt.show() 
