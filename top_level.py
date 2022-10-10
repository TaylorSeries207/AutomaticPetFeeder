from flask import Flask, render_template_string, request 
from time import sleep
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
from scale_1kg import weighting
from app import data_return


GPIO_pins = (14, 15, 18) # Microstep Resolution MS1-MS3 -> GPIO Pin
direction= 20       # Direction -> GPIO Pin
step = 21      # Step -> GPIO Pin

# Declare an named instance of class pass GPIO pins numbers
mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")

def top_level_func():
    
    recent_val,length=data_return()
    next_len=length
    
    
   
    
    
    while (1):
        recent_val,length=data_return()
        
        #print ("recent val=",recent_val)
        #print ("length=",length)
       
        
        if (length==0 and next_len==0):
            next_len=next_len+1
            print ("next length=",next_len)
        elif (length==0 and next_len!=0):
            next_len=1
            
        elif (length==1):
            next_len=length+1
            
        elif (next_len==length):
            next_len=next_len+1;
            val,leng=data_return()
            print ("top_level recent val=",val)
            print ("top_level length=",leng)
           
            print("open gate")
            mymotortest.motor_go(True, "Full" , 100,5*.0004, False, .05)
        
            
           # while (weighting()<val):
                #print ("enter while loop")
                #print(weighting())
        
                #print("Rotating Clockwise")
                #break
            if (weighting()>=int(val)):
                print("close gate")
                mymotortest.motor_go(False, "Full" , 100,5*.0004, False, .05)
def test():
    while (1):
        recent_val,length=data_return()
        print ("top_level test recent_val=",recent_val)
        print ("top_level test length=",length)
    
if __name__ == "__main__":
    #test()
    top_level_func()