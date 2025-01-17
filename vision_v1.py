import serial
import cv2
import time

SERIAL_PORT = '/dev/ttyACM0'
SERVO_MIN = 0
SERVO_MAX = 180
SERVO_INITIAL = 90
SERVO_CURRENT = SERVO_INITIAL
CAMERA_INDEX = 1
CASCADE_HAND = 'palm.xml'

serial_conn = serial.Serial(SERIAL_PORT,9600)
print('Vision Initializing. . .')
time.sleep(2)
print('Vision Initialization Complete')

camera = cv2.VideoCapture(CAMERA_INDEX)
print('Camera Available')
#Have to write a script to check and use auxillary/redundant vision or just call out for vision dysfunction

#lets track hands first, easier to move and track probably
hand_casc = cv2.CascadeClassifier(CASCADE_HAND)
print('Cascade Loaded')
#Checks for detection failures must be written, and a plan to reinstall and use/find an alternative must be induced

def hand_track():
    ret, frame = camera.read()
    midline = frame.shape[1]//2
    #Checks if ret is 0, frame unable to be recovered, probably a buffer to restart process or check camera functionality
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    hand = hand_casc.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(50,50))
    if len(hand)>0:
        (x,y,w,h) = hand[0]
        print(f'Hand detected at ({x},{y},{x+w},{y+h})')
        if (midline<x):
            print("Turnin' Right")
            SERVO_CURRENT+=5                 #I dont like the way it might move using this method, I might have to find a way to gradually move it
        elif (midline>(x+w)):
            print("Turnin' Left")
            SERVO_CURRENT-=5
        serial_conn.write(f"{SERVO_CURRENT}\n".encode())        #This is the line that sends the required position of the servo to the arduino.
    time.sleep(2)                           #Lets give a delay so that the bot can move slowly, and jittering is not present in the servo
                                            #This was added because I saw this thing snap its neck like from 180 to 0 and it nearly cut the wire to the camera clean off

if __name__ == "__main__":
    while True:
      hand_track()
    
        
    
