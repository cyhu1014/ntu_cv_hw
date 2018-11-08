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
def expand (img ,expand_num):
    blank_image = np.zeros((64+expand_num*2,64+expand_num*2,3), np.uint8)
    for i in range (expand_num,len(img)+expand_num):
        for j in range(expand_num,len(img[0])+expand_num):
            blank_image[i][j][0]=img[i-expand_num][j-expand_num][0]
            blank_image[i][j][1]=img[i-expand_num][j-expand_num][0]
            blank_image[i][j][2]=img[i-expand_num][j-expand_num][0]
    return blank_image

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
    '''
    if(i==1 and j==4):
        print(img[i-1][j-1][0],img[i-1][j][0],img[i-1][j+1][0])
        print(img[i][j-1][0],img[i][j][0],img[i][j+1][0])
        print(img[i+1][j-1][0],img[i+1][j][0],img[i+1][j+1][0])
        print(f_array[0],f_array[1],f_array[2],f_array[3])'''
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
        

img = cv2.imread(sys.argv[1])
b_img = binarize(img)
ds_b_img = down_sample (b_img)
#cv2.imwrite("binarize.jpg",b_img)
#cv2.imwrite("down_sample_lena.jpg",ds_b_img)
yokoi_matrix = yokoi_4connected(ds_b_img)
text_file = open("yokoi_matrix.txt", "w")
for i in range (len(yokoi_matrix)):
    for j in range (len(yokoi_matrix[0])):
        if(yokoi_matrix[i][j]==6):
            text_file.write(" ")
        else:
            text_file.write(str(yokoi_matrix[i][j]))
    text_file.write("\n" )
text_file.close()
'''
##test code
e_ds_b_img = expand(ds_b_img,1)
text_file = open("e_ds_b_img.txt", "w")
for i in range (len(e_ds_b_img)):
    for j in range (len(e_ds_b_img[0])):
        if(e_ds_b_img[i][j][0]==0):
            text_file.write(" ")
        else:
            text_file.write("1")
    text_file.write("\n" )
text_file.close()
#cv2.imwrite("expand_ds_lena.jpg",e_ds_b_img)
'''

