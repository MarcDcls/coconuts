# Copyright 2026 Marc Duclusaud

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

#     http://www.apache.org/licenses/LICENSE-2.0

import can
import time

BITRATE = 1000000 # 1 Mbps


class RMDMotor:
    """
    Python interface for MyActuator RMD-X/L series motors over CAN bus.
    """
    def __init__(self, bus, id: int=1):
        self.bus = bus
        self.motor_id = id
        self.status = {
            "temp": 0,       # °C
            "current": 0.0,  # A
            "speed": 0,      # deg/s
            "position": 0,   # deg
            "last_update": 0 # s
        }

    def _send(self, data):
        """
        Sends a 8-byte CAN frame without waiting for a response.
        """
        msg = can.Message(
            arbitration_id=self.motor_id + 0x140,
            data=data,
            is_extended_id=False
        )
        try:
            self.bus.send(msg)
        except can.CanError as e:
            print(f"CAN Error: {e}")

    def update_status(self, data):
        """
        Updates the motor status based on received CAN data.
        """

        # Status update
        if data[0] in [0x9C, 0xA4]:
            self.status.update({
                "temp": data[1],
                "current": int.from_bytes(data[2:4], byteorder='little', signed=True) * 100, 
                "speed": int.from_bytes(data[4:6], byteorder='little', signed=True), 
                "position": int.from_bytes(data[6:8], byteorder='little', signed=True) * 100, 
                "last_update": time.perf_counter()
            })
        
        # PID print
        elif data[0] in [0x30, 0x31, 0x32]:
            print(f"Motor ID {self.motor_id} PID parameters:")
            print(f"  Current Kp: {data[1]}")
            print(f"  Current Ki: {data[2]}")
            print(f"  Velocity Kp: {data[3]}")
            print(f"  Velocity Ki: {data[4]}")
            print(f"  Position Kp: {data[5]}")
            print(f"  Position Ki: {data[6]}")
            print(f"  Position Kd: {data[7]}", flush=True)

        # Ping print
        elif data[0] == 0x01:
            print(f"Motor ID {self.motor_id} responded to ping.", flush=True)

        # Acceleration print
        elif data[0] == 0x42:
            if data[1] == 0x00:
                print(f"Motor ID {self.motor_id} position planning acceleration: {int.from_bytes(data[4:8], byteorder='little', signed=False)}", flush=True)
            elif data[1] == 0x01:
                print(f"Motor ID {self.motor_id} position planning deceleration: {int.from_bytes(data[4:8], byteorder='little', signed=False)}", flush=True)
            elif data[1] == 0x02:
                print(f"Motor ID {self.motor_id} velocity planning acceleration: {int.from_bytes(data[4:8], byteorder='little', signed=False)}", flush=True)
            elif data[1] == 0x03:
                print(f"Motor ID {self.motor_id} velocity planning deceleration: {int.from_bytes(data[4:8], byteorder='little', signed=False)}", flush=True)
            
    # --- UTILITY COMMANDS ---
    
    def ping(self):
        """Sends a ping command to check if the motor is responsive."""
        self._send([0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def read_status(self):
        """Reads motor temperature, voltage, and error flags (Command 0x9C)."""
        self._send([0x9C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    
    def read_pid(self):
        """Reads the current PID parameters from the motor (Command 0x30)."""
        self._send([0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def read_acceleration(self, pos_acc: bool=True, pos_dec: bool=True, vel_acc: bool=True, vel_dec: bool=True):
        """Reads the acceleration setting from the motor (Command 0x42)."""
        if pos_acc:
            self._send([0x42, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
            time.sleep(0.1)
        if pos_dec:
            self._send([0x42, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
            time.sleep(0.1)
        if vel_acc:
            self._send([0x42, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
            time.sleep(0.1)
        if vel_dec:
            self._send([0x42, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
            time.sleep(0.1)

    # --- CONFIGURATION COMMANDS ---

    def set_zero(self):
        """Sets the current multi-turn position as the encoder zero position in the ROM (Command 0x64)."""
        self._send([0x64, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def restart(self):
        """Restarts the motor system (Command 0x76)."""
        self._send([0x76, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def write_pid_to_ram(self, cur_kp: int, cur_ki: int, vel_kp: int, vel_ki: int, pos_kp: int, pos_ki: int, pos_kd: int):
        """Writes PID parameters to volatile RAM (Command 0x31)."""
        self._send([0x31, cur_kp, cur_ki, vel_kp, vel_ki, pos_kp, pos_ki, pos_kd])
    
    def write_pid_to_rom(self, cur_kp: int, cur_ki: int, vel_kp: int, vel_ki: int, pos_kp: int, pos_ki: int, pos_kd: int):
        """Writes PID parameters to non-volatile ROM (Command 0x32)."""
        self._send([0x32, cur_kp, cur_ki, vel_kp, vel_ki, pos_kp, pos_ki, pos_kd])
    
    # --- CONTROL COMMANDS ---

    def stop_motor(self):
        """Turns off the motor and clears any running state (Command 0x80)."""
        self._send([0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def brake_motor(self):
        """Stops the motor and holds position (Command 0x81)."""
        self._send([0x81, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    
    def set_position(self, angle_deg: int, max_speed_dps: int=3600):
        """Multi-turn absolute position control (Command 0xA4).
        Value: angle in degrees. Protocol uses 0.01 deg/LSB.
        """
        angle_val = int(angle_deg * 100)
        angle_bytes = angle_val.to_bytes(4, byteorder='little', signed=True)
        max_speed_bytes = int(max_speed_dps).to_bytes(2, byteorder='little', signed=False)
        data = [0xA4, 0x00] + list(max_speed_bytes) + list(angle_bytes)
        self._send(data)

    # --- STATUS GETTERS ---

    def get_position(self):
        """Returns the last known position in degrees."""
        return self.status["position"] / 100.0
    
    def get_velocity(self):
        """Returns the last known velocity in degrees per second."""
        return self.status["speed"]
    
    def get_current(self):
        """Returns the last known current in Amperes."""
        return self.status["current"]
    
    def get_temperature(self):
        """Returns the last known temperature in degrees Celsius."""
        return self.status["temp"]
    
    def get_last_update_time(self):
        """Returns the timestamp of the last status update."""
        return self.status["last_update"]


class RMDMotorBroadcast(RMDMotor):
    """
    Subclass for broadcasting commands to all motors on the CAN bus.
    """
    def __init__(self, bus):
        super().__init__(bus, id=(0x280 - 0x140))  # Broadcast ID is 0x280


class RMDListener(can.Listener):
    """
    Asynchronous listener that intercepts CAN messages and updates 
    the corresponding RMDMotor instances.
    """
    def __init__(self, motors_dict):
        """
        """
        self.motors = motors_dict 

    def on_message_received(self, msg):
        if msg.arbitration_id - 0x240 in self.motors:
            id = msg.arbitration_id - 0x240
            self.motors[id].update_status(msg.data)


if __name__ == "__main__":
    import can.interfaces.canalystii as canalystii
    import time
    import sys

    if len(sys.argv) <= 1:
        print("Usage: python rmd_motor.py [IDS]")
        print("Example: python rmd_motor.py 1 2 3")
        sys.exit(1)

    ids = [int(arg) for arg in sys.argv[1:]]

    with canalystii.CANalystIIBus(channel=0, bitrate=BITRATE, receive_own_messages=True) as bus:
        motors = {}
        for id in ids:
            motors[id] = RMDMotor(bus, id)

        listener = RMDListener(motors)
        with can.Notifier(bus, [listener]):
            while True:
                step_start = time.time()

                for id, motor in motors.items():
                    motor.read_status()
                    print(f"Motor ID {id} status: {motor.status}")
                
                while time.time() - step_start < 0.005:
                    time.sleep(1e-4)