import cv2                                #black=0,white=255
import numpy as np
import matplotlib.pyplot as plt
# iterative connected components algorithms 
def iterativeCCA (img):
    row =len(img)
    col = len(img[0])
    label =  [[0 for j in range(col)] for i in range(row)]
    
    #initialize####
    num = 0
    for i in range (0,row):
        for j in range (0,col):
            if(img[i][j]==1):
                num+=1
                label[i][j]=num
            else:
                label[i][j]=0
    ############initialize end

    ############create label2 for neighbor check
    num+=1
    label2 =  [[0 for j in range(col+2)] for i in range(row+2)]
    for i in range (0,row+2):
        label2[0][i]=num
    for i in range (1,row+1):
        label2[i][0]=num
        for j in range (1,col+1):
            if(label[i-1][j-1]==0):
                label2[i][j]=num
            else:
                label2[i][j]=label[i-1][j-1]
        label2[i][col+1]=num
    for i in range (0,row+2):
        label2[row+1][i]=num        
    change=True
    while(change ==True):
        change=False
        for i in range(1,row):
            for j in range(1,col):
                if(label2[i][j]!=num):
                    M=icca_min_neighbors_4connected(label2,i,j)
                    if(label2[i][j]!=M):
                        change=True
                        label2[i][j]=M
        for i in range(row,0,-1):
            for j in range(col,0,-1):
                if(label2[i][j]!=num):
                    M=icca_min_neighbors_4connected(label2,i,j)
                    if(label2[i][j]!=M):
                        change=True
                        label2[i][j]=M              
    ####return label2 to label1
    for i in range (0,row):
        for j in range (0,col):
            if(label2[i+1][j+1]==num):
                label[i][j]=0
            else:
                label[i][j]=label2[i+1][j+1]
    
    return label
               
###find 4 direction min value
def icca_min_neighbors_4connected(label,i,j):
    #q=label[i-1][j-1]
    w=label[i-1][j]
    #e=label[i-1][j+1]
    a=label[i][j-1]
    s=label[i][j]
    d=label[i][j+1]
    #z=label[i+1][j-1]
    x=label[i+1][j]
    #c=label[i+1][j+1]  
    return min(w,a,s,d,x)
    

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
        if(img[i][j][0]<128):
            x[i][j]=0
            img[i][j][0]=0
            img[i][j][1]=0
            img[i][j][2]=0
        else:
            x[i][j]=1
            img[i][j][0]=255
            img[i][j][1]=255
            img[i][j][2]=255
cv2.imwrite('lena_threshold128.jpg',img)

#create 
he = histogram_equalization(Histogram)
print(len(he))
print(len(Histogram))
'''
for i in range (len(he)):
    print(he[i])
'''


plt.plot(H_list)
plt.savefig('Histgram.jpg')


#create connected component and bounding box 



#main end

#code end



                