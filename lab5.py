import RPi.GPIO as GPIO
import time
from math import sin, pi

GPIO.setmode(GPIO.BCM)


# Setup for PWM 1
#    1, 2, 3,  4,  5,  6,  7,  8,  9, 10
p = [2, 3, 4, 17, 27, 14, 15, 18, 23, 24]
inputPin = 25

f_pwm = 500     # frequency of PWM (Hz)
f_B = 0.2		# frequency for Brightness (Hz)
phi = [i * pi / 11 for i in range(10)]

pwm = [0]*10
GPIO.setup(inputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
for i in range(10):
	GPIO.setup(p[i], GPIO.OUT)				# sets all pins to be outputs
	pwm[i] = GPIO.PWM(p[i], f_pwm)	# create pwm objects in a list

dc = [0]*10
try:
  for i in range(10):
    pwm[i].start(0)
  while True:
    t = time.time()
    state = GPIO.input(inputPin)	# check pin 25 for direction
    if state == HIGH:
      direction = -1
    else:
      direction = 1 

    for i in range(10):		# calcuate duty cycles and apply them
      dc[i] = 100*((sin((2*pi*f_B*t)-direction*phi[i]))**2)
      pwm[i].ChangeDutyCycle(dc[i])

except KeyboardInterrupt:   # stop gracefully on ctrl-C
  print('\nExiting')

for i in range(10):
	pwm[i].stop()
GPIO.cleanup()
