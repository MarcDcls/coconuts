# Copyright 2026 Marc Duclusaud

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

#     http://www.apache.org/licenses/LICENSE-2.0

import can

class RMDMotor:
    """
    Python interface for MyActuator RMD-X/L series motors over CAN bus.
    """
    def __init__(self, bus, motor_id=0x141):
        self.bus = bus
        self.motor_id = motor_id

    def _send_and_receive(self, data):
        """
        Sends a 8-byte CAN frame and waits for the motor's response.
        """
        msg = can.Message(
            arbitration_id=self.motor_id,
            data=data,
            is_extended_id=False
        )
        try:
            self.bus.send(msg)
            reply = self.bus.recv(0.5) # 500ms timeout for safety
            if reply:
                return self._parse_response(reply.data)
            return None
        except can.CanError as e:
            print(f"CAN Error: {e}")
            return None

    def _parse_response(self, data):
        """
        Parses the standard feedback frame (Temperature, Current, Speed, Position).
        """
        if not data or len(data) < 8:
            return None

        res = {
            "command_byte": hex(data[0]),
            "temp": data[1],  # °C
            "current": int.from_bytes(data[2:4], byteorder='little', signed=True) * 0.01,  # A
            "speed": int.from_bytes(data[4:6], byteorder='little', signed=True),  # deg/s
            "position": int.from_bytes(data[6:8], byteorder='little', signed=True)  # deg
        }
        return res

    # --- CONFIGURATION COMMANDS ---

    def read_pid(self):
        """Reads the current PID parameters from the motor (Command 0x30)."""
        return self._send_and_receive([0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def write_pid_to_ram(self, pos_kp, pos_ki, vel_kp, vel_ki, tor_kp, tor_ki):
        """Writes PID parameters to volatile RAM (Command 0x31)."""
        return self._send_and_receive([0x31, 0x00, pos_kp, pos_ki, vel_kp, vel_ki, tor_kp, tor_ki])

    def set_encoder_offset(self):
        """Sets the current position as the encoder zero point (Command 0x19)."""
        return self._send_and_receive([0x19, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    # --- CONTROL COMMANDS ---

    def stop_motor(self):
        """Turns off the motor and clears any running state (Command 0x80)."""
        return self._send_and_receive([0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def brake_motor(self):
        """Stops the motor and holds position (Command 0x81)."""
        return self._send_and_receive([0x81, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def torque_control(self, current_ma):
        """
        Torque/Current control (Command 0xA1). 
        Value: current in mA (range depends on motor model, e.g., -2000 to 2000).
        """
        current_bytes = int(current_ma).to_bytes(2, byteorder='little', signed=True)
        data = [0xA1, 0x00, 0x00, 0x00, current_bytes[0], current_bytes[1], 0x00, 0x00]
        return self._send_and_receive(data)

    def speed_control(self, speed_dps):
        """
        Speed closed-loop control (Command 0xA2).
        Value: speed in deg/s. Protocol uses 0.01 dps/LSB.
        """
        # Convert degrees/s to 0.01 deg/s units for the motor
        speed_val = int(speed_dps * 100)
        speed_bytes = speed_val.to_bytes(4, byteorder='little', signed=True)
        data = [0xA2, 0x00, 0x00, 0x00] + list(speed_bytes)
        return self._send_and_receive(data)

    def position_control(self, angle_deg):
        """
        Multi-turn absolute position control (Command 0xA3).
        Value: angle in degrees. Protocol uses 0.01 deg/LSB.
        """
        # Convert degrees to 0.01 degree units
        angle_val = int(angle_deg * 100)
        angle_bytes = angle_val.to_bytes(4, byteorder='little', signed=True)
        data = [0xA3, 0x00, 0x00, 0x00] + list(angle_bytes)
        return self._send_and_receive(data)

    def read_motor_stats(self):
        """Reads motor temperature, voltage, and error flags (Command 0x9C)."""
        return self._send_and_receive([0x9C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])