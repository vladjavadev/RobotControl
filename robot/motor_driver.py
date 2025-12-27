import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import sys
import time

print("Python-Interpreter: {}\n".format(sys.version))

# PWM pins for motor speed control
pinPWMA = "P9_14"  # Motor A speed
pinPWMB = "P9_16"  # Motor B speed

# GPIO pins for motor direction control
ina_1 = "P9_25"  # Motor A direction 1
ina_2 = "P9_23"  # Motor A direction 2
inb_1 = "P9_29"  # Motor B direction 1
inb_2 = "P9_27"  # Motor B direction 2

# PWM Parameters
FREQ = 250000
duty_levels = [30, 45, 60, 75, 90]
vModeMin = 0
vModeMax = 4

def get_dc(vMode):
    """Get duty cycle percentage based on velocity mode"""
    if vMode > vModeMin and vMode <= vModeMax:
        dc = duty_levels[vMode] / 100
        return dc
    else:
        return duty_levels[0] / 100

def init():
    """Initialize GPIO and PWM pins"""
    # Setup GPIO pins for direction control
    GPIO.setup(ina_1, GPIO.OUT)
    GPIO.setup(ina_2, GPIO.OUT)
    GPIO.setup(inb_1, GPIO.OUT)
    GPIO.setup(inb_2, GPIO.OUT)
    
    # Initialize all direction pins to LOW
    GPIO.output(ina_1, GPIO.LOW)
    GPIO.output(ina_2, GPIO.LOW)
    GPIO.output(inb_1, GPIO.LOW)
    GPIO.output(inb_2, GPIO.LOW)
    
    # Start PWM with 0% duty cycle
    PWM.start(pinPWMA, 0, FREQ, 0)
    PWM.start(pinPWMB, 0, FREQ, 0)
    print("Motor driver initialized")

def forward(vMode=1):
    """Move both motors forward"""
    dc = get_dc(vMode)
    # Set direction: Motor A forward
    GPIO.output(ina_1, GPIO.HIGH)
    GPIO.output(ina_2, GPIO.LOW)
    # Set direction: Motor B forward
    GPIO.output(inb_1, GPIO.HIGH)
    GPIO.output(inb_2, GPIO.LOW)
    # Set speed
    PWM.set_duty_cycle(pinPWMA, dc * 100)
    PWM.set_duty_cycle(pinPWMB, dc * 100)

def reverse(vMode=1):
    """Move both motors in reverse"""
    dc = get_dc(vMode)
    # Set direction: Motor A reverse
    GPIO.output(ina_1, GPIO.LOW)
    GPIO.output(ina_2, GPIO.HIGH)
    # Set direction: Motor B reverse
    GPIO.output(inb_1, GPIO.LOW)
    GPIO.output(inb_2, GPIO.HIGH)
    # Set speed
    PWM.set_duty_cycle(pinPWMA, dc * 100)
    PWM.set_duty_cycle(pinPWMB, dc * 100)

def turnLeft(dTime, vMode=1):
    """Turn left by running right motor forward, left motor stopped/reversed"""
    dc = get_dc(vMode)
    # Motor A (left) - stop or reverse
    GPIO.output(ina_1, GPIO.LOW)
    GPIO.output(ina_2, GPIO.LOW)
    PWM.set_duty_cycle(pinPWMA, 0)
    # Motor B (right) - forward
    GPIO.output(inb_1, GPIO.HIGH)
    GPIO.output(inb_2, GPIO.LOW)
    PWM.set_duty_cycle(pinPWMB, dc * 100)
    time.sleep(dTime)

def turnRight(dTime, vMode=1):
    """Turn right by running left motor forward, right motor stopped/reversed"""
    dc = get_dc(vMode)
    # Motor A (left) - forward
    GPIO.output(ina_1, GPIO.HIGH)
    GPIO.output(ina_2, GPIO.LOW)
    PWM.set_duty_cycle(pinPWMA, dc * 100)
    # Motor B (right) - stop or reverse
    GPIO.output(inb_1, GPIO.LOW)
    GPIO.output(inb_2, GPIO.LOW)
    PWM.set_duty_cycle(pinPWMB, 0)
    time.sleep(dTime)

def spinLeft(vMode=1):
    """Spin left in place (left motor reverse, right motor forward)"""
    dc = get_dc(vMode)
    # Motor A (left) - reverse
    GPIO.output(ina_1, GPIO.LOW)
    GPIO.output(ina_2, GPIO.HIGH)
    PWM.set_duty_cycle(pinPWMA, dc * 100)
    # Motor B (right) - forward
    GPIO.output(inb_1, GPIO.HIGH)
    GPIO.output(inb_2, GPIO.LOW)
    PWM.set_duty_cycle(pinPWMB, dc * 100)

def spinRight(vMode=1):
    """Spin right in place (left motor forward, right motor reverse)"""
    dc = get_dc(vMode)
    # Motor A (left) - forward
    GPIO.output(ina_1, GPIO.HIGH)
    GPIO.output(ina_2, GPIO.LOW)
    PWM.set_duty_cycle(pinPWMA, dc * 100)
    # Motor B (right) - reverse
    GPIO.output(inb_1, GPIO.LOW)
    GPIO.output(inb_2, GPIO.HIGH)
    PWM.set_duty_cycle(pinPWMB, dc * 100)

def stop():
    """Stop all motors"""
    # Set all direction pins LOW
    GPIO.output(ina_1, GPIO.LOW)
    GPIO.output(ina_2, GPIO.LOW)
    GPIO.output(inb_1, GPIO.LOW)
    GPIO.output(inb_2, GPIO.LOW)
    # Set PWM to 0
    PWM.set_duty_cycle(pinPWMA, 0)
    PWM.set_duty_cycle(pinPWMB, 0)
    time.sleep(0.3)

def cleanup():
    """Clean up GPIO and PWM resources"""
    stop()
    PWM.stop(pinPWMA)
    PWM.stop(pinPWMB)
    PWM.cleanup()
    GPIO.cleanup()
    print("Motor driver cleaned up")

# Example usage
if __name__ == "__main__":
    try:
        init()
        print("Moving forward...")
        forward(vMode=2)
        time.sleep(2)
        
        print("Stopping...")
        stop()
        time.sleep(1)
        
        print("Turning right...")
        turnRight(1.0, vMode=2)
        stop()
        
        print("Moving in reverse...")
        reverse(vMode=2)
        time.sleep(2)
        
        stop()
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    finally:
        cleanup()