#ntu computer vision (2018,fall)
#hw10
import cv2
import sys
import numpy as np
ori = cv2.imread(sys.argv[1])
mask1 = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
mask2 = [[1, 1, 1], [1, -8, 1], [1, 1, 1]]
min_mask = [[2, -1, 2], [-1, -4, -1], [2, -1, 2]]
gaussian_mask = [
		[0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0],
		[0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
		[0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
		[-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
		[-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
		[-2, -9, -23, -1, 103, 178, 103, -1, -23, -9, -2],
		[-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
		[-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
		[0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
		[0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
		[0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0]
	]
dog_mask = [
		[-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1],
		[-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
		[-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
		[-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
		[-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
		[-8, -13, -17, 15, 160, 283, 160, 15, -17, -13, -8],
		[-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
		[-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
		[-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
		[-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
		[-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1]
	]
def mask_3 (ori , mask , threshold):
    ret = np.zeros ((512,512))
    img_len  = len(ori)
    for i in range (1,img_len-1):
        for j in range (1,img_len-1):
            num = 0
            a=0
            for ii in range (i-1,i+2):
                b=0
                for jj in range (j-1,j+2):
                    num+=ori[ii][jj][0]*mask[a][b]
                    b+=1      
                a+=1
            
            if(num > threshold):
                ret[i][j]= 1
            elif(num < -threshold):
                
                ret[i][j]= -1
            else:
                ret[i][j]= 0
    return ret

def mask_3_ans (mat):
    ret = np.zeros ((512,512,3) ,dtype="uint8")
    img_len  = len(mat)
    for i in range (1,img_len-1):
        for j in range (1,img_len-1):
            flag=0
            if(mat[i][j]==1):
                ret[i][j]=(255,255,255)
            else:
                for ii in range (i-1,i+2):
                    for jj in range (j-1,j+2):
                        if(mat[ii][jj]==-1.0):
                            ret[i][j]=(0,0,0)
                            flag=1
                            break
                    if(flag==1):
                            break
                if(flag==0):
                    aret[i][j]=(255,255,255)
                
    return ret


def mask_11 (ori , mask , threshold):
    ret = np.zeros ((512,512) )
    mask_len = len(mask)
    img_len  = len(ori)
    for i in range (5,img_len-5):
        for j in range (5,img_len-5):
            num = 0
            a=0
            
            for ii in range (i-5,i+6):
                b=0
                for jj in range (j-5,j+6):
                    num+=ori[ii][jj][0]*mask[a][b]
                    b+=1

                a+=1
            
            if(num > threshold):
                ret[i][j]= 1
            elif(num < -threshold):
                ret[i][j]= -1
            else:
                ret[i][j]= 0
    
    return ret
def mask_11_ans (mat):
    ret = np.zeros ((512,512,3) ,dtype="uint8")
    img_len  = len(mat)
    
    for i in range (5,img_len-5):
        for j in range (5,img_len-5):
            flag=0
            for ii in range (i-5,i+6):
                for jj in range (j-5,j+6):
                    if(mat[ii][jj]==-1):
                        flag=1
                        break
                if(flag==1):
                        break
                ret[i][j]=(255,255,255)
    return ret

LM1 = mask_3 (ori , mask1 , 15)


cv2.imwrite('Laplace_Mask1_15.png',mask_3_ans (LM1))


'''
cv2.imwrite('Laplace_Mask2_15.png',Laplace_Mask1 (ori , mask2 , 45))

cv2.imwrite('Min_variance_Laplacian_20.png',Laplace_Mask1 (ori , min_mask , 60))
gm = mask_11 (ori , gaussian_mask , 60)
cv2.imwrite('gaussian_mask_3000.png',mask_11_ans(gm))'''