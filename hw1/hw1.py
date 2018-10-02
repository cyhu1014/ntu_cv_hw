import cv2
import numpy as np
img = cv2.imread('lena.bmp')
img2 = cv2.imread('lena.bmp')
img3 = cv2.imread('lena.bmp')
##right-side-left
for i in range (0,512):
    for j in range (0,256):
        img[i][j]=img2[i][511-j]
        img[i][511-j]=img2[i][j]
cv2.imwrite('lena_right-side-left.jpg',img)
##upside down
for j in range (0,512):
    for i in range (0,256):
        img[i][j]=img2[511-i][j]
        img[511-i][j]=img2[i][j]
cv2.imwrite('lena_upside-down.jpg',img)
#diagonally-mirrored
for i in range (0,512):
    for j in range (0,256):
        img3[i][j]=img[i][511-j]
        img3[i][511-j]=img[i][j]
cv2.imwrite('lena_diagonally-mirrored.jpg', img3)