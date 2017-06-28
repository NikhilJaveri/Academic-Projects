import numpy as np
from math import *
from PIL import Image
import os

def DCT3(Image, Kernel_dim):
        
        # Construct DCT Coefficient table

        u = Kernel_dim[0]
        v = Kernel_dim[1]
            
        DCT_table = np.zeros(shape=(u,v), dtype = 'float64')
            
        for m in range(u):
                for n in range(v):
                        if (m == 0):
                                DCT_table[m,n] = sqrt(1.0/u)
                        elif (m > 0):
                                DCT_table[m,n] = (sqrt(2.0/u))*(cos((pi*((2*n)+1)*m)/(2*u)))

        [row, col, depth] = Image.shape

        DCT_image = np.zeros(shape=(row,col,depth), dtype = 'float64')

        DCT_block = np.zeros(shape=(u,v), dtype = 'float64')

        Image_block = np.zeros(shape=(u,v), dtype = 'float64')

        for k in range(depth):
                for m in range(0,row,u):
                        for n in range(0,col,v):

                                # Retrieve the image blocks of dimension u x v and convert them to DCT equivalents

                                for x in range(u):
                                        for y in range(v):
                                                Image_block[x,y] = Image[m+x,n+y,k]

                                DCT_block = Mat_multiply(DCT_table, Mat_multiply(Image_block, Mat_transpose(DCT_table)))

                                for x in range(u):
                                        for y in range(v):
                                                DCT_image[m+x,n+y,k] = DCT_block[x,y]

        return DCT_image

def DCT_table(Kernel_dim):
        
        u = Kernel_dim[0]
        v = Kernel_dim[1]
            
        DCT_table = np.zeros(shape=(u,v), dtype = 'float64')
            
        for m in range(u):
                for n in range(v):
                        if (m == 0):
                                DCT_table[m,n] = sqrt(1.0/u)
                        elif (m > 0):
                                DCT_table[m,n] = (sqrt(2.0/u))*(cos((pi*((2*n)+1)*m)/(2*u)))

        return DCT_table

def DWT3(Image, Area_dim):

        [row,col,depth] = Image.shape

        row_new = Area_dim[0]
        col_new = Area_dim[1]

        DWT_image_col = np.zeros(shape=(row,col,depth), dtype = 'float64')
        DWT_image_row = np.zeros(shape=(row,col,depth), dtype = 'float64')
        DWT_image = np.zeros(shape=(row,col,depth), dtype = 'float64')

        for z in range(depth):
                for m in range(0,row_new,2):
                        for n in range(col_new):

                                DWT_image_row[m/2,n,z] = ((float(Image[m,n,z]) + float(Image[m+1,n,z])))/2
                                DWT_image_row[(row_new+m)/2,n,z] = ((float(Image[m,n,z]) - float(Image[m+1,n,z])))/2

        for z in range(depth):
                for m in range(row_new):
                        for n in range(0,col_new,2):

                                DWT_image_col[m,n/2,z] = ((float(DWT_image_row[m,n,z]) + float(DWT_image_row[m,n+1,z])))/2
                                DWT_image_col[m,(col_new+n)/2,z] = ((float(DWT_image_row[m,n,z]) - float(DWT_image_row[m,n+1,z])))/2


        if ((row_new < row) & (col_new <col)):
                for z in range(depth):
                        for m in range(row):
                                for n in range(col):

                                        if ((m < row_new) & (n < col_new)):
                                                DWT_image[m,n,z] = DWT_image_col[m,n,z]

                                        elif ((m >= row_new) | (n >= col_new)):
                                                DWT_image[m,n,z] = Image[m,n,z]
        else:
                DWT_image = DWT_image_col

        return DWT_image

def IDCT3(Image,coeff_per_block,Kernel_dim):

        u = Kernel_dim[0]
        v = Kernel_dim[1]

        DCT_table = np.zeros(shape=(u,v), dtype = 'float64')
            
        for m in range(u):
                for n in range(v):
                        if (m == 0):
                                DCT_table[m,n] = sqrt(1.0/u)
                        elif (m > 0):
                                DCT_table[m,n] = (sqrt(2.0/u))*(cos((pi*((2*n)+1)*m)/(2*u)))

        [row, col, depth] = Image.shape

        Dec_table = ZigZag(u)

        Dec = np.zeros(shape = (u,v), dtype = 'uint8')

        IDCT_image = np.zeros(shape=(row,col,depth), dtype = 'uint8')

        IDCT_block = np.zeros(shape=(u,v), dtype = 'uint8')

        Image_block = np.zeros(shape=(u,v), dtype = 'float64')

        for m in xrange(u):
                for n in xrange(v):
                        if (Dec_table[m,n] < coeff_per_block):
                                Dec[m,n] = 1
                        elif (Dec_table[m,n] >= coeff_per_block):
                                Dec[m,n] = 0

        for k in range(depth):
                for m in range(0,row,u):
                        for n in range(0,col,v):

                                # Retrieve the image blocks of dimension u x v and convert them to DCT equivalents

                                for x in range(u):
                                        for y in range(v):
                                                Image_block[x,y] = Image[m+x,n+y,k]*Dec[x,y]

                                IDCT_block = Mat_multiply(Mat_transpose(DCT_table), Mat_multiply(Image_block, DCT_table))

                                for x in range(u):
                                        for y in range(v):
                                                temp = IDCT_block[x,y]
                                                if (temp > 255):
                                                        temp = 255
                                                elif (temp < 0):
                                                        temp = 0

                                                IDCT_image[m+x,n+y,k] = temp

        return IDCT_image

def IDWT3(DWT_image, Area_dim):

        [row,col,depth] = DWT_image.shape

        row_new = Area_dim[0]
        col_new = Area_dim[1]

        IDWT_image_col = np.zeros(shape=(row,col,depth), dtype = 'float64')
        IDWT_image_row = np.zeros(shape=(row,col,depth), dtype = 'float64')
        IDWT_image = np.zeros(shape=(row,col,depth), dtype = 'float64')

        for z in range(depth):
                for m in range(row_new):
                        for n in range(0,col_new,2):

                                IDWT_image_col[m,n,z] = DWT_image[m,n/2,z] + DWT_image[m,(col_new+n)/2,z]
                                IDWT_image_col[m,n+1,z] = DWT_image[m,n/2,z] - DWT_image[m,(col_new+n)/2,z]


        for z in range(depth):
                for m in range(0,row_new,2):
                        for n in range(col_new):

                                IDWT_image_row[m,n,z] = IDWT_image_col[m/2,n,z] + IDWT_image_col[(row_new+m)/2,n,z]
                                IDWT_image_row[m+1,n,z] = IDWT_image_col[m/2,n,z] - IDWT_image_col[(row_new+m)/2,n,z]

        if ((row_new < row) & (col_new <col)):
                for z in range(depth):
                        for m in range(row):
                                for n in range(col):

                                        if ((m < row_new) & (n < col_new)):
                                                IDWT_image[m,n,z] = IDWT_image_row[m,n,z]

                                        elif ((m >= row_new) | (n >= col_new)):
                                                IDWT_image[m,n,z] = DWT_image[m,n,z]
        else:
                IDWT_image = IDWT_image_row

        return IDWT_image

def Mat_multiply(Matrix_1, Matrix_2):

        [row_1, col_1] = Matrix_1.shape
        [row_2, col_2] = Matrix_2.shape

        if (row_2 != col_1):
                print('Matrices cannot be multiplied')
                pass
        
        Result_mat = np.zeros(shape = (row_1,col_2), dtype = 'float64')

        for m in range(row_1):
                for n in range(col_2):

                        for z in range(col_1):
                                Result_mat[m,n] += Matrix_1[m,z]*Matrix_2[z,n]

        return Result_mat

def Mat_transpose(Matrix):

        [row, col] = Matrix.shape

        Transposed_mat = np.zeros(shape = (col,row), dtype = 'float64')

        for m in range(row):
                for n in range(col):
                        Transposed_mat[n,m] = Matrix[m,n]

        return Transposed_mat

def read_rgb(file_name,row,col):
        
        image = np.fromfile(file_name, dtype ='uint8')

        # Reading all the channels
        Red_plane = np.zeros(shape=(row,col))
        Green_plane = np.zeros(shape=(row,col))
        Blue_plane = np.zeros(shape=(row,col))

        i = 0
        for m in range(row):
                for n in range(col):
                        Red_plane[m][n] = image[i]
                        Green_plane[m][n] = image[i+row*col]
                        Blue_plane[m][n] = image[i+2*row*col]
                        i =i+1

        # Bringing all together
        Intermediate_image = np.dstack((Red_plane,Green_plane,Blue_plane))
        Final_image = Image.fromarray(np.uint8(Intermediate_image))
##        Final_image.save('out.jpg')
##        os.system('out.jpg')
        return Final_image

def ZigZag(n):
        
    def path(i, j):
        if j < (n - 1):
            return max(0, i-1), j+1
        else:
            return i+1, j
        
    ZZ_table = np.zeros(shape = (n,n), dtype = 'uint32')
    x, y = 0, 0
    
    for v in xrange(n*n):
        ZZ_table[y,x] = v
        if (x + y) & 1:
            x, y = path(x, y)
        else:
            y, x = path(y, x)
            
    return ZZ_table
