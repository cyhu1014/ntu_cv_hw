#ntu-csie computer vision 2018,fall
#hw8
import cv2
import sys
import random
import matplotlib.pyplot as plt
import numpy as np

def new_img (img):
    new_i = np.zeros((len(img),len(img[0]),3), np.uint8)
    for i in range (len(img)):
        for j in range (len(img[0])):
            new_i[i][j]=img[i][j]
    return new_i

def additive_white_Gaussian_noise(img , amplitude):
    use_img = new_img(img)
    randnum = []
    length = len(use_img) 

    for i in range (length):        
        for j in range (length):
           
            rand = np.random.normal(0, amplitude)
            rand = int(rand)
            randnum.append(rand)
            temp = rand+img[i][j][0]
            if(temp>255):
                temp=255
            elif(temp<0):
                temp=0
            use_img[i][j]= (temp,temp,temp)
  
    return use_img

def salt_and_pepper (img,threshold):
    use_img = new_img(img)
    x = 1/threshold
    x  = int (x)
    length = len(use_img) 
    for i in range (length):
        for j in range (length):
            rand = random.randint(1,x)
            if(rand==1):
                use_img[i][j]=(0,0,0)
            elif (rand==x):
                use_img[i][j]=(255,255,255)
            else:
                use_img[i][j]=img[i][j]
                
   
    return use_img



def box_filter (img,kernel):
    k=0
    if(kernel == 3):
        k=1
    else:
        k=2

    expand_img = expand(img,k)
    new_i = np.zeros((len(img),len(img[0]),3), np.uint8)
    
    for i in range (k,len(img)+k):
        for j in range (k,len(img)+k):
            mean = 0
            for ii in range (i-k,i+k+1):
                for jj in range(j-k,j+k+1):
                    mean+=expand_img[ii][jj][0]
            mean = mean/(kernel*kernel)
            if(mean-int(mean)>=0.5):
                mean = int(mean)+1
            else:
                mean = int(mean)
            new_i[i-k][j-k]=(mean,mean,mean)
    return new_i

def median_filter (img,kernel):
    k=0
    m=0
    if(kernel == 3):
        k=1
        m=5
    else:
        k=2
        m=13

    expand_img = expand(img,k)
    new_i = np.zeros((len(img),len(img[0]),3), np.uint8)
    
    for i in range (k,len(img)+k):
        for j in range (k,len(img)+k):
            median = []
            for ii in range (i-k,i+k+1):
                for jj in range(j-k,j+k+1):
                    median.append(expand_img[ii][jj][0])
            
            new_i[i-k][j-k]=(median[m],median[m],median[m])
    return new_i


def expand (img ,expand_num):
    blank_image = np.zeros((len(img)+expand_num*2,len(img)+expand_num*2,3), np.uint8)
    for i in range (expand_num,len(img)+expand_num):
        for j in range(expand_num,len(img[0])+expand_num):
            blank_image[i][j][0]=img[i-expand_num][j-expand_num][0]
            blank_image[i][j][1]=img[i-expand_num][j-expand_num][0]
            blank_image[i][j][2]=img[i-expand_num][j-expand_num][0]
    return blank_image

def dilation (img):
    img_size = len(img)
    size =2
    exp=expand(img,2)
    new_i = np.zeros((len(img),len(img[0]),3), np.uint8)
    for i in range(size,img_size+size):
        for j in range (size,img_size+size):
            
            iter = 0
            temp_max  = 0
            for ii in range (i-2,i+3):
                for jj in range (j-2,j+3):
                   if(iter!=0 and iter !=4 and iter!=20 and iter!=24 ):
                       temp_max = max(temp_max,exp[ii][jj][0])
                   iter+=1 
            new_i[i-2][j-2][0]=temp_max
            new_i[i-2][j-2][1]=temp_max
            new_i[i-2][j-2][2]=temp_max
    return new_i

    

def erosion (img):
    img_size = len(img)
    size =2
    exp=expand(img,2)
    new_i = np.zeros((len(img),len(img[0]),3), np.uint8)
    for i in range(size,img_size+size):
        for j in range (size,img_size+size):
            iter = 0
            temp_min  = 255
            for ii in range (i-2,i+3):
                for jj in range (j-2,j+3):
                   if(iter!=0 and iter !=4 and iter!=20 and iter!=24 ):
                       temp_min = min(temp_min,exp[ii][jj][0])
                   iter+=1 
            new_i[i-2][j-2][0]=temp_min
            new_i[i-2][j-2][1]=temp_min
            new_i[i-2][j-2][2]=temp_min

    return new_i

def opening (img):
    x = erosion(img)
    x = dilation(x)
    return x

def closing (img):
    x = dilation(img)
    x = erosion(x)
    return x
def SNR (VS,VN):
    length = len(VS)
    mu = 0
    muN = 0
    for i in range (length):
        for j in range (length):
            mu+=VS[i][j][0]
            muN+=VN[i][j][0]-VS[i][j][0]
    mu = mu/length/length
    muN = muN/length/length
    VS_num = 0
    VN_num = 0
    for i in range (length):
        for j in range (length):
            x = VS[i][j][0] - mu
            x = x*x
            VS_num += x
            x = VN[i][j][0]-VS[i][j][0]-muN
            x = x*x
            VN_num += x
    VS_num = VS_num/length/length
    VN_num = VN_num/length/length
    VS_num = np.sqrt(VS_num)
    VN_num = np.sqrt(VN_num)
    ans = 20 * np.log10(VS_num/VN_num)

    return ans




####main start 
img = cv2.imread(sys.argv[1])
#first four noise img
awgn10 = additive_white_Gaussian_noise(img,10)
awgn30 = additive_white_Gaussian_noise(img,30)
sap005 = salt_and_pepper (img ,0.05)
sap01 = salt_and_pepper (img ,0.1)
cv2.imwrite("awgn10.png",awgn10)
cv2.imwrite("awgn30.png",awgn30)
cv2.imwrite ("sap005.png",sap005)
cv2.imwrite ("sap01.png",sap01)

#awgn with box filter
awgn10_b3 = box_filter(awgn10,3)
cv2.imwrite ("awgn10_b3.png",awgn10_b3)
awgn10_b5 = box_filter(awgn10,5)
cv2.imwrite ("awgn10_b5.png",awgn10_b5)
awgn30_b3 = box_filter(awgn30,3)
cv2.imwrite ("awgn30_b3.png",awgn30_b3)
awgn30_b5 = box_filter(awgn30,5)
cv2.imwrite ("awgn30_b5.png",awgn30_b5)
#sap with box filter
sap005_b3 = box_filter(awgn10,3)
cv2.imwrite ("sap005_b3.png",sap005_b3)
sap005_b5 = box_filter(awgn10,5)
cv2.imwrite ("sap005_b5.png",sap005_b5)
sap01_b3 = box_filter(awgn30,3)
cv2.imwrite ("sap01_b3.png",sap01_b3)
sap01_b5 = box_filter(awgn30,5)
cv2.imwrite ("sap01_b5.png",sap01_b5)

#awgn with median_filter
awgn10_m3 = median_filter(awgn10,3)
cv2.imwrite ("awgn10_m3.png",awgn10_m3)
awgn10_m5 = median_filter(awgn10,5)
cv2.imwrite ("awgn10_m5.png",awgn10_m5)
awgn30_m3 = median_filter(awgn30,3)
cv2.imwrite ("awgn30_m3.png",awgn30_m3)
awgn30_m5 = median_filter(awgn30,5)
cv2.imwrite ("awgn30_m5.png",awgn30_m5)
#sap with median filter
sap005_m3 = median_filter(awgn10,3)
cv2.imwrite ("sap005_m3.png",sap005_m3)
sap005_m5 = median_filter(awgn10,5)
cv2.imwrite ("sap005_m5.png",sap005_m5)
sap01_m3 = median_filter(awgn30,3)
cv2.imwrite ("sap01_m3.png",sap01_m3)
sap01_m5 = median_filter(awgn30,5)
cv2.imwrite ("sap01_m5.png",sap01_m5)


x = opening(awgn10)
awgn10_oc = closing(x)
cv2.imwrite("awgn10_oc.png",awgn10_oc)

x = closing (awgn10)
awgn10_co = opening(x)
cv2.imwrite("awgn10_co.png",awgn10_co)

x = opening(awgn30)
awgn30_oc = closing(x)
cv2.imwrite("awgn30_oc.png",awgn30_oc)

x = closing (awgn30)
awgn30_co = opening(x)
cv2.imwrite("awgn30_co.png",awgn30_co)

x = opening(sap005)
sap005_oc = closing(x)
cv2.imwrite("sap005_oc.png",sap005_oc)

x = closing (sap005)
sap005_co = opening(x)
cv2.imwrite("sap005_co.png",sap005_co)

x = opening(sap01)
sap01_oc = closing(x)
cv2.imwrite("sap01_oc.png",sap01_oc)

x = closing (sap01)
sap01_co = opening(x)
cv2.imwrite("sap01_co .png",sap01_co)


