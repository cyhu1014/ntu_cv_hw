##ntu computer vision hw4
##Write programs which do binary morphological dilation, erosion,
# opening, closing, and hit-and-miss transform on a binary image 
import cv2
import sys
octogon = [
	[0,1,1,1,0],
	[1,1,1,1,1],
	[1,1,1,1,1],
	[1,1,1,1,1],
	[0,1,1,1,0]
]

def binarize(img):
    img_bin = []
    for i in range (0,len(img)):
        img_bin.append([])
        for j in range (0,len(img)):
            if(img[i][j][0]<128):
                img_bin[i].append(0)
                img[i][j][0]=0
                img[i][j][1]=0
                img[i][j][2]=0
            else:
                img_bin[i].append(1)
                img[i][j][0]=255
                img[i][j][1]=255
                img[i][j][2]=255
    return img_bin

def dilation (bin,img):

    dila = []    
    for i in range (len(bin)+4):
        dila.append([])
        for j in range (len(bin)+4):
            dila[i].append(0)

    for i in range (2,len(bin)+2):
        for j in range (2,len(bin)+2):
            if(bin[i-2][j-2]==1 ):
                iteration=0
                for ii in range (i-2,i+3):
                    for jj in range (j-2,j+3):
                        if(iteration!=0 and iteration!=4 and iteration!=20 and iteration!=24 ):
                            dila[ii][jj]=1        
                        iteration+=1 
    for i in range (2,len(bin)+2):
        for j in range (2,len(bin)+2):
            if(dila[i][j]==1):
                img[i-2][j-2][0]=255
                img[i-2][j-2][1]=255
                img[i-2][j-2][2]=255
            else:
                img[i-2][j-2][0]=0
                img[i-2][j-2][1]=0
                img[i-2][j-2][2]=0
    
def erosion (bin,img):
    img_expand = []
    img_expand.append([])
    img_expand.append([])
    for i in range (len(bin)+4):
        img_expand[0].append(0)
        img_expand[1].append(0)
    for i in range (len(bin)):
        img_expand.append([])
        img_expand[i+2].append(0)
        img_expand[i+2].append(0)
        for j in range (len(bin)):
            img_expand[i+2].append(bin[i][j])
        img_expand[i+2].append(0)
        img_expand[i+2].append(0)
    img_expand.append([])
    img_expand.append([])
    for i in range (len(bin)+4):
        img_expand[len(bin)+2].append(0)
        img_expand[len(bin)+3].append(0)
    ero = []
    for i in range (len(bin)):
        ero.append([])
        for j in range(len(bin[0])):
            ero[i].append(0)

    for i in range (2,len(bin)+2):
        for j in range (2,len(bin)+2):
            iteration=0
            num=0
            for k in range (i-2,i+3):
                for l in range (j-2,j+3):
                    if(iteration!=0 and iteration!=4 and iteration!=20 and iteration!=24 ):
                        if(img_expand[k][l]==1):
                            num+=1
                    iteration+=1
            if(num>=21): 
                ero[i-2][j-2]=1
    for i in range (len(bin)):
        for j in range (len(bin)):
            if(ero[i][j]==1):
                img[i][j][0]=255
                img[i][j][1]=255
                img[i][j][2]=255
            else:
                img[i][j][0]=0
                img[i][j][1]=0
                img[i][j][2]=0     

def hit_and_miss(bin,img):
    inv_bin = []
    A = []
    inv_A = []
    for i in range (len(bin)):
        inv_bin.append([])
        A.append([])
        inv_A.append([])
        for j in range(len(bin)):
            if(bin[i][j]==1):
                inv_bin[i].append(0)
            else:
                inv_bin[i].append(1)
            A[i].append(0)
            inv_A[i].append(0)
            
    ##A with J
    for i in range (len(A)-1):
        for j in range (1,len(A)):
            if(bin[i+1][j]==1 and bin[i][j]==1 and bin[i][j-1]==1):
                A[i][j]=1
    ##A with K
    for i in range (1,len(A)):
        for j in range (1,len(A)-1):
            if(inv_bin[i-1][j]==1 and inv_bin[i-1][j+1]==1 and inv_bin[i][j+1]==1):
                inv_A[i][j]=1

    for i in range (len(bin)):
        for j in range (len(bin)):
            if(inv_A[i][j]==1 and A[i][j]==1):
                img[i][j][0]=255
                img[i][j][1]=255
                img[i][j][2]=255
            else:
                img[i][j][0]=0
                img[i][j][1]=0
                img[i][j][2]=0     
    
    
    
    
def main(args):
    
    ##create dilation erosion closing and open
    img = cv2.imread("lena.bmp")  
    img_bin=binarize(img)  
    cv2.imwrite("b.jpg",img)
    dilation (img_bin,img)
    cv2.imwrite("dilation.jpg",img)
    img_bin=binarize(img)
    erosion(img_bin,img)
    cv2.imwrite("closeing.jpg",img)
    img = cv2.imread("lena.bmp")
    img_bin=binarize(img)
    erosion(img_bin,img)
    cv2.imwrite("erosion.jpg",img)
    img_bin=binarize(img)
    dilation (img_bin,img)
    cv2.imwrite("opening.jpg",img)
    
    ##hit and miss transform
    img =cv2.imread("lena.bmp")
    img_bin=binarize(img)
    hit_and_miss(img_bin,img)
    cv2.imwrite("hitandmiss.jpg",img)


    

if __name__ == '__main__':
    main(sys.argv)