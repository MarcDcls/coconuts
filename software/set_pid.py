# Copyright 2026 Marc Duclusaud

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

#     http://www.apache.org/licenses/LICENSE-2.0

import can
import can.interfaces.canalystii as canalystii
from software.rmd_motor import BITRATE, RMDMotor, RMDListener
import time
import sys

if len(sys.argv) != 4:
    print("Usage: python set_filter.py [ID] [Kp] [Ki]")
    print("Example: python set_filter.py 1 100 5")
    sys.exit(1)

motor_id = int(sys.argv[1])
Kp = float(sys.argv[2])
Ki = float(sys.argv[3])

# Default current and velocity PI values
cur_kp = 100
cur_ki = 100
vel_kp = 100
vel_ki = 5

with canalystii.CANalystIIBus(channel=0, bitrate=BITRATE, receive_own_messages=False) as bus:
    motors = {motor_id: RMDMotor(bus, motor_id)}

    listener = RMDListener(motors)
    with can.Notifier(bus, [listener]):
        for id, motor in motors.items():
            motor.write_pid(cur_kp, cur_ki, vel_kp, vel_ki, Kp, Ki, to_rom=True)
            time.sleep(0.3)