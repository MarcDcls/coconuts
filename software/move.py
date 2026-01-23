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

if len(sys.argv) <= 1:
    print("Usage: python move.py [POS_IN_DEG] [IDS]")
    print("Example: python move.py 90 1 2 3")
    sys.exit(1)

position = float(sys.argv[1])
ids = [int(arg) for arg in sys.argv[2:]]

with canalystii.CANalystIIBus(channel=0, bitrate=BITRATE, receive_own_messages=False) as bus:
    motors = {}
    for id in ids:
        motors[id] = RMDMotor(bus, id)

    listener = RMDListener(motors)
    with can.Notifier(bus, [listener]):
        for id, motor in motors.items():
            for _ in range(3):
                motor.set_position(position, max_speed_dps=500)
                time.sleep(0.3)
            motor.stop_motor()
            time.sleep(0.3)