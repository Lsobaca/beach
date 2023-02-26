# Snapshot on Face Detection Example
#
# Note: You will need an SD card to run this example.
#
# This example demonstrates using face tracking on your OpenMV Cam to take a
# picture.

import sensor, image, pyb, gc, machine



RED_LED_PIN = 1
GREEN_LED_PIN = 2
BLUE_LED_PIN = 3


sensor.reset() # Initialize the camera sensor.
sensor.set_contrast(3)
sensor.set_gainceiling(16)
# HQVGA and GRAYSCALE are the best for face tracking.
sensor.set_framesize(sensor.QQVGA)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.skip_frames(time = 2000) # Let new settings take affect.
sensor.set_vflip(True) # Flips the image vertically

sensor.set_hmirror(True) # Mirrors the image horizontally
seri = pyb.UART(1,9600,timeout_char=1000)
seri.init(9600, bits=8, parity=None, stop=1, timeout_char=1000)
gc.enable()

pin9 = pyb.Pin(pyb.Pin.board.PG1,pyb.Pin.OUT_PP)


def min(pmin, a, s):
    global num
    if a < pmin:
        pmin = a
        num = s
    return pmin
num_sub, num_sub_tot= 1,20
num = 0
# Load up a face detection HaarCascade. This is object that your OpenMV Cam
# can use to detect faces using the find_features() method below. Your OpenMV
# Cam has fontalface HaarCascade built-in. By default, all the stages of the
# HaarCascade are loaded. However, You can adjust the number of stages to speed
# up processing at the expense of accuracy. The frontalface HaarCascade has 25
# stages.
face_cascade = image.HaarCascade("frontalface", stages=25)

while(True):

    pyb.LED(RED_LED_PIN).on()
    print("About to start detecting faces...")
    sensor.skip_frames(time = 2000) # Give the user time to get ready.

    pyb.LED(RED_LED_PIN).off()
    print("Now detecting faces!")
    pyb.LED(BLUE_LED_PIN).on()

    diff = 10 # We'll say we detected a face after 10 frames.
    while(diff):
        img = sensor.snapshot()
        # Threshold can be between 0.0 and 1.0. A higher threshold results in a
        # higher detection rate with more false positives. The scale value
        # controls the matching scale allowing you to detect smaller faces.
        faces = img.find_features(face_cascade, threshold=0.5, scale_factor=1.5)

        if faces:
            diff -= 1
            for r in faces:
                img.draw_rectangle(r)
    d0 = img.find_lbp((0,0,img.width(),img.height()))

    pmin = 99999
    img = None
    for s in range(num_sub):
        dist = 0
        for i in range(2,num_sub_tot +1):
            img = image.Image("users/luis/%d.pgm" %i)
            d1 = img.find_lbp((0,0,img.width(),img.height()))
            dist += image.match_descriptor(d0,d1,threshold=50)

    print("Avg dist for subject: %d: %d" %(s,dist/num_sub_tot))
    pmin = min(pmin,dist/num_sub_tot,s)
    print(pmin)


    if pmin <= 11000:
       n = 5
       while(n):
         pyb.LED(GREEN_LED_PIN).on()
         pyb.delay(100)
         pyb.LED(GREEN_LED_PIN).off()
         pyb.delay(100)

         pin9.on()



         n-=1
         pyb.delay(1000)

    pyb.LED(BLUE_LED_PIN).off()
    #seri.write("no")
    pin9.off()
    print("Face detected! Saving image...")
    #seri.print('1')
        #print(img.b_mean())
        #sensor.snapshot().save("example.pgm") # Save Pic.
        #print(img.difference("example2.pgm"))

