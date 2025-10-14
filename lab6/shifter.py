import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class Shifter:
  def __init__(self, dataPin, latchPin, clockPin):
    self.dataPin = dataPin
    self.latchPin = latchPin
    self.clockPin = clockPin
    
    
    GPIO.setup(dataPin, GPIO.OUT)
    GPIO.setup(latchPin, GPIO.OUT, initial=0)  # start latch & clock low
    GPIO.setup(clockPin, GPIO.OUT, initial=0)

    def __ping(self,pin):
      GPIO.output(pin,1)
      time.sleep(0)
      GPIO.output(pin,0)

    def shiftByte(self,b):
      for i in range(8):
        GPIO.output(self.dataPin, (b>>1) & 1)
        self.__ping(self.clockPin)
      self.__ping(self.latchPin)
