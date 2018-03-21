import importlib.util

try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    import FakeRPi.GPIO as GPIO


class GpioOpener(BaseOpener):
    def open_door(self):
        """
        Open the door and turn the LED in the open button on.

        :return:
        """
        GPIO.output(self.OPEN_PIN, 1)
        sleep(1)
        GPIO.output(self.OPEN_PIN, 0)

        #GPIO.output(self.LED_PIN, 1)

    def close_door(self):
        """
        Turn the LED in the open button off.

        :return:
        """
        #GPIO.output(self.LED_PIN, 0)
        pass