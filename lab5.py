import RPi.GPIO as GPIO
import time
from math import sin, pi

GPIO.setmode(GPIO.BCM)

p = 25    		# GPIO pin number
f_pwm = 500     # frequency of PWM (Hz)
f_B = 0.25		# frequency for Brightness (Hz)

GPIO.setup(p, GPIO.OUT)
pwm = GPIO.PWM(p, f_pwm)        # create PWM object

try:
  pwm.start(0)             			# initiate PWM object
  while True:
    t = time.time()
    dc = 100*((sin(2*pi*f_B*t))**2)	# B = sin(2pi*f_B*t)^2
    pwm.ChangeDutyCycle(dc)			# update duty cycle value
except KeyboardInterrupt:   # stop gracefully on ctrl-C
  print('\nExiting')

pwm.stop()
GPIO.cleanup()