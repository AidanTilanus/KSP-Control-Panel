from time import sleep

def pulse(pin, duration=0.001):
    """
    Pulse a GPIO pin high for a specified duration.

    Args:
        pin: The GPIO pin to pulse.
        duration: The duration in seconds to keep the pin high (default is 0.1 seconds).
    """
    pin.on()
    sleep(duration)
    pin.off()