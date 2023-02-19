import time
import cv2
import numpy as np
from collections import deque
import serial
 
 
min_threshold = 10                      # these values are used to filter our detector.
max_threshold = 200                     # they can be tweaked depending on the camera distance, camera angle, ...
min_area = 50                          # ... focus, brightness, etc.
min_circularity = 0.3
min_inertia_ratio = 0.5
 

cap = cv2.VideoCapture(0)               # '0' is the webcam's ID. usually it's 0/1/2/3/etc. 'cap' is the video object.
cap.set(15, -4)                         # '15' references video's exposure. '-4' sets it.
 
'''
You can also adjust brightness, contrast, and many other video properties using set().
https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html
'''
 
counter = 0                             # script will use a counter to handle FPS.
readings = deque([0, 0], maxlen=10)     # lists are used to track the number of pips.
display = deque([0, 0], maxlen=10)
 
while True:
    ret, im = cap.read()                                    # 'im' will be a frame from the video.
    #start= time.monotonic()
    
    params = cv2.SimpleBlobDetector_Params()                # declare filter parameters.
    params.filterByArea = True
    params.filterByCircularity = True
    params.filterByInertia = True
    params.minThreshold = min_threshold
    params.maxThreshold = max_threshold
    params.minArea = min_area
    params.minCircularity = min_circularity
    params.minInertiaRatio = min_inertia_ratio

    detector = cv2.SimpleBlobDetector_create(params)        # create a blob detector object.

    keypoints = detector.detect(im)                         # keypoints is a list containing the detected blobs.

    # here we draw keypoints on the frame.
    im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imshow("Dice Reader", im_with_keypoints)            # display the frame with keypoints added.

    if counter % 10 == 0:                                   # enter this block every 10 frames.
        reading = len(keypoints)                            # 'reading' counts the number of keypoints (pips).
        readings.append(reading)                            # record the reading from this frame.

        if readings[-1] == readings[-2] == readings[-3]:    # if the last 3 readings are the same...
            display.append(readings[-1])                    # ... then we have a valid reading.
    
        #end = time.monotonic()
        #time = 'start : {:>9.2f}'.format(end-start)
        print (time)
        # if the most recent valid reading has changed, and it's something other than zero, then print it.
        if display[-1] != display[-2] and display[-1] != 0:
            msg = f"{display[-1]}"
            print(msg)
            if __name__ == '__main__':
                ser = serial.Serial('/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0', 9600, timeout=1)
                ser.flush()
                ser.write(msg.encode())
                ser.write(b"\n")
                #ser.write(time.encode())
                #ser.write('start : {:>9.2f}'.format(end-start))
                line = ser.readline().decode('utf-8').rstrip()
                print(line)
                time.sleep(5)
            
            break

    counter += 1

    if cv2.waitKey(1) & 0xff == 27:                          # press [Esc] to exit.
            break


 
'''
# this code prints coordinates of two keypoints. it could be expanded to track individual dice, detect when
# dice are thrown, etc.
 
    try:
        x0 = keypoints[0].pt.x
        y0 = keypoints[0].pt.y
        x1 = keypoints[1].pt.x
        y1 = keypoints[1].pt.y
        msg = f"(x0, y0) = ({x0}, {y0})\n(x1, y1) = ({x1}, {y1})\n\n"
        print(msg)
    except:
        pass
'''
 
cv2.destroyAllWindows()