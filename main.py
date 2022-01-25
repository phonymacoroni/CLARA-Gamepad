import hid
import serial
from enum import Enum


def construct_button_bits(gpst):
    """
    Constructs the button bits from the gamepad state
    :param gpst: Gamepad State
    :return butt_st: 8 Bits Representing the Button State
    """
    # Blank Butt
    butt_st = 0b00000000

    # Regular Buttons
    if gpst[4] & 0b100000:
        print("A")
        butt_st |= 0b00000001
    if gpst[4] & 0b1000000:
        print("B")
        butt_st |= 0b00000010
    if gpst[4] & 0b10000:
        print("X")
        butt_st |= 0b00000100
    if gpst[4] & 0b10000000:
        print("Y")
        butt_st |= 0b00001000

    # D Pad Devils
    butt_bits = bin(gpst[4])
    # Cut off the front of the butt
    butt_bits = butt_bits[2:]
    # Take only the last 4 bits
    butt_bits = butt_bits[-4:]
    d_devils = int(butt_bits, 2)
    # If else statements for the d_devils cases 0-7
    if d_devils == 0:
        print("D-Pad Up")
        butt_st |= 0b00000000
    elif d_devils == 1:
        print("D-Pad Up Right")
        butt_st |= 0b00010000
    elif d_devils == 2:
        print("D-Pad Right")
        butt_st |= 0b00100000
    elif d_devils == 3:
        print("D-Pad Down Right")
        butt_st |= 0b00110000
    elif d_devils == 4:
        print("D-Pad Down")
        butt_st |= 0b01000000
    elif d_devils == 5:
        print("D-Pad Down Left")
        butt_st |= 0b01010000
    elif d_devils == 6:
        print("D-Pad Left")
        butt_st |= 0b01100000
    elif d_devils == 7:
        print("D-Pad Up Left")
        butt_st |= 0b01110000

    # TODO: Add RB and LB

    return butt_st

def construct_sticky(gpst):
    """
    Constructs the sticky bits from the gamepad state
    :param gpst: Gamepad state
    :return stick_st: 4 Bytes Representing the Sticky State
    """
    # Blank single byte
    stick_st = 0b00000000
    # OR report[0] with the sticky bits
    stick_st |= gpst[0]
    # Shift the sticky bits to the left by 8 bits
    stick_st = stick_st << 8
    # OR report[1] with the sticky bits
    stick_st |= gpst[1]
    # Shift the sticky bits to the left by 8 bits
    stick_st = stick_st << 8
    # OR report[2] with the sticky bits
    stick_st |= gpst[2]
    # Shift the sticky bits to the left by 8 bits
    stick_st = stick_st << 8
    # OR report[3] with the sticky bits
    stick_st |= gpst[3]

    return stick_st
    

def get_gamepad():
    for device in hid.enumerate():
        # If the device has a product string that is "Logitech Dual Action", return it
        if device['product_string'] == 'Logitech Dual Action':
            return (f"0x{device['vendor_id']:04x}", f"0x{device['product_id']:04x}")
            # return (device['vendor_id']:04x, f"0x{device['product_id']:04x}")
    return None


def main():
    (gp_vid, gp_pid) = get_gamepad()
    if gp_vid is None:
        return

    print(f"Found gamepad with vid:pid {gp_vid}:{gp_pid}")

    gamepad = hid.device()
    gamepad.open(0x046d, 0xc216)
    gamepad.set_nonblocking(1)

    ser = serial.Serial('/dev/tty.usbserial-020ABD5F', 9600)
    ser.close()
    print(ser.name)

    ser.open()

    while True:
        gpst = gamepad.read(64)
        if gpst:
            # for val in gpst:
            #     print(format(val, "08b"), ", ", end="")
            #     # print(format(val, "03d"), ", ", end="")
            #     pass
            # print()
            # Write the 4th element of the gpst to the serial port

            # Construct Button Bits
            butt_st = construct_button_bits(gpst)

            # Construct Sticky
            stick_st = construct_sticky(gpst)

            # Combined Sticky and Button Bits
            stick_butt = butt_st << 16 | stick_st
            stick_butt_bin = bin(stick_butt) # TODO: Chop off first 2, convert to string, send with newline
            ser.write(stick_butt)
            ser.write(b'\n') # TODO: Remove
            print(ser.readline())
            # print(gpst[4] & 0b00101000)
            # if gpst[4] & Buttons.A.value:
            #     print(format(gpst[4], "03d"), "A")


if __name__ == '__main__':
    main()