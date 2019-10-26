import logging
import importlib.util
from time import sleep

from . base_keyboard import BaseKeyboard

try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    import FakeRPi.GPIO as GPIO

log = logging.getLogger(__name__)


class MatrixKeyboard(BaseKeyboard):
    OPEN_PIN = 15
    #LED_PIN = 14
    #BUTTON_PIN = 0
    ROWS = [11, 7, 5, 3]
    COLS = [16, 12, 10, 8]

    MATRIX = {16: {11: 'C', 7: 'B', 5: '0', 3: 'A'},
              12: {11: 'D', 7: '9', 5: '8', 3: '7'},
              10: {11: 'E', 7: '6', 5: '5', 3: '4'},
              8:  {11: 'F', 7: '3', 5: '2', 3: '1'}}

    BOUNCE_TIME = 30
    BUTTONS = {'1': [BOUNCE_TIME, False], '2': [BOUNCE_TIME, False], '3': [BOUNCE_TIME, False],
               '4': [BOUNCE_TIME, False], '5': [BOUNCE_TIME, False], '6': [BOUNCE_TIME, False],
               '7': [BOUNCE_TIME, False], '8': [BOUNCE_TIME, False], '9': [BOUNCE_TIME, False],
               'A': [BOUNCE_TIME, False], '0': [BOUNCE_TIME, False], 'B': [BOUNCE_TIME, False],
               'C': [BOUNCE_TIME, False], 'D': [BOUNCE_TIME, False], 'E': [BOUNCE_TIME, False],
               'F': [BOUNCE_TIME, False]}

    def __init__(self):
        GPIO.setwarnings(False)

        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.OPEN_PIN, GPIO.OUT)
        GPIO.output(self.OPEN_PIN, 0)

        #GPIO.setup(self.LED_PIN, GPIO.OUT)
        #GPIO.output(self.LED_PIN, 0)
        #GPIO.setup(self.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        for pin in self.ROWS:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
        for pin in self.COLS:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def read_buttons(self):
        """
        Buttons have 4 states. They can be:
          1. released
          2. in the process of being pressed (bouncing)
          3. pressed
          4. in the process of being released (bouncing)

        1|        ,-----.
         |     /\/       \/\
        0| ___/             \___
            1   2    3    4   1

        We are only interested in the two bouncing states. These are the key
        press and key release events. This function returns buttons that have
        been released, are in the 4th state. Also we only return the first
        button that got detected because within 30ms no human being should be
        able to more than one. If that's the case, your clearly a robot
        brute-forcing the lock.

        :return:
        """
        pressed = ''
        for k, v in self.BUTTONS.items():
            if self.BUTTONS[k][0] > 0:
                self.BUTTONS[k][0] = self.BUTTONS[k][0] - 1
        for row in self.ROWS:
            GPIO.output(row, 1)
            for col in self.COLS:
                pin = GPIO.input(col)
                # only react if not in bounce timeout
                if self.BUTTONS[self.MATRIX[col][row]][0] == 0:
                    if not self.BUTTONS[self.MATRIX[col][row]][1] and pin:
                        # bounce in
                        self.BUTTONS[self.MATRIX[col][row]][1] = True
                        self.BUTTONS[self.MATRIX[col][row]][0] = self.BOUNCE_TIME
                    elif self.BUTTONS[self.MATRIX[col][row]][1] and not pin:
                        # bounce out
                        self.BUTTONS[self.MATRIX[col][row]][1] = False
                        self.BUTTONS[self.MATRIX[col][row]][0] = self.BOUNCE_TIME
                        pressed = self.MATRIX[col][row]
            GPIO.output(row, 0)
        #if GPIO.input(self.BUTTON_PIN):
        #    pressed.append('O')
        # only return the first detected button release
        # log.debug('buttons released: %s' % ', '.join(pressed))
        return pressed





