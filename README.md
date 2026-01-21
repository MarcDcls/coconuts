# CoconNuts Project

[![License: CERN-OHL-S-2.0](https://img.shields.io/badge/Hardware-CERN--OHL--S--2.0-blue.svg)](LICENSE)
[![License: Apache-2.0](https://img.shields.io/badge/Software-Apache--2.0-yellow.svg)](LICENSE)

[WIP]

<p align="center">
  <img width="50%" alt="image" src="https://github.com/user-attachments/assets/c196ff6f-5483-44ac-a44b-0cd585367477" />
</p>

## CAN setup

To show SLCAN devices:
```
sudo modprobe usbserial vendor=0x04d8 product=0x0053
```

To set a 1Mb driver:
```
sudo slcand -o -s8 -F ttyUSB0
```

## Python CAN

Install the python-can module with the CANalyst-II driver:
```
pip install "python-can[canalystii]"
```

Add a rule to grant USB permissions:
```
sudo touch /etc/udev/rules.d/99-canalyst.rules
```

Then edit the rule using nano:
```
sudo nano /etc/udev/rules.d
```

Write `SUBSYSTEM=="usb", ATTRS{idVendor}=="04d8", MODE="0666"`, save using Ctrl+O and exit with Ctrl+X.

--------------------------------------------

```
sudo modprobe usbserial vendor=0x04d8 product=0x0053
sudo slcand -o -c -s8 /dev/ttyUSB0 can0
sudo ip link set can0 up
sudo ip link set can0 txqueuelen 1000
```

# Images

<img width="1207" height="1129" alt="image" src="https://github.com/user-attachments/assets/401a6d02-42ea-4c93-8a95-2f7a77933976" />
<img width="1336" height="794" alt="image" src="https://github.com/user-attachments/assets/2ac5253d-ad15-4d6a-8d11-d881b6dfe14e" />

<img height="450px" alt="image" src="https://github.com/user-attachments/assets/1bb45d46-6496-4f9d-9dc8-e4c168c15ec8" />
<img height="450px" alt="image" src="https://github.com/user-attachments/assets/63a41d52-8d3c-4607-9072-feea86809b89" />
