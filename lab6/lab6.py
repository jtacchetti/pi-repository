import time
import random
import RPi.GPIO as GPIO
from shifter import Shifter

shifter = Shifter(23, 24, 25)

position = 0 	# initial position at 0
n = 8 			# 8 LEDs
delay = 0.05

try:
	while True:
		pattern = 1 << position
		shifter.shiftByte(pattern)
		
		step_direction  = random.choice([-1,1])
		new_position = position + step_direction

		if new_position < 0:
			new_position = 1
		elif new_position >= n:
			new_position = n - 2

		position = new_position
		time.sleep(delay)

except KeyboardInterrupt:
	GPIO.cleanup()
