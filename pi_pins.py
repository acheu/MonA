#Raspberry Pi Pin Query and operation
import RPi.GPIO as GPIO


class pi1_pins(object):
    __ms_out = 16  # GPIO Pin 23
    __ms_in = 18  # GPIO Pin 24
    
    def __init(self):
        #initialization
        GPIO.setmode(GPIO.BOARD)

    def mona_switch_ping(self):
        #Query if the face-switch connection on the painting is turned to ON
	GPIO.setmode(GPIO.BOARD)
	#GPIO.setup(self.__ms_in, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.__ms_out, GPIO.OUT)
	GPIO.output(self.__ms_out, GPIO.HIGH)
	GPIO.setup(self.__ms_in, GPIO.IN)
	return GPIO.input(18)
	#return GPIO.input(self.__ms_in)

