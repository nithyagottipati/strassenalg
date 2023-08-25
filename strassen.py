import sys
import random
import time
import math
import fileinput

dim = int(sys.argv[2])

matrixArr = []
for line in fileinput.input(sys.argv[3]):
    matrixArr.extend([int(line)])


def createArr():
    a = [[0] * dim for i in range(dim)]
    b = [[0] * dim for i in range(dim)]
    for i in range(dim):
        for j in range(dim):
            a[i][j] = matrixArr.pop(0)
    for i in range(dim):
        for j in range(dim):
            b[i][j] = matrixArr.pop(0)
    return a, b

def printDiagonal(matrix):
    for i in range(len(matrix)):
        print(matrix[i][i])

def multiply(A, B):
    n = len(A)
    C = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][k] += A[i][j] * B[j][k]
    return C

def add(A, B):
    n = len(A)
    C = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
    return C

def subtract(A, B):
    n = len(A)
    C = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]
    return C

def helper(A, B):
    n = len(A)
    # if n == 63:
    if n == 1:
        return multiply(A, B)
    if n % 2 != 0:
        new = n + 1
        A_new = [[0] * new for i in range(new)]
        B_new = [[0] * new for i in range(new)]
        for i in range(n):
            for j in range(n):
                A_new[i][j] = A[i][j]
                B_new[i][j] = B[i][j]
    else:
        A_new = A
        B_new = B
    
    C_new = strassen(A_new, B_new)
    C = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = C_new[i][j]
    return C

def strassen(A, B):
    n = len(A)
    # if (n <= 65):
    if (n <= 1):
        return multiply(A, B)

    # initializing the new submatrices
    newSize = n // 2

    a11 = [[0] * newSize for i in range(newSize)]
    a12 = [[0] * newSize for i in range(newSize)]
    a21 = [[0] * newSize for i in range(newSize)]
    a22 = [[0] * newSize for i in range(newSize)]
    b11 = [[0] * newSize for i in range(newSize)]
    b12 = [[0] * newSize for i in range(newSize)]
    b21 = [[0] * newSize for i in range(newSize)]
    b22 = [[0] * newSize for i in range(newSize)]
    
    f1 = [[0] * newSize for i in range(newSize)]
    f2 = [[0] * newSize for i in range(newSize)]

    # dividing into 4 submatrices:
    for i in range(0, newSize):
        for j in range(0, newSize):
            a11[i][j] = A[i][j]  # top left
            a12[i][j] = A[i][j + newSize]  # top right
            a21[i][j] = A[i + newSize][j]  # bottom left
            a22[i][j] = A[i + newSize][j + newSize]  # bottom right

            b11[i][j] = B[i][j]  # top left
            b12[i][j] = B[i][j + newSize]  # top right
            b21[i][j] = B[i + newSize][j]  # bottom left
            b22[i][j] = B[i + newSize][j + newSize]  # bottom right

    # Calculating p1 to p7:
    f1 = add(a11, a22)
    f2 = add(b11, b22)
    p1 = helper(f1, f2) 

    f1 = add(a21, a22) 
    p2 = helper(f1, b11) 

    f2 = subtract(b12, b22)
    p3 = helper(a11, f2)  

    f2 = subtract(b21, b11) 
    p4 = helper(a22, f2) 

    f1 = add(a11, a12)  
    p5 = helper(f1, b22)  

    f1 = subtract(a21, a11)  
    f2 = add(b11, b12) 
    p6 = helper(f1, f2) 

    f1 = subtract(a12, a22) 
    f2 = add(b21, b22) 
    p7 = helper(f1, f2) 

    # calculating c21, c21, c11 and c22:
    c12 = add(p3, p5) 
    c21 = add(p2, p4) 

    f1 = add(p1, p4)
    f2 = add(f1, p7) 
    c11 = subtract(f2, p5) 

    f1 = add(p1, p3) 
    f2 = add(f1, p6) 
    c22 = subtract(f2, p2)

    # Inputting results into returnable matrix:
    C = [[0] * n for i in range(n)]
    for i in range(newSize):
        for j in range(newSize):
            C[i][j] = c11[i][j]
            C[i][j + newSize] = c12[i][j]
            C[i + newSize][j] = c21[i][j]
            C[i + newSize][j + newSize] = c22[i][j]
    return C

def test():
    for n in [128, 256, 513, 1025]:
        A = []
        B = []
        A = [[random.randint(0,2) for i in range(n)] for j in range(n)]
        B = [[random.randint(0,2) for i in range(n)] for j in range(n)]
        for i in [15, 30, 35, 50, 55, 60, 65, 70]:
            strassen_time = 0
            for j in range(2):
                strassen_start = time.time_ns()
                helper(A, B)
                strassen_end = time.time_ns()
                strassen_time += strassen_end - strassen_start
            strassen_time = strassen_time / 2

            print("avg strassen multiplication dimension ", n, " is at crossover point ", i, " : ", strassen_time)
test()

# def triangle():
#     for i in range(1, 6):
#         p = i * 0.01
#         M = [[0] * 1024 for x in range(1024)]
#         for j in range(1024):
#             for k in range(1024):
#                 random_gen = random.uniform(0,1)
#                 if random_gen < p:
#                         M[j][k] = 1
#         A = helper(M, M)
#         B = helper(A, M)
#         num = 0
#         for n in range(1024):
#             num += B[n][n]
#         num = num / 6
#         # exp = 1024 * 1023 * 1022 * p * p * p / 6
#         print("number of triangles for p value of ", p, " is ", num)
#         # print("expected number of triangles for ", p, " is ", exp)
# triangle()