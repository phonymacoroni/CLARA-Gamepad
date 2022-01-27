# README

This is a python program to listen for input from the Logitech F310 Gamepad and
send them over serial to a TinyPico board. 


# Instructions
## Prerequisites
1. Python 3.6 or later
2. Install the requirements using `pip install -r requirements.txt` in the root of the directory

## Running
Ensure a `config.yaml` file exists in the root of the directory.
A sample `config.yaml` file is provided below, please ensure your config files contains all of these keys.
```yaml
---
  time_delay: 0.15
  desired_gamepad: 'Logitech Dual Action'
  desired_baud: 9600
  desired_vid: 0x046d
  desired_pid: 0xc216
  hardset_pico: '/dev/tty.usbserial-020ABD5F'
  deadzone: 20
```

Ensure that the serial port is not already open.

Run the program with the following command:
```
python3 -O main.py
```
The `-O` flag "optimizes" the program, which gets rid of debug print statements.


# Proposed Protocol
| Bits |     0-3     |  4  |  5  |   6 |  7  |  8  |   9 |  10-17 | 18-25 | 26-33  | 34-42 |
|:-----|:-----------:|:---:|:---:|----:|:---:|:---:|----:|-------:|:-----:|:------:|------:|
| Ref  | D-PAD Dir\* |  Y  |  X  |   B |  A  | RB  |  LB | LJoy 1 | LJoy2 | RJoy 1 | RJoy2 |

### Notes
\* D-Pad direction is represented by a 4 bit number, 0-7.
Here 0 is up, then clockwise to 7 at increments of 45 degrees
the value increases. (e.g. Bottom Left is 5, and Right is 2)


Joystick values are represented by 8 bit numbers, 0-255. 
Investigate Ranges.


For Kate and Brian, made with ❤️