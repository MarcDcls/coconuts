# Coconuts project

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
