import time
import random
import RPi.GPIO as GPIO
from shifter import Shifter

shifter = Shifter(23, 24, 25)	# data, latch, clock

position = 0 	# initial position at 0
n = 8 			# 8 LEDs
delay = 0.05	# delay 0.05 sec for each step
try:
	while True:
		pattern = 1 << position
		shifter.shiftByte(pattern)
		step_direction  = random.choice([-1,1])		# decide on a direction
		new_position = position + step_direction	# apply direction to new position

		# correct position if out-of-bounds
		if new_position < 0:
			new_position = 1
		elif new_position >= n:
			new_position = n - 2
		
		# update position and delay
		position = new_position
		time.sleep(delay)

except KeyboardInterrupt:
	GPIO.cleanup()
