# Untitled - By: saint - Sun Feb 26 2023

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)



def min(pmin, a, s):
    global num
    if a < pmin:
        pmin = a
        num = s
    return pmin


def compareimages(img):
    d0 = img.find_lbp((0,0,img.width(),img.height()))

    img = None
    pmin = 999999


    for s in range(num_sub):
        dist = 0
        for i in range(2,num_sub_tot +1):
            img = image.Image("users/luis/%d.pgm" %i)
            d1 = img.find_lbp((0,0,img.width(),img.height()))
            dist += image.match_descriptor(d0,d1,threshold=50)

        print("Avg dist for subject: %d: %d" %(s,dist/num_sub_tot))
        pmin = min(pmin,dist/num_sub_tot,s)
        print(pmin)
        return pmin
