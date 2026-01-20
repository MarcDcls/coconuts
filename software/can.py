import can
import can.interfaces.canalystii as canalystii

BAUDRATE = 1000000 # 1 Mbps
MOTOR_ID = 0x141
READ_MOTOR_STATS_CMD = [0x9C, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]

with canalystii.CANalystIIBus(channel=0, bitrate=BAUDRATE) as bus:
    print("CANalyst-II bus opened with bitrate:", BAUDRATE)
    
    msg = can.Message(arbitration_id=MOTOR_ID, data=READ_MOTOR_STATS_CMD, is_extended_id=False)
    
    while True:
        try:
            bus.send(msg)
            print("Message sent on {}".format(bus.channel_info))
        
        except can.CanError:
            print("Message NOT sent")
        
        reply = bus.recv(1.0)  # Timeout after 1 second
        if reply:
            print("Reply received:")
            print("ID: ", hex(reply.arbitration_id))
            print("Data: ", reply.data)

            temp = reply.data[1]
            current = int.from_bytes(reply.data[2:4], byteorder='little', signed=True) * 0.1
            velocity = int.from_bytes(reply.data[4:6], byteorder='little', signed=True)
            position = int.from_bytes(reply.data[6:8], byteorder='little', signed=True)

            print(f"Temperature: {temp} °C")
            print(f"Current: {current} A")
            print(f"Velocity: {velocity} deg/s")
            print(f"Position: {position} deg")

        else:
            print("No reply received within the timeout period.")