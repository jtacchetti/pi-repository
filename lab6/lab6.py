import time
import random
import RPi.GPIO as GPIO
from shifter import Shifter

shifter = Shifter(23, 24, 25)

position = 0 	# initial position at 0
n = 8 			# 8 LEDs
delay = 0.05
print(f'Setup data pins')
try:
	while True:
		pattern = 1 << position
		shifter.shiftByte(pattern)
		print(f'shifting byte')
		step_direction  = random.choice([-1,1])
		new_position = position + step_direction
		print(f'decided on direction')
		if new_position < 0:
			new_position = 1
		elif new_position >= n:
			new_position = n - 2
		print(f'delaying')
		position = new_position
		time.sleep(delay)

except KeyboardInterrupt:
	GPIO.cleanup()
