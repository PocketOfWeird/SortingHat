import sys
import time

# Import the PCA9685 module.
import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

# Configure min and max servo pulse lengths
servo_min = 250  # Min pulse length out of 4096
servo_max = 360  # Max pulse length out of 4096

def open_mouth(num_times):
    for i in range(0, num_times):
        pwm.set_pwm(0, 0, servo_min)
        time.sleep(.15)
        pwm.set_pwm(0, 0, servo_max)
        time.sleep(.15)
        pwm.set_pwm(0, 0, servo_min)

open_mouth(2)
#print 'Puppet Script:', str(sys.argv[1])
