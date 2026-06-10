from keypad import Keypad
from machine import Pin,Timer,PWM,I2C
from ssd1306 import SSD1306_I2C #Import the display driver for the SSD1306
import time

Attempts=3
Update_Buffer=""
secretCode = '24790819'
isLocked = True
inbuffer = "--------"
pwm = PWM('GP28',freq = 50) 
print("State = LOCKED")
pwm.duty_u16(4800)
buzzer=PWM('GP6')
i2c = I2C(1, sda=Pin('GP10'), scl=Pin('GP11'))    # Set up I2C
display = SSD1306_I2C(128, 64, i2c)               # Create display 128x64 pixels





def Alarm(x):               # Sets up the Alarm function
   buzzer.freq(x)           # Sets the Frequency using the 'x'
   buzzer.duty_u16(30000)   # Turns the buzzer on
   time.sleep(0.5)          
   buzzer.duty_u16(0)       

def Unlocked_Display():#sets up the 'Unlocked_Display' function 
   display.fill(0)                      # Clear the display (all black)
   display.ellipse(23,32,12,12,1,True)  # Draw a circle at (23,32), radius = 12
   display.rect(21,21,5,23,0,True)      # Rectangle at (3,3) size=23x5, colour=0 (off)    
   display.text("--------",50,20)       # Display text at (13,0)
   display.text("Unlocked",50,38)
   display.show()                       # Call the show() method last to update display
   
def Locked_Display():#sets up the 'Locked_Display' function 
   display.fill(0)                      # Clear the display (all black)
   display.ellipse(23,32,12,12,1,True)  # Draw a circle at (23,32), radius = 12
   display.rect(12,30,23,5,0,True)      # Rectangle at (3,3) size=23x5, colour=0 (off)
   display.text("--------",50,20)       # Display text at (13,0)
   display.text("Locked",50,38)
   display.text(f'Attempts Left:{Attempts}',0,50)
   Update_Buffer=""
   display.show()                       # Call the show() method last to update display
   time.sleep(1)
def Update_Display(x):#sets up the 'Update_Display' function 
# This function is used to display the current entred code and show that there is only 8 possible digits that can be entered
    global Update_Buffer
    Update_Buffer+=x                     # Adds the value in 'x' to the end of 'Update_Buffer'
    display.fill(0)                      
    display.ellipse(23,32,12,12,1,True)  
    display.rect(12,30,23,5,0,True)      
    display.text(Update_Buffer+"-"*(8-len(Update_Buffer)),50,20)       # Displays the current values in 'Update_buffer' with '-' added to the end up to a length of 8 characters
    display.text("Locked",50,38)
    display.text(f'Attempts Left:{Attempts}',0,50)
    display.show() 
    if len(Update_Buffer)==8:
        Update_Buffer=""                 #Resets 'Update_Buffer'
#def LockOut_Display():
def LockOut_Display(x):
    count=x
    for x in range (0,x):           #counts down from a specified value in 'x'
            display.fill(0)                      
            display.ellipse(23,32,12,12,1,True)  
            display.rect(12,30,23,5,0,True)        
            display.text("ATTEMPTS",50,20)       
            display.text("EXHAUSTED",50,38)
            display.text(f"Online in:{count}",0,50)
            count=count-1           # Subtract 1 from count to mimic a count down
            time.sleep(1)           # Time the micro controller is sleeping
            display.show() 

Locked_Display()

def keyPressed(keyValue):
   global isLocked, inbuffer,Attempts,Update_Buffer        # Global variable 
   if Attempts>0:                           # Checks if all attempts have been used
         if isLocked:
            if keyValue == '#':              # User is trying to unlock
               if inbuffer == secretCode:    # Success only if the code matches
                  isLocked = False
                  print(" - Correct, State = UNLOCKED")
                  pwm.duty_u16(8050)
                  Unlocked_Display()        #Displays the 'Unlocked' State
                  Attempts=3                #Resets Attempts 
                  inbuffer = "--------"     #Resets the inbuffer so the code isnt saved 
               else:
                  print(" - Incorrect code.")
                  Alarm(700)
                  pwm.duty_u16(4800)
                  inbuffer = "--------"                  # Wrong code so reset the buffer
                  Update_Buffer=""
                  Attempts=Attempts-1                 # Subtrats 1 from the total current Attempts 
                  Locked_Display()                    # updates the 'Locked' display
               
            else:                                     # New number needs storing in the buffer:
               inbuffer = inbuffer[1:] + keyValue     # Move buffer to the left and add new value
               print(keyValue, end="")
               Update_Display(keyValue)
         elif keyValue == '*':                        # Unlocked and '*' pressed so change the 
            isLocked = True                           # state to locked.
            print("State = LOCKED")
            pwm.duty_u16(4800)
            Locked_Display()
   elif Attempts==0:
        print('used all attempts')
            
        Alarm(500)
        time.sleep(0.1)
        Alarm(500)
        Attempts=3             # resets the attempts counter back to 3 
        LockOut_Display(20)           #Sets the display into the Lockout phase with a variable to choose a time it will be locked out for
        Locked_Display()        #sets the display back to locked
        Alarm(2000)

# Setup keypad object with the correct pins and with keyPressed() as the callback function
kp = Keypad(rows = (Pin(26), Pin(22), Pin(21), Pin(20)),
            columns = (Pin(19), Pin(18), Pin(17), Pin(16)),
            callback = keyPressed)
