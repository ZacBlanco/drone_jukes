#! ./env/bin/python
# ---------------------------------------------------------------
# Hubsan X4 H107D - Python head-end for Arduino Hubsan Controller
# ---------------------------------------------------------------
# v0.1.1 - 2018-03-20 - Zac Blanco, Zohaib Zahid
# ---------------------------------------------------------------
import sys
import configparser
import serial
import pygame
from drone_controller import DroneController

from serial.tools import list_ports
from time import sleep


def toggleSmoothing(smooth):
    if smooth == 0:
        smooth = 1
    else:
        smooth = 0
    return smooth


def flip(ser, def_dir, throttle, axis):

    # Blip the throttle...
    ser.write('0')
    ser.write(chr(254))
    sleep(0.2)
    # Pitch back momentarily...
    ser.write(axis)
    ser.write(chr(254))
    sleep(0.2)
    # ..then Pitch forward hard.
    ser.write(axis)
    ser.write(chr(1))
    sleep(0.5)
    # Return controls to default and compensate throttle momentarily...
    ser.write(axis)
    ser.write(chr(def_dir))
    ser.write('0')
    ser.write(chr(255))
    sleep(1)
    # ...and finally even out the throttle.
    ser.write('0')
    ser.write(chr(throttle))


def main():

    print("\nHubsan X4 H107L - Python head-end for Arduino Hubsan Controller.")
    print("----------------------------------------------------------------")

    print("> Loading config settings...\n")
    config = configparser.ConfigParser()
    config.read('hubsan.config')

    print("> Detecting COM ports...\n")
    ports = list()
    i = 0
    for port in list_ports.comports():
        print("  %s: [%s] %s" % (str(i), port[0], port[1]))
        ports.append(port)
        i += 1
    if len(ports) == 0:
        print("Error: No Arduino Serial ports detected! Try reconnecting the USB cable.")
        sys.exit(1)
    portnum = input("\n  Enter the number of the desired COM port: ")
    comport = ports[int(portnum)]
    print("\n- [%s] Selected." % comport[0])

    print("\n> Opening Serial port...")
    ser = serial.Serial(comport[0], 115200, timeout=1)
    print(" - Successful.")

    print("\n> TERMINAL STATUS:")
    print("------------------")
    while True:
        line = ser.readline().strip()
        if line != "":
            print(" %s" % line)
        if (line == "** Status: READY. **"):
            break

    print("\n> INITIALIZING CONTROL INTERFACE.")
    print("---------------------------------")
    dc = DroneController(ser, )
    # Set up control values
    # def_t = throttle = 0
    # def_y = yaw = 128 + int(config['flight']['yaw_trim'])
    # def_p = pitch = 128 + int(config['flight']['pitch_trim'])
    # def_r = roll = 128 + int(config['flight']['roll_trim'])
    print(" Post-Trim Flight Defaults = Yaw: %s Pitch: %s Roll: %s" % (str(yaw),
                                                                       str(pitch), str(roll)))
    yt = int(config['flight']['yaw_trim'])
    pt = int(config['flight']['pitch_trim'])
    rt = int(config['flight']['roll_trim'])
    dc = DroneController(ser, yt, pt, rt)
    smooth = 0

    # Set up PyGame event handlers and event loop
    pygame.init()
    window = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Hubsan X4 H107L Python Controller v0.1")
    clock = pygame.time.Clock()

    print("\nTHR:YAW:PIT:ROL\n---------------")

    while True:

        clock.tick(200)  # Lock framerate of the input for consistency.
        dc.update_control_values(pygame.event.get())
        dc.send_control_signals()
        # See if the control value has changed, and if so, send a control message.

if __name__ == '__main__':
    main()
