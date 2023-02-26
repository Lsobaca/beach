# Untitled - By: saint - Sun Feb 26 2023

import sensor, image, time,pyb

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_vflip(True) # Flips the image vertically

sensor.set_hmirror(True) # Mirrors the image horizontally



RED_LED_PIN = 1
BLUE_LED_PIN = 3

clock = time.clock()

num = 20
while(num):
    clock.tick()
    sensor.skip_frames(time=1000)
    pyb.LED(RED_LED_PIN).on()

    sensor.snapshot().save("users/luis/%s.pgm" %(num))

    num-=1
    pyb.LED(RED_LED_PIN).off()

    print(clock.fps())
    print(num)
