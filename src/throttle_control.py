#!/usr/bin/env python

''' This node manages all the control signals sent from the Raspberry Pi to
manipulate vehicle speed. Currently this includes braking and acceleration.'''


import rospy
from std_msgs.msg import Float32, Float64
import RPi.GPIO as gpio
import time


class ThrottleController():
    def __init__(self):
        rospy.init_node("throttle_controller")
        self.rate = 60

        # Commands
        self.brake_pub = rospy.Publisher("~brake/input", Float32, queue_size=10)
        self.accelerator_sub = rospy.Subscriber("~accelerator/input", Float64, self.accelerator_callback)

        # GPIO Pin Setup
        self.ACCELERATOR_PIN = 37
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.ACCELERATOR_PIN, gpio.OUT)
        self.accelerator_pwm = gpio.PWM(self.ACCELERATOR_PIN, 1000)
        self.accelerator_pwm.start(0)

    def spin(self):
        r = rospy.Rate(self.rate)
        while not rospy.is_shutdown():
            self.update()
            r.sleep()

    def update(self):
        # # Testing Accelerator PWM
        # for i in range(0,101):
        #     self.accelerator_pwm.ChangeDutyCycle(i)
        #     print i
        #     time.sleep(0.05)
        #
        # time.sleep(1)
        # self.accelerator_pwm.stop()
        # time.sleep(1)
        #
        # self.accelerator_pwm.start(100)
        # for i in range(100, -1, -1):
        #     self.accelerator_pwm.ChangeDutyCycle(i)
        #     print i
        #     time.sleep(0.05)
        #
        # time.sleep(1)
        pass

    def accelerator_callback(self, msg):
        # Convert fraction into PWM duty cycle (0 -> 100%)
        fraction = msg.data
        if (fraction < 0.):
            fraction = 0.
        if (fraction > 1.):
            fraction = 1.

        duty_cycle = fraction*100.
        print "Running with duty cycle: %f" % duty_cycle
        self.accelerator_pwm.ChangeDutyCycle(duty_cycle)


if __name__ == '__main__':
    try:
        throttle_controller = ThrottleController()
        throttle_controller.spin()
    except rospy.ROSInterruptException:
        pass
    finally:
        gpio.cleanup()
