#! ./env/bin/python
'''A drone control interface for the libHubsan serial drone control protocol

To test the controls and see the values to be written over the serial interface
you can run this python file. It will create a pygame window to listen for keyboard
events, and then print the resulting realtime control values to the terminal.

This mimics the behavior of the pyHubsan script without actually sending any values
through the serial interface.

'''
import sys
import unittest
import time
from unittest import mock
import pygame
import serial


def constrain_controls(current_val, minval, maxval, dtype=int):
    '''Constrains controls within a min/max value

    Args:
        current_val: The value to constrain
        minval: Minimum allowed value
        maxval: Maximum allowed value
        dtype: The desired datatype of the variable.

    Returns:
        (number): A value contrained to the input parameters
    '''
    c = dtype(current_val)
    if current_val < minval:
        c = minval
    elif current_val > maxval:
        c = maxval
    return c


class DroneController(object):
    '''An object which can be used to send serial commands to the drone to change control values
    '''
    CTRL_MAX = 255
    CTRL_MID = 128
    CTRL_DIV = 3

    def __init__(self, ser, trim_yaw=0, trim_pitch=0, trim_roll=0):
        '''Initialize the object with trim and serial object

        Args:
            ser: The serial object from the pyserial library which is used to send commands
            trim_yaw: The default trim for the yaw of the drone. Must be in the range (-128, 128)
            trim_pitch: The default trim for the yaw of the drone. Must be in the range (-128, 128)
            trim_roll: The default trim for the yaw of the drone. Must be in the range (-128, 128)
        '''
        self.trims = [trim_yaw, trim_pitch, trim_roll]
        for v in self.trims:
            if v < -128 or v > 128:
                raise ValueError("Trim values must be in the range (-128, 128). Got {}".format(v))
        self.ser = ser
        if not isinstance(self.ser, serial.Serial):
            raise ValueError("ser argument must be an instance of serial. Serial class.")

        # [throttle, yaw, pitch, roll]
        mid = DroneController.CTRL_MID
        self.ctrl_params = [0, mid, mid, mid]
        self.last_sent = self.ctrl_params.copy()

    def throttle(self):
        '''Return the current throttle value'''
        return self.ctrl_params[0]

    def yaw(self):
        '''Return the current raw yaw value with trim'''
        return self.ctrl_params[1] + self.trims[0]

    def pitch(self):
        '''Return the current pitch yaw value with trim'''
        return self.ctrl_params[2] + self.trims[1]

    def roll(self):
        '''Return the current raw roll value with trim'''
        return self.ctrl_params[3] + self.trims[2]

    def reset_controls(self):
        '''Resets all controls'''
        mid = DroneController.CTRL_MID
        self.ctrl_params = [0, mid, mid, mid]

    def print_trims(self):
        '''Prints the trim values in a human-readable format'''
        pass
        # print()
        # print("Yaw Trim: {}, Pitch Trim: {}, Roll Trim: {}".format(
        #                                             self.trims[0], self.trims[1], self.trims[2]))

    def update_control_values(self, keyboard_events):
        move_throttle = 0
        ctrl_mid = DroneController.CTRL_MID
        ctrl_max = DroneController.CTRL_MAX
        ctrl_div = DroneController.CTRL_DIV
        for event in keyboard_events:
            if event.type == pygame.QUIT:
                pass
                # DO SOMETHING WITH QUIT
                # If you don't want to exit...I won't modify for now
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # KILL ENGINE AND RESET CONTROLS
                    self.reset_controls()  # Reset controls to default values
                if event.key == pygame.K_w:
                    move_throttle = 1
                if event.key == pygame.K_s:
                    move_throttle = -1
                if event.key == pygame.K_a:
                    self.ctrl_params[1] = ctrl_mid - (ctrl_max-self.trims[0])/ctrl_div
                if event.key == pygame.K_d:
                    self.ctrl_params[1] = ctrl_mid + (ctrl_max-self.trims[0])/ctrl_div
                if event.key == pygame.K_UP:
                    self.ctrl_params[2] = ctrl_mid - (ctrl_max - self.trims[1])/ctrl_div
                if event.key == pygame.K_DOWN:
                    self.ctrl_params[2] = ctrl_mid + (ctrl_max - self.trims[1])/ctrl_div
                if event.key == pygame.K_LEFT:
                    self.ctrl_params[3] = ctrl_mid + (ctrl_max - self.trims[2])/ctrl_div
                if event.key == pygame.K_RIGHT:
                    self.ctrl_params[3] = ctrl_mid - (ctrl_max - self.trims[2])/ctrl_div
                if event.key == pygame.K_q:
                    smooth = toggleSmoothing(smooth)
                if event.key == pygame.K_COMMA:
                    self.trims[0] -= 1
                    self.print_trims()
                if event.key == pygame.K_PERIOD:
                    self.trims[0] += 1
                    self.print_trims()
                if event.key == pygame.K_o:
                    self.trims[1] += 1
                    self.print_trims()
                if event.key == pygame.K_l:
                    self.trims[1] -= 1
                    self.print_trims()
                if event.key == pygame.K_SEMICOLON:
                    self.trims[2] += 1
                    self.print_trims()
                if event.key == pygame.K_k:
                    self.trims[2] -= 1
                    self.print_trims()
                # No flipping here...
                # if (event.key == pygame.K_e):
                    # flip(ser,def_p,throttle,"2")
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    move_throttle = 0
                if event.key == pygame.K_s:
                    move_throttle = 0
                if event.key == pygame.K_a:
                    self.ctrl_params[1] = ctrl_mid
                if event.key == pygame.K_d:
                    self.ctrl_params[1] = ctrl_mid
                if event.key == pygame.K_UP:
                    self.ctrl_params[2] = ctrl_mid
                if event.key == pygame.K_DOWN:
                    self.ctrl_params[2] = ctrl_mid
                if event.key == pygame.K_LEFT:
                    self.ctrl_params[3] = ctrl_mid
                if event.key == pygame.K_RIGHT:
                    self.ctrl_params[3] = ctrl_mid

        # Constrain the control values to a rational range
        self.ctrl_params[0] += move_throttle
        self.ctrl_params[0] = constrain_controls(self.ctrl_params[0], 0, ctrl_max)

    def send_control_signals(self):
        ctrl = self.ctrl_params.copy()
        ctrl[1] = constrain_controls(ctrl[1] + self.trims[0], 0, DroneController.CTRL_MAX)
        ctrl[2] = constrain_controls(ctrl[2] + self.trims[1], 0, DroneController.CTRL_MAX)
        ctrl[3] = constrain_controls(ctrl[3] + self.trims[2], 0, DroneController.CTRL_MAX)

        for i in range(len(ctrl)):
            if ctrl[i] != self.last_sent[i]:
                self.ser.write('0')  # Send control flag
                self.ser.write(chr(ctrl[i]))
                sys.stdout.write("\r%03d:%03d:%03d:%03d" % (ctrl[0], ctrl[1], ctrl[2], ctrl[3]))
                sys.stdout.flush()
                self.last_sent[i] = ctrl[i]

        # No support yet for smoothing
        # if smooth != last_s:
        #     last_s = smooth
        #     ser.write('4') # Control flag: Toggle Smoothing
        #     print(str(smooth))


class DroneControllerTest(unittest.TestCase):

    def test_controls(self):
        pygame.init()
        window = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Mock Test Controller")
        clock = pygame.time.Clock()
        mockser = mock.Mock(spec=serial.Serial)
        dc = DroneController(mockser)
        while True:
            time.sleep(.2)
            clock.tick(200)
            dc.update_control_values(pygame.event.get())
            dc.send_control_signals()

if __name__ == "__main__":
    unittest.main()
