import cv2                                #black=0,white=255
import numpy as np
import matplotlib.pyplot as plt


def histogram_equalization (histogram):
    he =[]
    s = []
    for i in range (256):
        he.append(0)
        s.append(0)
    for i in range (256):
        for j in range (i):
            he[i]+=histogram[j]
        s[i]=255*he[i]/(512*512)
    return s

# main start

#create threshold 128 image      
img = cv2.imread('lena.bmp')
Histogram= []
H_list = []
for i  in range (0,256):
    H_list.append(0)
x= [[0 for j in range(len(img[0]))] for i in range(len(img))]
for i in range (0,512):
    for j in range (0,512):
        H_list[img[i][j][0]]+=1
        Histogram.append(img[i][j][0])

#create 
he = histogram_equalization(H_list)

histogram_e = []
he_list=[]
for i in range (256):
    he_list.append(0)
for i in range  (0,512):
    for j in range (0,512):
        img[i][j]=he[int(img[i][j][0])]
for i in range  (0,512):
    for j in range (0,512):
        he_list[int(img[i][j][0])]+=1
        histogram_e.append(int(img[i][j][0]))

    
cv2.imwrite("lena_he.jpg",img)

plt.hist(histogram_e,bins=256)

plt.savefig("hist_equl.jpg")
plt.clf()
plt.hist(Histogram,bins=256)
plt.savefig("hist.jpg")


#create connected component and bounding box 

#main end

#code end



                