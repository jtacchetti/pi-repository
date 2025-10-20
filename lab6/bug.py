import time
import random
import RPi.GPIO as GPIO
from shifter import Shifter
import threading

GPIO.setmode(GPIO.BCM)

class Bug:
	def __init__(self,timestep=0.1,x=3,isWrapOn=False):
		self.timestep = timestep
		self.x = x
		self.isWrapOn = isWrapOn
		self.__shifter = Shifter(23, 24, 25)	# data, latch, clock
		self.__running = False

	def __update_led(self):
		pattern = 1 << self.x
		self.__shifter.shiftByte(pattern)

	def start(self):
		self.__running = True
		try:
			while self.__running:
				self.__update_led()
				step_direction  = random.choice([-1,1])		# decide on a direction
				new_position = self.x + step_direction	# apply direction to new position

				if self.isWrapOn:
					new_position %= 8
				else:
					# Wrap off
					if new_position < 0:
						new_position = 1
					elif new_position >= 8:
						new_position = 6
		
				# update position and delay
				self.x = new_position
				time.sleep(self.timestep)

		except KeyboardInterrupt:
			self.stop()

	def stop(self):
		self.__running = False
		self.__shifter.shiftByte(0)
		GPIO.cleanup()

# SETUP
S1 = 5
S2 = 6
S3 = 13
GPIO.setup(S1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(S2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(S3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

bug = Bug()

last_s2 = GPIO.input(S2)	# initialize s2 value before loop
is_on = False


# MAIN LOOP
try:
	while True:
		s1 = GPIO.input(S1)
		s2 = GPIO.input(S2)
		s3 = GPIO.input(S3)

		if s1 and not is_on:	# s1 switched on
			print(f'BUG SWITCHED ON')
			bug.start()
			is_on = True
		elif not s1 and is_on:	# s1 switched off
			print(f'BUG SWITCHED OFF')
			bug.stop()
			is_on = False


		if s2 != last_s2:		# s2 changed
			if s2: 				# the switch is on
				bug.isWrapOn = not bug.isWrapOn
				print(f'WRAP MODE TOGGLED to {bug.isRrapOn}')
			last_s2 = s2 		# update last_s2


		if s3:					# the switch is on
			bug.timestep = 0.1/3
		else:
			bug.timestep = 0.1

		time.sleep(0.05)

except KeyboardInterrupt:
	bug.stop()
	print(f'Exiting...')
