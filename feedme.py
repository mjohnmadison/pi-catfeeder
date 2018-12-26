import time, sys
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
servoPin=12 #Pin the servo is connected to
GPIO.setup(servoPin, GPIO.OUT)
pwm=GPIO.PWM(servoPin,50) #setting 50 Hz
pwm.start(7) # Position 0 degrees, may need to tweak

def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar
    if progress >= 1:
        progress = 1
    block = int(round(barLength*progress))
    text = "\rFeeding: [{0}] {1:.1f}%".format( "#"*block + "-"*(barLength-block), progress*100)
    sys.stdout.write(text)
    sys.stdout.flush()

# Run the action to feed the cats. Turns feeder 180 degrees to drop food into dish, then back to 0 for refill.

for i in range(0,180): #Turn the hopper to drop the food in dish
    DC=1./18.*(i)+2
    update_progress(i*0.28/100.0) # Update progress bar based on servo posistion. This should max at 50%
    pwm.ChangeDutyCycle(DC)
    time.sleep(.02)
for i in range (180,0,-1): # Return the hopper to filling position
    DC=1/18.*i+2
    update_progress((100 - (i*0.28)) / 100) # Starting at 50%, update the progress bar to 100%
    pwm.ChangeDutyCycle(DC)
    time.sleep(.02)

pwm.stop()
GPIO.cleanup()
update_progress(100) # Set progress bar to 100%
print "\n...Done"
