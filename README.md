# CoconNuts Project

[![License: CERN-OHL-S-2.0](https://img.shields.io/badge/Hardware-CERN--OHL--S--2.0-blue.svg)](LICENSE)
[![License: Apache-2.0](https://img.shields.io/badge/Software-Apache--2.0-yellow.svg)](LICENSE)

This repository contains the hardware design of the CocoNuts humanoid platform and the software to operate it with a CANalyst-II interface. 

It is currently under development and marked as a work in progress.

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

## List of commands

TODO

# Images

<img width="1207" height="1129" alt="image" src="https://github.com/user-attachments/assets/401a6d02-42ea-4c93-8a95-2f7a77933976" />
<img width="1336" height="794" alt="image" src="https://github.com/user-attachments/assets/2ac5253d-ad15-4d6a-8d11-d881b6dfe14e" />

<img height="450px" alt="image" src="https://github.com/user-attachments/assets/1bb45d46-6496-4f9d-9dc8-e4c168c15ec8" />
<img height="450px" alt="image" src="https://github.com/user-attachments/assets/63a41d52-8d3c-4607-9072-feea86809b89" />
