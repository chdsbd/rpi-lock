from __future__ import print_function

from RPIO import PWM
import time
import sys

from read_process import log

servo_pin = 27
servo_range = [800, 1400]  # Left, Right (2300 Max, 500 Min)

method = sys.argv[1]

PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)
servo = PWM.Servo()

def unlock_door(method=None):
    if method == 'web':
        log('Allow', 'Web Button', 'Web User')
    print('Unlocking...')
    servo.set_servo(servo_pin, servo_range[1])
    time.sleep(4)
    print('Locking...')
    servo.set_servo(servo_pin, servo_range[0])
    time.sleep(2)
    servo.stop_servo(servo_pin)

if __name__ == '__main__':
    try:
        unlock_door(method)
    except Exception as e:
        servo.stop_servo(servo_pin)
        print(e)
