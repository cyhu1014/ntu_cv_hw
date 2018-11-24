##ntu computer vision 2018 fall
##hw7
import sys
import cv2 
import numpy as np
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
def expand (img ,expand_num):
    blank_image = np.zeros((64+expand_num*2,64+expand_num*2,3), np.uint8)
    for i in range (expand_num,len(img)+expand_num):
        for j in range(expand_num,len(img[0])+expand_num):
            blank_image[i][j][0]=img[i-expand_num][j-expand_num][0]
            blank_image[i][j][1]=img[i-expand_num][j-expand_num][0]
            blank_image[i][j][2]=img[i-expand_num][j-expand_num][0]
    return blank_image
#########################all about yokoi
def yokoi_4connected (img):
    exp_img = expand(img,1)
    yokoi_matrix = np.zeros((len(img),len(img[0])), np.uint8)
    for i in range (1,len(img)+1):
        for j in range (1,len(img[0])+1):
            if(exp_img[i][j][0]==0):
                yokoi_matrix[i-1][j-1]=6
            else:
                yokoi_matrix[i-1][j-1]=f_func(exp_img,i,j)
    return yokoi_matrix
def f_func(img,i,j):
    f_array = ["a","a","a","a"]
    f_array[0]=h_func(img[i][j][0],img[i][j+1][0],img[i-1][j+1][0],img[i-1][j][0])
    f_array[1]=h_func(img[i][j][0],img[i-1][j][0],img[i-1][j-1][0],img[i][j-1][0]) 
    f_array[2]=h_func(img[i][j][0],img[i][j-1][0],img[i+1][j-1][0],img[i+1][j][0])
    f_array[3]=h_func(img[i][j][0],img[i+1][j][0],img[i+1][j+1][0],img[i][j+1][0])
    if (f_array[0]=="r" and f_array[1]=="r" and f_array[2]=="r" and f_array[3]=="r"):
        return 5
    else:
        num = 0
        for i in range (4):
            if(f_array[i]=="q"):
                num+=1
        return num
def h_func (b,c,d,e):
    if(b==c):
        if(d!=b or e!=b):
            return "q"
        elif(d==b and e==b):
            return "r"
    else:
        return "s"
#######################all abut pro
def pair_relationship_operator (matrix):
    
    h = h_pro(matrix)
    
    pq= cal_pq(h)
    return pq
    
def h_pro (matrix):    
    h = np.zeros((len(matrix),len(matrix[0])),np.uint8)
    
    for i in range (len(matrix)):
        for j in range (len(matrix)):
            if(matrix[i][j]==1):
                h[i][j]=1
            elif(matrix[i][j]==6):
                h[i][j]=0
            else:
                h[i][j]=2
    return h   #h :1 for edge ,2 for other point ,0 for background
def cal_pq (h): #1 for p, 2 for q  ,0 for background
    length = len(h)
    e_h = np.zeros((length+2,length+2),np.uint8)
    
    for i in range (1,length+1):
        for j in range (1,length+1):
            e_h[i][j]=h[i-1][j-1]
    pq  = np.zeros((length,length),np.uint8)      
    for i in range (1,length+1):
        for j in range(1,length+1):
            if(e_h[i][j]==0):
                pq[i-1][j-1]=0
            elif(e_h[i][j]==2):
                pq[i-1][j-1]=2
            else :
                
                if(e_h[i-1][j]==1 or e_h[i+1][j]==1 or e_h[i][j-1]==1 or e_h[i][j+1]==1):
                    pq[i-1][j-1]=1
                else:
                    pq[i-1][j-1]=2
    return pq
    
############################
def connected_shrink_operator(img):
    yokoi_matrix=yokoi_4connected(ds_b_img)
    pq = pair_relationship_operator(yokoi_matrix)
    e_img = expand(img,1)
    flag=1
    while(flag==1):
        flag=0
        yokoi_matrix=yokoi_4connected(ds_b_img)
        pq = pair_relationship_operator(yokoi_matrix)
        e_img = expand(img,1)
        for i in range (1,len(e_img)-1):
            for j in range(1,len(e_img[0])-1):
                if(e_img[i][j][0]==255 and pq[i-1][j-1]==1):
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
############################function define end
############################main()
img = cv2.imread(sys.argv[1])
b_img = binarize(img)
ds_b_img = down_sample (b_img)
output=connected_shrink_operator(ds_b_img)
cv2.imwrite("output_img.jpg",output)
