# README

This is a python program to listen for input from the Logitech F310 Gamepad and
send them over serial to a TinyPico board. 


# Instructions
## Prerequisites
1. Python 3.6 or later
2. Install the requirements using `pip install -r requirements.txt` in the root of the directory

## Running
Ensure that the serial port is not already open.

Run the program with the following command:
```
python3 -O main.py
```
The `-O` flag "optimizes" the program, which gets rid of debug print statements.


#Proposed Protocol
| Bits |  0  |  1  |  2  |   3 |     4-7     |  8  |   9 |  10-17 | 18-25 | 26-33  | 34-42 |
|:-----|:---:|:---:|:---:|----:|:-----------:|:---:|----:|-------:|:-----:|:------:|------:|
| Ref  |  A  |  B  |  X  |   Y | D-PAD Dir\* | RB  |  LB | LJoy 1 | LJoy2 | RJoy 1 | RJoy2 |

###Notes
\* D-Pad direction is represented by a 4 bit number, 0-7.
Here 0 is up, then clockwise to 7 at increments of 45 degrees
the value increases. (e.g. Bottom Left is 5, and Right is 2)


Joystick values are represented by 8 bit numbers, 0-255. 
Investigate Ranges.


For Kate and Brian, made with ❤️