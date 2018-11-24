##ntu computer vision 2018 fall
##hw7
import sys
import cv2 
import numpy as np
def binarize (img):
    blank_image = np.zeros((len(img),len(img[0]),3), np.uint8)
    for i in range (len(img)):
        for j in range (len(img[0])):
            if(img[i][j][0]>=128):
                blank_image[i][j][0]=255
                blank_image[i][j][1]=255
                blank_image[i][j][2]=255
            else:
                blank_image[i][j][0]=0
                blank_image[i][j][1]=0
                blank_image[i][j][2]=0
    return blank_image

def down_sample (img):
    blank_image = np.zeros((64,64,3), np.uint8)
    index_i = 0
    index_j = 0
    for i in range (0,512,8):
        for j in range (0,512,8):
            #print(i,j,index_i,index_j)
            blank_image[index_i][index_j][0]=img[i][j][0]
            blank_image[index_i][index_j][1]=img[i][j][0]
            blank_image[index_i][index_j][2]=img[i][j][0]
            index_j+=1
        index_j=0
        index_i+=1
    return blank_image

def mark_interior_border (img):  ##1:b  ,2:i  ,0:background
    interior_border = np.zeros((64,64),dtype=int)
    

    e_img = expand(img,1)
   
    for i in range (1,len(e_img)-1):
        for j in range (1,len(e_img[0])-1):
            if(e_img[i][j][0]==0):
                interior_border[i-1][j-1]=0
            else:
                interior_border[i-1][j-1]=2
                if(e_img[i-1][j][0]==0 or e_img[i+1][j][0]==0 or e_img[i][j-1][0]==0 or e_img[i][j+1][0]==0):
                    interior_border[i-1][j-1]=1
                if(e_img[i-1][j-1][0]==0 or e_img[i+1][j+1][0]==0 or e_img[i+1][j-1][0]==0 or e_img[i-1][j+1][0]==0):
                    interior_border[i-1][j-1]=1
    return interior_border
                
def expand (img ,expand_num):
    blank_image = np.zeros((64+expand_num*2,64+expand_num*2,3), np.uint8)
    for i in range (expand_num,len(img)+expand_num):
        for j in range(expand_num,len(img[0])+expand_num):
            blank_image[i][j][0]=img[i-expand_num][j-expand_num][0]
            blank_image[i][j][1]=img[i-expand_num][j-expand_num][0]
            blank_image[i][j][2]=img[i-expand_num][j-expand_num][0]
    return blank_image   

def pair_relationship_operator (mib):
    pro  = np.zeros((64,64),dtype=int)
    e_mib = np.zeros((66,66),dtype=int)
    for i in range(1,e_mib.shape[0]-1):
        for j in range (1,e_mib.shape[1]-1):
            e_mib[i][j] = mib[i-1][j-1]
    for i in range(1,66-1):
        for j in range (1,66-1):
            if(e_mib[i][j]==0 ):  
                pro[i-1][j-1]=0  #0:background
            elif(e_mib[i][j]==2):
                pro[i-1][j-1]=2 #2:q
            else:
                pro[i-1][j-1]=2
                if(e_mib[i-1][j]==2 or e_mib[i+1][j]==2 or e_mib[i][j-1]==2 or e_mib[i][j+1]==2):
                    pro[i-1][j-1]=1
                if(e_mib[i-1][j-1]==2 or e_mib[i+1][j+1]==2 or e_mib[i+1][j-1]==2 or e_mib[i-1][j+1]==2):
                    pro[i-1][j-1]=1   
    return pro

def connected_shrink_operator(img):
    mib  =mark_interior_border (img)
    marked = pair_relationship_operator (mib)
    #write_txt(pro,"pro.txt")
    #write_txt(mib,"mib.txt")
    e_img = expand(img,1)
    flag=1
    while(flag==1):
        flag=0
        print(1)
        mib  =mark_interior_border (img)
        marked = pair_relationship_operator (mib)
        e_img = expand(img,1)
        for i in range (1,len(e_img)-1):
            for j in range(1,len(e_img[0])-1):
                if(e_img[i][j][0]==255 and marked[i-1][j-1]==1):
                    x=cso_func (e_img[i][j][0],e_img[i][j+1][0],e_img[i-1][j][0],
                                e_img[i][j-1][0],e_img[i+1][j][0],e_img[i+1][j+1][0],
                                e_img[i-1][j+1][0],e_img[i-1][j-1][0],e_img[i+1][j-1][0])
                    if(x==0):
                        img[i-1][j-1]=(0,0,0)
                        e_img[i][j]=(0,0,0)
                        flag=1                  
    return img

def cso_func (x0,x1,x2,x3,x4,x5,x6,x7,x8):
    a1=h(x0,x1,x6,x2)
    a2=h(x0,x2,x7,x3)
    a3=h(x0,x3,x8,x4)
    a4=h(x0,x4,x5,x1)
    r = a1+a2+a3+a4
    if(r==1):
        return 0
    else:
        return 1
def h (b,c,d,e):
    if(b==c and (b!=d or b!=e)):
        return 1
    return 0

def write_txt (matrix,filename):
    text_file = open(filename, "w")
    for i in range (len(matrix)):
        for j in range (len(matrix[0])):
            if(matrix[i][j]==0):
                text_file.write(" ")
            else:
                text_file.write(str(matrix[i][j]))
        text_file.write("\n" )
    text_file.close()

img = cv2.imread(sys.argv[1])
b_img = binarize(img)
ds_b_img = down_sample (b_img)
output_img = connected_shrink_operator(ds_b_img)
cv2.imwrite("lenathin.jpg",output_img)
