#Raspberry Pi Pin Query and operation
import RPi.GPIO as GPIO


class pi1_pins(object):
    __ms_out = 23  # GPIO Pin 23
    __ms_in = 24  # GPIO Pin 24
    
    def __init(self):
        #initialization
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(__ms_out, GPIO.OUT)  # Initialize GPI023 as digital output
        GPIO.setup(__ms_in, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # Initialize GPI023 as digital input
        GPIO.output(__ms_out, GPIO.HIGH)  # Set to HIGH

    def mona_switch_ping(self):
        #Query if the face-switch connection on the painting is turned to ON
        return GPIO.input(__ms_in)

