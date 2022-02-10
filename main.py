import hid
import serial
import time
import yaml

# LOAD SEMI-OPTIONAL CONSTANTS
# load constants from config.yaml file
try:
    with open('config.yaml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.Loader)
except FileNotFoundError:
    print('config.yaml file not found, fix that please')
    cfg = {}
    quit()

DESIRED_GAMEPAD = cfg.get('desired_gamepad')
DESIRED_BAUD = cfg.get('desired_baud')
DESIRED_VID = cfg.get('desired_vid')
DESIRED_PID = cfg.get('desired_pid')
HARDSET_PICO = cfg.get('hardset_pico')
DEADZONE = cfg.get('deadzone')

# Setup Deadzones
dz_2 = (128 - DEADZONE) / 2
dz_c1 = 128 - DEADZONE
dz_c2 = 128 + DEADZONE
dz_3 = (128 + DEADZONE) + dz_2
dz_4 = 255


def construct_button_bits(gpst):
    """
    Constructs the button bits from the gamepad state
    :param gpst: Gamepad State
    :return butt_st: 10 Bits Representing the Button State
    """
    # Blank Butt
    butt_st = 0b00000000

    # Regular Buttons
    if gpst[4] & 0b100000:
        if __debug__: print("A")
        butt_st |= 0b00000001
    if gpst[4] & 0b1000000:
        if __debug__: print("B")
        butt_st |= 0b00000010
    if gpst[4] & 0b10000:
        if __debug__: print("X")
        butt_st |= 0b00000100
    if gpst[4] & 0b10000000:
        if __debug__: print("Y")
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
        if __debug__: print("D-Pad Up")
        butt_st |= 0b00000000
    elif d_devils == 1:
        if __debug__: print("D-Pad Up Right")
        butt_st |= 0b00010000
    elif d_devils == 2:
        if __debug__: print("D-Pad Right")
        butt_st |= 0b00100000
    elif d_devils == 3:
        if __debug__: print("D-Pad Down Right")
        butt_st |= 0b00110000
    elif d_devils == 4:
        if __debug__: print("D-Pad Down")
        butt_st |= 0b01000000
    elif d_devils == 5:
        if __debug__: print("D-Pad Down Left")
        butt_st |= 0b01010000
    elif d_devils == 6:
        if __debug__: print("D-Pad Left")
        butt_st |= 0b01100000
    elif d_devils == 7:
        if __debug__: print("D-Pad Up Left")
        butt_st |= 0b01110000

    # Rear Buttons
    butt_st = butt_st << 2
    if gpst[5] & 0b1:
        if __debug__: print("LB")
        butt_st |= 0b0000000001
    if gpst[5] & 0b10:
        if __debug__: print("RB")
        butt_st |= 0b0000000010

    return butt_st


def chop_stick(stick_st):
    """
    Chops the sticky bit into ranges and returns the binned value
    :param stick_st: 8 bit stick value
    :return: Chopped Stick Value
    """

    if stick_st < dz_2:
        return int(0)
    elif stick_st < dz_c1:
        return int(dz_2)
    elif dz_c2 > stick_st > dz_c1:
        return int(128)
    elif stick_st < dz_3:
        return int(dz_3)
    elif stick_st <= dz_4:
        return int(255)
    else:
        return int(128)


def construct_sticky(gpst):
    """
    Constructs the sticky bits from the gamepad state
    :param gpst: Gamepad state
    :return stick_st: 4 Bytes Representing the Sticky State
    """
    # Blank single byte
    stick_st = 0b00000000
    # OR report[0] with the sticky bits
    stick_st |= chop_stick(gpst[0])
    # Shift the sticky bits to the left by 8 bits
    stick_st = stick_st << 8
    # OR report[1] with the sticky bits
    stick_st |= chop_stick(gpst[1])
    # Shift the sticky bits to the left by 8 bits
    stick_st = stick_st << 8
    # OR report[2] with the sticky bits
    stick_st |= chop_stick(gpst[2])
    # Shift the sticky bits to the left by 8 bits
    stick_st = stick_st << 8
    # OR report[3] with the sticky bits
    stick_st |= chop_stick(gpst[3])

    return stick_st


def get_gamepad():
    for device in hid.enumerate():
        # If the device has a product string that is "Logitech Dual Action", return it
        if device['product_string'] == 'Logitech Dual Action':
            return (f"0x{device['vendor_id']:04x}", f"0x{device['product_id']:04x}")
            # return (device['vendor_id']:04x, f"0x{device['product_id']:04x}")
    return None


def main():
    # If you want to hardset the gamepad the following is not really needed
    (gp_vid, gp_pid) = get_gamepad()
    if gp_vid is None:
        return
    if __debug__: print(f"Found gamepad with vid:pid {gp_vid}:{gp_pid}")

    # Open the Gamepad
    gamepad = hid.device()
    gamepad.open(DESIRED_VID, DESIRED_PID)
    gamepad.set_nonblocking(1)

    # Open the Serial Port
    ser = serial.Serial(HARDSET_PICO, DESIRED_BAUD)
    ser.close()
    if __debug__: print(f"Found serial at {ser.name}" + f" with baud {ser.baudrate}")
    ser.open()

    print("--- Serial Port Opened, Gamepad Connected, Ready for Action ---")

    # Save Previous State
    prev_butt = None

    # Main Loop
    while True:
        # Read in the next gamepad report
        gpst = gamepad.read(64)

        # If the report is not empty
        if gpst:

            # Debug Printing of the report in decimal and binary
            # ---- DEBUG PRINTING HERE ----
            # for val in gpst:
            #     print(format(val, "08b"), ", ", end="")
            #     # print(format(val, "03d"), ", ", end="")
            #     pass
            # print()
            # ---- END DEBUG PRINTING HERE ----

            # Construct Button Bits
            butt_st = construct_button_bits(gpst)

            # Construct Sticky
            stick_st = construct_sticky(gpst)

            # Print sizes of the variables
            # if __debug__: print(f"Button Bits: {butt_st}")
            # if __debug__: print(f"Sticky Bits: {stick_st}")

            # Combined Sticky and Button Bits
            stick_butt = format(butt_st, '010b') + format(stick_st, '032b') + '\n'

            # Combine the button and sticky bits printout
            if __debug__: print(f"Combined: {stick_butt}")

            # Write to Serial
            if stick_butt is not prev_butt:
                # Stick in butt
                byr = ser.write(bytes(stick_butt, 'ascii'))

            # Assign the butt
            prev_butt = stick_butt

            if __debug__: print(f"Bytes Written: {byr}")

            # Print from the serial port buffer, allowing for multiple lines of debug
            while ser.in_waiting:
                print(ser.readline())

            # Wait to ensure no tomfoolery
            # time.sleep(TIME_DELAY)


if __name__ == '__main__':
    main()
