# CoconNuts Project

[![License: CERN-OHL-S-2.0](https://img.shields.io/badge/Hardware-CERN--OHL--S--2.0-blue.svg)](LICENSE)
[![License: Apache-2.0](https://img.shields.io/badge/Software-Apache--2.0-yellow.svg)](LICENSE)

This repository contains the hardware design of the CocoNuts humanoid platform and the software to operate it with a CANalyst-II interface. 

<p align="center">
  <img width="50%" alt="image" src="https://github.com/user-attachments/assets/c196ff6f-5483-44ac-a44b-0cd585367477" />
</p>

## Install

To install the repository, you need the uv package manager. 
If you don't have it yet, you can install it by following the instructions [here](https://docs.astral.sh/uv/getting-started/installation/#installation-methods).

Then, clone this repository and run the following command in your terminal:
```
uv sync
```

To use the CANalyst-II device, you need to add a rule to grant USB permissions. To do so, copy the 99-canalyst.rules file provided to 
the `/etc/udev/rules.d/` directory:
```
sudo cp 99-canalyst.rules /etc/udev/rules.d/.
```

## List of motor commands

Several scripts are provided to set up the RMD-X6 servomotors. The available commands are:
- `./set_id.sh <new_id>`: Set the ID of the connected servomotor to `<new_id>`.
- `./ping.sh <ids>`: Ping the list of `<ids>` to check if the servomotors are connected.
- `./set_zeros.sh`: Set the current position of all servomotors as their zero position in their ROM.
- `./stop.sh`: Stop and release all servomotors.
- `./state.sh <ids>`: Display the state (temperature, position, velocity, current, last timestep of reading) of the servomotors in the list of `<ids>`.
- `./set_filter.sh <bool> <ids>`: Set the CAN filter to enable (`<bool>` = 1) or disable (`<bool>` = 0) filtering for the list of `<ids>`. 
- `./set_acceleration.sh <acceleration> <ids>`: Set the maximum acceleration/deceleration for the velocity and position control modes of the servomotors in the list of `<ids>` to `<acceleration>`. Setting `<acceleration>` to 0 disables the acceleration limit and the acceleration follow the default profile of the servomotor.
- `./set_pid.sh <id> <kp> <ki>`: Set the Kp and Ki gains of the servomotor `<id>` to `<kp>` and `<ki>`.
- `./read_rom.sh <ids>`: Display the ROM parameters (acc/dec of the control modes, PID gains) of the servomotors in the list of `<ids>`.

The commands are implemented in the `software/rmd_motor.py` file, which can also be imported as a module in your own Python scripts to write custom motor scripts.

## One leg benchmark

A one leg benchmark has been built to test the performance of the CocoNuts platform.

<p align="center">
  <img height="500px" alt="side" src="https://github.com/user-attachments/assets/670382e0-5b16-49f1-a0da-d174fdbad3cc" />
  <img height="500px" alt="front" src="https://github.com/user-attachments/assets/468604bf-aac2-4643-8453-3a27cea17485" />
<p\>
  
# Images

<p align="center">
  <img height="400px" alt="ankle" src="https://github.com/user-attachments/assets/c7d00547-16c4-4649-9c0b-2d2433ca8479" />
  <img height="400px" alt="ankle_gif" src="https://github.com/user-attachments/assets/46627b9f-a138-459c-b790-17784022fee5" />
<p\>


<p align="center">
  <img height="400px" alt="knee" src="https://github.com/user-attachments/assets/08262d12-0a1c-4662-aa13-9130761fcb2a" />
  <img height="400px" alt="knee_gif" src="https://github.com/user-attachments/assets/2d6a13b7-a184-4975-9187-b6cd73e4122b" />
<p\>

<p align="center">
  <img height="400px" alt="both" src="https://github.com/user-attachments/assets/ed2c4a98-9103-4c32-ad8e-4702f33a26f0" />
  <img height="400px" alt="both_gif" src="https://github.com/user-attachments/assets/77848361-197f-4186-b5b8-0a61ff626a13" />
<p\>

<img width="1207" height="1129" alt="image" src="https://github.com/user-attachments/assets/401a6d02-42ea-4c93-8a95-2f7a77933976" />
<img width="1336" height="794" alt="image" src="https://github.com/user-attachments/assets/2ac5253d-ad15-4d6a-8d11-d881b6dfe14e" />

<img height="450px" alt="image" src="https://github.com/user-attachments/assets/1bb45d46-6496-4f9d-9dc8-e4c168c15ec8" />
<img height="450px" alt="image" src="https://github.com/user-attachments/assets/63a41d52-8d3c-4607-9072-feea86809b89" />
