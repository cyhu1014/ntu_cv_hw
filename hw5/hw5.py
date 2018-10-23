import cv2
import numpy as np
kernel = [[0,10,10,10 ,0],
          [10,10,10,10,10],
          [10,10,10,10,10],
          [10,10,10,10,10],
          [0,10,10,10,0]]
def expand (img,size):
    expand = []
    img_size=len(img)
    for i in range (size):
        expand.append([])
        for j in range (size*2+img_size):
            expand[i].append(0)
    for i in range (img_size):
        expand.append([])
        for j in range (size):
            expand[size+i].append(0)
        for j in range (img_size):
            expand[size+i].append(img[i][j][0])
        for j in range (size):
            expand[size+i].append(0)
    for i in range (size):
        expand.append([])
        for j in range (size*2+img_size):
            expand[i+img_size+size].append(0)
    return expand

def dilation (img):
    img_size = len(img)
    size =2
    exp=expand(img,2)
    
    for i in range(size,img_size+size):
        for j in range (size,img_size+size):
            if(exp[i][j]!=0 or True):
                iter = 0
                temp_max  = 0
                for ii in range (i-2,i+3):
                    for jj in range (j-2,j+3):
                       if(iter!=0 and iter !=4 and iter!=20 and iter!=24 ):
                           temp_max = max(temp_max,exp[ii][jj])
                       iter+=1 
                img[i-2][j-2][0]=temp_max
                img[i-2][j-2][1]=temp_max
                img[i-2][j-2][2]=temp_max

    

def erosion (img):
    img_size = len(img)
    size =2
    exp=expand(img,2)
    
    for i in range(size,img_size+size):
        for j in range (size,img_size+size):
            if(exp[i][j]!=0 or True):
                iter = 0
                temp_min  = 255
                for ii in range (i-2,i+3):
                    for jj in range (j-2,j+3):
                       if(iter!=0 and iter !=4 and iter!=20 and iter!=24 ):
                           temp_min = min(temp_min,exp[ii][jj])
                       iter+=1 
                img[i-2][j-2][0]=temp_min
                img[i-2][j-2][1]=temp_min
                img[i-2][j-2][2]=temp_min

    

def main ():
    img = cv2.imread("lena.bmp")
    dilation(img)
    cv2.imwrite("dilation_gary_scale.jpg",img)
    erosion(img)
    cv2.imwrite("closing_gary_scale.jpg",img)
    img = cv2.imread("lena.bmp")
    erosion(img)
    cv2.imwrite("erosion_gary_scale.jpg",img)
    dilation(img)
    cv2.imwrite("opening_gary_scale.jpg",img)
   
    



if __name__ == '__main__':
    main()