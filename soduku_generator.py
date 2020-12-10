
import random
import numpy as np

'''
Usage: 
In any other file: 
    import  soduku_generator
    
    cage_constraints = soduku_generator.createMatrix(Soduku_Size,Max_Cage_Length)
    

'''

soduku4 = [[1, 2, 3, 4],
           [3, 4, 1, 2],
           [2, 3, 4, 1],
           [4, 1, 2, 3]]

soduku9 = [[2, 1, 5, 6, 4, 7, 3, 9, 8],
           [3, 6, 8, 9, 5, 2, 1, 7, 4],
           [7, 9, 4, 3, 8, 1, 6, 5, 2],
           [5, 8, 6, 2, 7, 4, 9, 3, 1],
           [1, 4, 2, 5, 9, 3, 8, 6, 7],
           [9 ,7 ,3, 8, 1, 6, 4, 2, 5],
           [8, 2, 1, 7, 3, 9, 5, 4, 6],
           [6, 5, 9, 4, 2, 8, 7, 1, 3],
           [4, 3, 7, 1, 6, 5, 2, 8, 9]]

soduku16 = [[ 1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12, 13, 14, 15, 16],
            [ 9, 10, 11, 12,  1,  2,  3,  4,  13, 14, 15, 16,  5,  6,  7,  8],
            [ 5,  6,  7,  8, 13, 14, 15, 16,  1,  2,  3,  4,  9, 10, 11, 12],
            [13, 14, 15, 16,  9, 10, 11, 12,  5,  6,  7,  8,  1,  2,  3,  4],
            [ 3,  1,  4,  2,  7,  5,  8,  6, 11,  9,  14, 10, 15, 12, 16, 13],
            [11,  9, 14, 10,  3,  1,  4,  2, 15, 12,  16, 13, 7,  5,  8,  6],
            [ 7,  5,  8,  6, 15, 12, 16, 13,  3,  1,  4,  2,  11, 9,  14, 10],
            [15, 12, 16, 13, 11,  9, 14, 10,  7,  5,  8,  6,  3,  1,  4,  2],
            [ 2, 4,  1,  3,  6,  8,  5,  7,  10, 15,  9,  11, 12, 16, 13, 14],
            [10, 15, 9, 11,  2,  4,  1,  3,  12, 16, 13,  14, 6,  8,  5,  7],
            [6,  8,  5,  7, 12, 16, 13, 14,  2,  4,  1,  3,  10,  15, 9, 11],
            [12, 16, 13, 14, 10, 15, 9, 11,  6,  8,  5,  7,  2,   4,  1,  3],
            [ 4, 3,  2,  1,  8,  7,  6,  5,  14, 11, 10, 9,  16,  13,  12, 15],
            [14, 11, 10,  9,  4,  3,  2,  1, 16, 13, 12, 15, 8,  7,  6,  5],
            [8,  7,  6,  5,  16,  13, 12, 15, 4, 3,  2,  1,  14, 11, 10, 9],
            [16, 15, 14, 13, 12,  11, 10,  9, 8, 7,  6,  5,   4,  3,  2, 1]]
sodukus = {4:soduku4,9:soduku9,16:soduku16}

def createMatrix(N,cageLen):
    soduku = sodukus[N]
    sodukuVisited = np.zeros((N,N))

    def getEmptyCell():
        for i in range(N):
            for j in range(N):
                if sodukuVisited[i][j] == 0:
                    return (i,j)
        return None

    def getRandomNeighbor(i, j):
        tmp = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
        neighbors = []
        for ele in tmp:
            if -1<ele[0]<N and -1<ele[1]<N:
                neighbors.append(ele)

        random.shuffle(neighbors)
        for ele in neighbors:
            if sodukuVisited[ele[0], ele[1]] == 0:
                return ele
        return None

    def createRandomShape():
        length = random.randint(2, cageLen)
        start = getEmptyCell()
        if not start:
            return None
        sodukuVisited[start[0],start[1]] = 1
        res= [start]
        resVal = [soduku[start[0]][start[1]]]
        while(length>len(res)):
            random.shuffle(res)
            updated = False
            for ele in res:
                neighbor = getRandomNeighbor(ele[0],ele[1])
                if neighbor and soduku[neighbor[0]][neighbor[1]] not in resVal:
                    res.append(neighbor)
                    sodukuVisited[neighbor[0], neighbor[1]] = 1
                    resVal += [soduku[neighbor[0]][neighbor[1]]]
                    updated = True
                    break
            if not updated:
                return res
        return res

    final_res = []

    def getsum(shape):
        res = 0
        for ele in shape:
            res += soduku[ele[0]][ele[1]]
        return res

    current = createRandomShape()
    while(current):
        if len(current) == 1:
            current = createRandomShape()
            continue
        newcurrent = [(ele[0]+1, ele[1]+1) for ele in current]
        final_res.append((getsum(current),newcurrent))
        current = createRandomShape()
    print("Constraints Generated Sucessfully!")
    print("The constraints are:", final_res)
    return final_res



# print(createMatrix(9))




