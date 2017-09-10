#Testroom
import pi_pins
import time

while (True):
    pi = pi1_pins()
    a = pi.mona_switch_ping()
    print a
    sleep(1)
