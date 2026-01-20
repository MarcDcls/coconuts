# CoconNuts Project

[![License: CERN-OHL-S-2.0](https://img.shields.io/badge/Hardware-CERN--OHL--S--2.0-blue.svg)](LICENSE)
[![License: Apache-2.0](https://img.shields.io/badge/Software-Apache--2.0-yellow.svg)](LICENSE)

TODO

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
