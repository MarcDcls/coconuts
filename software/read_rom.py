# Copyright 2026 Marc Duclusaud

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

#     http://www.apache.org/licenses/LICENSE-2.0

import can
import can.interfaces.canalystii as canalystii
from rmd_motor import BITRATE, RMDMotor, RMDListener
import time
import sys

if len(sys.argv) <= 1:
    print("Usage: python read_rom.py [IDS]")
    print("Example: python read_rom.py 1 2 3")
    sys.exit(1)

ids = [int(arg) for arg in sys.argv[1:]]

with canalystii.CANalystIIBus(channel=0, bitrate=BITRATE, receive_own_messages=False) as bus:
    motors = {}
    for id in ids:
        motors[id] = RMDMotor(bus, id)

    listener = RMDListener(motors)
    with can.Notifier(bus, [listener]):
        for id, motor in motors.items():
            motor.read_acceleration()
            time.sleep(0.1)
            motor.read_pid()
            time.sleep(0.1)