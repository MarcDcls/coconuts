# Copyright 2026 Marc Duclusaud

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

#     http://www.apache.org/licenses/LICENSE-2.0

import can.interfaces.canalystii as canalystii
from software.rmd_motor import BITRATE, RMDMotorBroadcast
import time

with canalystii.CANalystIIBus(channel=0, bitrate=BITRATE) as bus:
    motors = RMDMotorBroadcast(bus)
    motors.stop_motor()
    time.sleep(1)
