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

if len(sys.argv) != 2:
    print("Usage: python set_id.py [NEW_ID]")
    print("Example: python set_id.py 1")
    sys.exit(1)

new_id = int(sys.argv[1])

with canalystii.CANalystIIBus(channel=0, bitrate=BITRATE, receive_own_messages=False) as bus:
    setting_id = 0x300 - 0x140
    broadcast_id = 0x280 - 0x140
    motors = {setting_id: RMDMotor(bus, setting_id), 
              broadcast_id: RMDMotor(bus, broadcast_id)}
    listener = RMDListener(motors)
    with can.Notifier(bus, [listener]):
        motors[setting_id].set_id(new_id)
        time.sleep(0.5)
        motors[broadcast_id].restart()
        time.sleep(0.5)