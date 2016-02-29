import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)

p = GPIO.PWM(13, 50)

p.start(7)
print "STARTED"

for i in range(0, 11):
    print "PWM duty cycle of: ", i
    p.ChangeDutyCycle(i)
    nextdc = i + 1
    raw_input("Hit return to go to next DC of {}".format(nextdc))
p.stop()
GPIO.cleanup()

