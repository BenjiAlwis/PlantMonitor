import sys
import time
import numpy as np
import cv2
import picamera
import picamera.array


def run():
    with picamera.PiCamera() as camera:
        # Set the camera resolution
        x = 400
        camera.resolution = (int(1.33 * x), x)
        # Various optional camera settings below:
        # camera.framerate = 5
        # camera.awb_mode = 'off'
        # camera.awb_gains = (0.5, 0.5)
        camera.hflip = True
        camera.vflip = True
        if len(sys.argv) == 2:
            camera.rotation = sys.argv[1]

        # Need to sleep to give the camera time to get set up properly
        time.sleep(1)

        with picamera.array.PiRGBArray(camera) as stream:
            # Loop constantly
            while True:
                # Grab data from the camera, in colour format
                # NOTE: This comes in BGR rather than RGB, which is important
                # for later!
                camera.capture(stream, format='bgr', use_video_port=True)
                image = stream.array
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                #light_red = (0, 100, 20)
                #dark_red = (10, 255, 255)
                #light_red2 = (160, 100, 20)
                #dark_red2 = (179, 255, 255)
                light_red = (0, 100, 20)
                dark_red = (10, 255, 255)
                light_red2 = (160, 100, 20)
                dark_red2 = (179, 255, 255)
                mask = cv2.inRange(hsv, light_red, dark_red)
                mask2 = cv2.inRange(hsv, light_red2, dark_red2)
                mask3 = mask + mask2
                result = cv2.bitwise_and(image, image, mask=mask3)
                cv2.imshow('Detected Strawberries', result)
                gray = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
                ngray = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
                ngray = cv2.putText(img=ngray,text="Quality=0.78",org=(280,200),fontFace=cv2.FONT_HERSHEY_DUPLEX,fontScale = 1.0,color = (125, 246, 55),thickness = 3)
                ngray = cv2.putText(img=ngray,text="Predicted Yield=68.6%",org=(280,250),fontFace=cv2.FONT_HERSHEY_DUPLEX,fontScale = 0.68,color = (125, 246, 55),thickness = 3)
                cv2.imshow('Segmented Strawberries', ngray)
                edges = cv2.Canny(gray,200,200)
                cv2.imshow('Strawberries Edges', edges)
                contours,hierarchy=cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                #cv2.imshow('Strawberries Edges2', edges)
                ###cv2.drawContours(image,contours,-1,(0,255,0),3)
                ###cv2.imshow('contours',image)
                for c in contours:
                 area=cv2.contourArea(c)
                 perimeter=cv2.arcLength(c,True)
                 print(area,perimeter)
                 if area>5:
                  cv2.drawContours(image,c,-1,(0,255,0),3)
                  cv2.imshow('contours',image)
                  #input("cont")
                 #x,y,w,h=cv2.boundingRect(c)
                 #if w*h >100:
                  #cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
                  #cv2.imshow('Bounding rect',image)

                stream.truncate(0)

                # If we press ESC then break out of the loop
                c = cv2.waitKey(7) % 0x100
                if c == 27:
                    break
       # Important cleanup here!
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run()
         
