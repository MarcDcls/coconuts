
<p align="right">
  <img width="30%" alt="image" src="https://github.com/user-attachments/assets/c196ff6f-5483-44ac-a44b-0cd585367477" />
</p>

# CocoNuts Project

[![License: CERN-OHL-S-2.0](https://img.shields.io/badge/Hardware-CERN--OHL--S--2.0-blue.svg)](LICENSE)
[![License: Apache-2.0](https://img.shields.io/badge/Software-Apache--2.0-yellow.svg)](LICENSE)

The **CocoNuts project** is an open-source humanoid robotics research platform. Its primary design philosophy is the **minimization of leg inertia** by concentrating mass near the root of the limbs, utilizing a combination of timing belts and parallel linkage mechanisms. This repository contains the hardware design of the CocoNuts humanoid platform and the software to operate it with a CANalyst-II interface.

The CAD of the CocoNuts platform is open-source and available under the CERN-OHL-S-2.0 license 
[here](https://cad.onshape.com/documents/326c7618f048bbd5c9f71f42/v/8ddbb93e8d16fabe401f72ed/e/6f8aa33372eceae3daea128b). The motors used in the robot are RMD-X6 QDD actuators and TD30-40 and TD40-52 harmonic drive actuators.

The software provided is distributed under the Apache-2.0 license and is implemented in Python, which is not adapted for real-time control, but allows to easily set up and test the servomotors and the mechanical design. 

## Project Status

The prototype of a one leg benchmark of the CocoNuts platform was built to evaluate the performance of the design concept. The experiments provided critical insights into the platform's design:
- Actuator Mismatch: The RMD-X6 motors proved to be oversized for the current scale of the leg. Their high torque capability is offset by their weight, resulting in an unfavorable power-to-weight ratio for this specific frame. This suggests that the design would be more efficient either with a larger structural scale or with lighter, more compact actuators.
- Mechanical Complexity: The timing belt and parallel linkage system, while successful in shifting mass towards the body, introduced significant compliance and mechanical play. In the current iteration, these factors outweighed the benefits of reduced leg inertia.

These findings indicate that a major architectural pivot is required to better align the actuation power with the mechanical structure. As a result, the project is currently on hold and I am maintaining this repository as an open-access technical reference for the robotics community.

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

The one leg benchmark presented [here](https://cad.onshape.com/documents/326c7618f048bbd5c9f71f42/v/8ddbb93e8d16fabe401f72ed/e/362dba3e9b9b20be3e7fcf95) can be controlled using the `benchmark.sh` script. The script runs a series of trajectories to test the performance of the leg design. By default, the benchmark runs these trajectories in a meshcat visualizer to verify the motion of the leg before running it physically.

<p align="center">
  <img height="500px" alt="side" src="https://github.com/user-attachments/assets/670382e0-5b16-49f1-a0da-d174fdbad3cc" />
  <img height="500px" alt="front" src="https://github.com/user-attachments/assets/468604bf-aac2-4643-8453-3a27cea17485" />
<p\>

Prior to running the benchmark on the real hardware, make sure to set up the motors by:
- Setting the knee motor ID to 1 and the ankle motor ID to 2 using the `set_id.sh` script.
- Deactivating the CAN filters for both motors using the command `./set_filter.sh 0 1 2`.
- Setting the zero positions of both motors using the command `./set_zeros.sh` while the leg is extended with the foot horizontal. You can verify the zero positions by running the command `./state.sh 1 2` and checking that both motors read a position of 0.
- Setting the acceleration limits of both motors to 0 using the command `./set_acceleration.sh 0 1 2`.

Once the setup is complete, you can run the benchmark using the command:
```
./benchmark.sh <option>
```

where `<option>` can be:
- `--plot`: Plot the motor trajectories instead of running the visualization.
- `--send`: Run the benchmark on the real hardware instead of the visualization.
- `--duration <seconds>`: Set the duration of the trajectory to `<seconds>`.
- `--ankle_only`: Run a sinusoidal trajectory on the ankle motor only.
- `--knee_only`: Run a sinusoidal trajectory on the knee motor only, with the ankle fixed.
- `--zero`: Run a zero position trajectory.

By default the trajectory consists of a sinusoidal motion of both the knee and ankle motors with a duration of 4 * pi seconds.

## Results

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

# Images

<img width="1207" height="1129" alt="image" src="https://github.com/user-attachments/assets/401a6d02-42ea-4c93-8a95-2f7a77933976" />
<img width="1336" height="794" alt="image" src="https://github.com/user-attachments/assets/2ac5253d-ad15-4d6a-8d11-d881b6dfe14e" />

<img height="450px" alt="image" src="https://github.com/user-attachments/assets/1bb45d46-6496-4f9d-9dc8-e4c168c15ec8" />
<img height="450px" alt="image" src="https://github.com/user-attachments/assets/63a41d52-8d3c-4607-9072-feea86809b89" />
