from __future__ import print_function

from RPIO import PWM
import time
import zmq

servo_pin = 27
servo_range = [800, 1400]  # Left, Right (2300 Max, 500 Min)

PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)
servo = PWM.Servo()

def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5555")
    print("Server started.")

    while True:
        message = socket.recv()
        print("Recieved request: %s" % message)
        if message == "unlock":
            unlock_door()
            socket.send(b"Servo Triggered")
        else:
            socket.send(b"Improper request, not unlocking door.")

def unlock_door():
    print('Unlocking...')
    servo.set_servo(servo_pin, servo_range[1])
    time.sleep(2.5)
    print('Locking...')
    servo.set_servo(servo_pin, servo_range[0])
    time.sleep(1)
    servo.stop_servo(servo_pin)
if __name__ == '__main__':
    try:
        server()
    except Exception as e:
        servo.stop_servo(servo_pin)
        print(e)
