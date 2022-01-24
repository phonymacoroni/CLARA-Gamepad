# README

This is a python program to listen for input from the Logitech F310 Gamepad and
send them over serial to a TinyPico board. 


#Proposed Protocol
| Bits |  0  |  1  |  2  |   3 |  4  |    5 |  6   |     7 |  8  |   9 | 10  | 11  |  12-19 | 20-27 | 28-36  | 37-44 |
|:-----|:---:|:---:|:---:|----:|:---:|-----:|:----:|------:|:---:|----:|:---:|:---:|-------:|:-----:|:------:|------:|
| Ref  |  A  |  B  |  X  |   Y | UP  | DOWN | LEFT | RIGHT | RB  |  LB | RT  | LT  | RJoy 1 | LJoy1 | RJoy 2 | LJoy2 |
