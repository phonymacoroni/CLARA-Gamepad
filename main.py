import hid
import serial
from enum import Enum

class Buttons(Enum):
    A = 0b00101000
    B = 0b01001000
    X = 0b00011000
    Y = 0b10001000


def get_gamepad():
    for device in hid.enumerate():
        # If the device has a product string that is "Logitech Dual Action", return it
        if device['product_string'] == 'Logitech Dual Action':
            return (f"0x{device['vendor_id']:04x}", f"0x{device['product_id']:04x}")
            # return (device['vendor_id']:04x, f"0x{device['product_id']:04x}")
    return None


def main():
    (gp_vid, gp_pid) = get_gamepad()
    print(f"Found gamepad with vid:pid {gp_vid}:{gp_pid}")

    if gp_vid is None:
        return

    gamepad = hid.device()
    gamepad.open(0x046d, 0xc216)
    gamepad.set_nonblocking(1)

    ser = serial.Serial('/dev/tty.usbserial-020ABD5F', 9600)
    ser.close()
    print(ser.name)

    ser.open()

    while True:
        report = gamepad.read(64)
        if report:
            for val in report:
                print(format(val, "08b"), ", ", end="")
                # print(format(val, "03d"), ", ", end="")
                pass
            print()
            # Write the 4th element of the report to the serial port

            if report[4] & 0b100000:
                print("'A' detected, Sending arbitrary number 7 over serial...")
                ser.write(b'7'+b'\n')
                print(ser.readline())
            # print(report[4] & 0b00101000)
            # if report[4] & Buttons.A.value:
            #     print(format(report[4], "03d"), "A")


if __name__ == '__main__':
    main()