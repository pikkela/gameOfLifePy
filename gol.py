from ctypes import sizeof
from msilib import add_stream
from multiprocessing.connection import wait
import curses
from curses import *
from curses.panel import *
from curses import wrapper

import random
import os
import time


from textwrap import dedent

n = 26#y ayis
m = 117#x ayis
#count = 0
empty = 0
ground = ["road ","grass", "mud  "]

def oneOrTwo(ones, twos):
    if ones == twos:
        return 0
    if ones > twos:
        return 1
    else:
        return 2

def genMap():
    val = [0] * n

    for y in range (n):
        val[y] = [0] * m

    for y in range (n):
        for x in range (m):
            num = random.choice([0, 1, 2])
            val[y][x] = num
    return val

def loopTrough(matx):
    world = [0] * m
    for y in range (n):
        for x in range (m):
            world[x] = ground[matx[y][x]] 
        print(world)

def printMatrix(matr,stdscr):
    for y in range (n):
        for x in range (m):
            if x == m-1:
                stdscr.addstr("")
            if matr[y][x] == 0:
                stdscr.addstr(y,x," ",curses.color_pair(1))
                #print("."," ", end='')
            else:
                stdscr.addstr(y,x,str(matr[y][x]),curses.color_pair(1))
                #print(matr[y][x]," ", end='')

############# Cell scan ###############
def rightCorner(people, cell, x, y):
    ones = 0
    twos = 0
    neigbours = [0,0]
    if cell == 1 or cell == 2:
        if people[y][x-1] == cell: 
            neigbours[0] += 1
        if people[y+1][x-1] == cell:   
            neigbours[0] += 1
        if people[y+1][x] == cell:   
            neigbours[0] += 1
        return neigbours
    if cell == 0: 
        if people[y][x-1] == 1 or people[y][x-1] == 2:
            if people[y][x-1] == 1:
                ones += 1
            else:
                twos +=1    
            neigbours[0] += 1
        if people[y+1][x] == 1 or people[y+1][x] == 2:
            if people[y+1][x] == 1:
                ones += 1
            else:
                twos +=1
            neigbours[0] += 1
        if people[y+1][x-1] == 1 or people[y+1][x-1] == 1:
            if people[y+1][x-1] == 1:
                ones += 1
            else:
                twos +=1
            neigbours[0] += 1
        neigbours[1] = oneOrTwo(ones, twos)
        return neigbours

def bottRightCorner(people, cell, x, y):
    ones = 0
    twos = 0
    neigbours = [0,0]
    if cell == 1 or cell == 2:
        if people[y-1][x] == cell:      
            neigbours[0] += 1
        if people[y-1][x-1] == cell:
            neigbours[0] += 1
        if people[y][x-1] == cell:
            neigbours[0] += 1
        return neigbours
    if cell == 0:
        if people[y-1][x] == 1 or people[y-1][x] == 2:
            if people[y-1][x] == 1:
                ones += 1
            else:
                twos +=1    
            neigbours[0] += 1
        if people[y-1][x-1] == 1 or people[y-1][x-1] == 2:
            if people[y-1][x-1] == 1:
                ones += 1
            else:
                twos +=1
            neigbours[0] += 1
        if people[y][x-1] == 1 or people[y][x-1] == 2:
            if people[y][x-1] == 1:
                ones += 1
            else:
                twos +=1
            neigbours[0] += 1
        neigbours[1] = oneOrTwo(ones, twos)
        return neigbours

def lastColMid(people, cell, x, y):
    ones = 0
    twos = 0
    neigbours = [0,0]
    if cell == 1 or cell == 2:
        if people[y-1][x-1] == cell:      
            neigbours[0] += 1
        if people[y-1][x] == cell:      
            neigbours[0] += 1
        if people[y][x-1] == cell:      
            neigbours[0] += 1
        if people[y+1][x] == cell:
            neigbours[0] += 1
        if people[y+1][x-1] == cell:
            neigbours[0] += 1
        return neigbours
    if cell == 0:
        if people[y-1][x-1] == 1 or people[y-1][x-1] == 2:
            if people[y-1][x-1] == 1:
                ones += 1
            else:
                twos +=1    
            neigbours[0] += 1
        if people[y-1][x] == 1 or people[y-1][x] == 2:
            if people[y-1][x] == 1:
                ones += 1
            else:
                twos +=1     
            neigbours[0] += 1
        if people[y][x-1] == 1 or people[y][x-1] == 2:
            if people[y][x-1] == 1:
                ones += 1
            else:
                twos +=1      
            neigbours[0] += 1
        if people[y+1][x] == 1 or people[y+1][x] == 2:
            if people[y+1][x] == 1:
                ones += 1
            else:
                twos +=1
            neigbours[0] += 1
        if people[y+1][x-1] == 1 or people[y+1][x-1] == 2:
            if people[y+1][x-1] == 1:
                ones += 1
            else:
                twos +=1
            neigbours[0] += 1
        neigbours[1] = oneOrTwo(ones, twos)
        return neigbours

def leftUpCorner(people, cell, x, y):
    ones = 0
    twos = 0
    neigbours = [0,0]
    if cell == 1 or cell == 2:
        if people[y][x+1] == cell:      
            neigbours[0] += 1
        if people[y+1][x] == cell:
            neigbours[0] += 1
        if people[y+1][x+1] == cell:
            neigbours[0] += 1
        return neigbours
    if cell == 0:
        if people[y][x+1] == 1 or people[y][x+1] == 2:
            if people[y][x+1] == 1:
                ones += 1
            else:
                twos +=1    
            neigbours[0] += 1
        if people[y+1][x] == 1 or people[y+1][x] == 2:
            if people[y+1][x] == 1:
                ones += 1
            else:
                twos +=1
            neigbours[0] += 1
        if people[y+1][x+1] == 1 or people[y+1][x+1] == 2:
            if people[y+1][x+1] == 1:
                ones += 1
            else:
                twos +=1
            neigbours[0] += 1
        neigbours[1] = oneOrTwo(ones, twos)
        return neigbours

def leftMid(people, cell, x, y):
    ones = 0
    twos = 0
    neigbours = [0,0]
    if cell == 1 or cell == 2:
        if people[y-1][x] == cell:      
            neigbours[0] += 1
        if people[y-1][x+1] == cell:      
            neigbours[0] += 1
        if people[y][x+1] == cell:      
            neigbours[0] += 1
        if people[y+1][x] == cell:
            neigbours[0] += 1
        if people[y+1][x+1] == cell:
            neigbours[0] += 1
        return neigbours
    if cell == 0:
        if people[y-1][x] == 1 or people[y-1][x] == 2:
            if people[y-1][x] == 1:
                ones += 1
            else:
                twos +=1     
            neigbours[0] += 1
        if people[y-1][x+1] == 1 or people[y-1][x+1] == 2:
            if people[y-1][x+1] == 1:
                ones += 1
            else:
                twos +=1     
            neigbours[0] += 1
        if people[y][x+1] == 1 or people[y][x+1] == 2:
            if people[y][x+1] == 1:
                ones += 1
            else:
                twos +=1      
            neigbours[0] += 1
        if people[y+1][x] == 1 or people[y+1][x] == 2:
            if people[y+1][x] == 1:
                ones += 1
            else:
                twos +=1
            neigbours[0] += 1
        if people[y+1][x+1] == 1 or people[y+1][x+1] == 2:
            if people[y+1][x+1] == 1:
                ones += 1
            else:
                twos +=1
            neigbours[0] += 1
        neigbours[1] = oneOrTwo(ones, twos)
        return neigbours

def topMid(people, cell, x, y):
    ones = 0
    twos = 0
    neigbours = [0,0]
    if cell == 1 or cell == 2:
        if people[y][x-1] == cell:      
            neigbours[0] += 1
        if people[y][x+1] == cell:      
            neigbours[0] += 1
        if people[y+1][x-1] == cell:      
            neigbours[0] += 1
        if people[y+1][x] == cell:
            neigbours[0] += 1
        if people[y+1][x+1] == cell:
            neigbours[0] += 1
        return neigbours
    if cell == 0:
        if people[y][x-1] == 1 or people[y][x-1] == 2:
            if people[y][x-1] == 1:
                ones += 1
            else:
                twos +=1   
            neigbours[0] += 1
        if people[y][x+1] == 1 or people[y][x+1] == 2:
            if people[y][x+1] == 1:
                ones += 1
            else:
                twos +=1     
            neigbours[0] += 1
        if people[y+1][x-1] == 1 or people[y+1][x-1] == 2:
            if people[y+1][x-1] == 1:
                ones += 1
            else:
                twos +=1      
            neigbours[0] += 1
        if people[y+1][x] == 1 or people[y+1][x] == 2:
            if people[y+1][x] == 1:
                ones += 1
            else:
                twos +=1
            neigbours[0] += 1
        if people[y+1][x+1] == 1 or people[y+1][x+1] == 2:
            if people[y+1][x+1] == 1:
                ones += 1
            else:
                twos +=1
            neigbours[0] += 1
        neigbours[1] = oneOrTwo(ones, twos)
        return neigbours

def bottMid(people, cell, x, y):
    ones = 0
    twos = 0
    neigbours = [0,0]
    if cell == 1 or cell == 2:
        if people[y][x-1] == cell:      
            neigbours[0] += 1
        if people[y][x+1] == cell:      
            neigbours[0] += 1
        if people[y-1][x-1] == cell:      
            neigbours[0] += 1
        if people[y-1][x] == cell:
            neigbours[0] += 1
        if people[y-1][x+1] == cell:
            neigbours[0] += 1
        return neigbours
    neigbours = [0,0]
    if cell == 0:
        if people[y][x-1] == 1 or people[y][x-1] == 2:
            if people[y][x-1] == 1:
                ones += 1
            else:
                twos +=1     
            neigbours[0] += 1
        if people[y][x+1] == 1 or people[y][x+1] == 2:
            if people[y][x+1] == 1:
                ones += 1
            else:
                twos +=1      
            neigbours[0] += 1
        if people[y-1][x-1] == 1 or people[y-1][x-1] == 2:
            if people[y-1][x-1] == 1:
                ones += 1
            else:
                twos +=1     
            neigbours[0] += 1
        if people[y-1][x] == 1 or people[y-1][x] == 2:
            if people[y-1][x] == 1:
                ones += 1
            else:
                twos +=1
            neigbours[0] += 1
        if people[y-1][x+1] == 1 or people[y-1][x+1] == 2:
            if people[y-1][x+1] == 1:
                ones += 1
            else:
                twos +=1
            neigbours[0] += 1
        neigbours[1] = oneOrTwo(ones, twos)
        return neigbours

def middle(people, cell, x, y):
    ones = 0
    twos = 0
    neigbours = [0,0]
    if cell == 1 or cell == 2:
        if people[y-1][x-1] == cell:      
            neigbours[0] += 1
        if people[y-1][x] == cell:      
            neigbours[0] += 1
        if people[y-1][x+1] == cell:      
            neigbours[0] += 1
        if people[y][x-1] == cell:
            neigbours[0] += 1
        if people[y][x+1] == cell:
            neigbours[0] += 1
        if people[y+1][x-1] == cell:      
            neigbours[0] += 1
        if people[y+1][x] == cell:      
            neigbours[0] += 1
        if people[y+1][x+1] == cell:      
            neigbours[0] += 1
        return neigbours
    if cell == 0:
        if people[y-1][x-1] == 1 or people[y-1][x-1] == 2:
            if people[y-1][x-1] == 1:
                ones += 1
            else:
                twos +=1    
            neigbours[0] += 1
        if people[y-1][x] == 1 or people[y-1][x] == 2:
            if people[y-1][x] == 1:
                ones += 1
            else:
                twos +=1      
            neigbours[0] += 1
        if people[y-1][x+1] == 1 or people[y-1][x+1] == 2:
            if people[y-1][x+1] == 1:
                ones += 1
            else:
                twos +=1     
            neigbours[0] += 1
        if people[y][x-1] == 1 or people[y][x-1] == 2:
            if people[y][x-1] == 1:
                ones += 1
            else:
                twos +=1
            neigbours[0] += 1
        if people[y][x+1] == 1 or people[y][x+1] == 2:
            if people[y][x+1] == 1:
                ones += 1
            else:
                twos +=1
            neigbours[0] += 1
        if people[y+1][x-1] == 1 or people[y+1][x-1] == 2:
            if people[y+1][x-1] == 1:
                ones += 1
            else:
                twos +=1      
            neigbours[0] += 1
        if people[y+1][x] == 1 or people[y+1][x] == 2:
            if people[y+1][x] == 1:
                ones += 1
            else:
                twos +=1     
            neigbours[0] += 1
        if people[y+1][x+1] == 1 or people[y+1][x+1] == 2:
            if people[y+1][x+1] == 1:
                ones += 1
            else:
                twos +=1      
            neigbours[0] += 1
        neigbours[1] = oneOrTwo(ones, twos)
        return neigbours

def leftBottomCorner(people, cell, x, y):
    neigbours = [0,0]
    ones = 0
    twos = 0
    if cell == 1 or cell == 2:
        if people[y-1][x] == cell:      
            neigbours[0] += 1
        if people[y-1][x+1] == cell:
            neigbours[0] += 1
        if people[y][x+1] == cell:
            neigbours[0] += 1
        return neigbours
    if cell == 0:
        if people[y-1][x] == 1 or people[y-1][x] == 2:
            if people[y-1][x] == 1:
                ones += 1
            else:
                twos +=1      
            neigbours[0] += 1
        if people[y-1][x+1] == 1 or people[y-1][x+1] == 2:
            if people[y-1][x+1] == 1:
                ones += 1
            else:
                twos +=1 
            neigbours[0] += 1
        if people[y][x+1] == 1 or people[y][x+1] == 2:
            if people[y][x+1] == 1:
                ones += 1
            else:
                twos +=1 
            neigbours[0] += 1

        neigbours[1] = oneOrTwo(ones, twos)
        return neigbours

########################################
def genNewPeople(count, cell, newPeople, x, y):
    #Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    #Any live cell with more than three live neighbours dies, as if by overpopulation.
    if cell != 0:
        if count[0] < 2 or count[0] > 3:
            newPeople[y][x] = empty
    #Any live cell with two or three live neighbours lives on to the next generation.
        if count[0] == 2 or count[0] == 3:
            newPeople[y][x] = cell
    #Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    else:
        if count[0] == 3:
            newPeople[y][x] = 1
        else:
            newPeople[y][x] = 0
 
def checkNeighbours(people):
    newPeople = genMap()
    for y in range (n):
        for x in range (m):
            cell = people[y][x]
            if cell == 1 or cell == 2 or cell == 0:
                if x == 0:
                    if y == 0:
                        count = leftUpCorner(people, cell, x, y)
                        genNewPeople(count, cell, newPeople, x, y)
                        #newPeople[y][x] = count
                        ##print(count, "= leftUp")
                    if y > 0 and y < n-1:
                         count = leftMid(people, cell, x, y)
                         genNewPeople(count, cell, newPeople, x, y)
                         #newPeople[y][x] = count
                         ##print(count, "= leftMid")
                    if y == n-1:
                        count = leftBottomCorner(people, cell, x, y)
                        genNewPeople(count, cell, newPeople, x, y)
                        #newPeople[y][x] = count
                        ##print(count, "= LeftBottom")
                if x == m-1:                            #[2, 1, 1, 1, 1, 2, 0, X] check X´s neighbours     
                    if y == 0:                          #[1, 0, 1, 2, 2, 0, 1, 0]#[1, 2, 2, 2, 0, 2, 1, 0]
                       count = rightCorner(people, cell, x, y)
                       genNewPeople(count, cell, newPeople, x, y)
                       #newPeople[y][x] = count
                       ##print(count, "= rightUp")
                    if y > 0 and y < n-1:
                        count = lastColMid(people, cell, x, y)
                        genNewPeople(count, cell, newPeople, x, y)
                        #newPeople[y][x] = count
                        ##print(count, "= rightMid")
                    if y == n-1:
                        count = bottRightCorner(people, cell, x, y)
                        genNewPeople(count, cell, newPeople, x, y)
                        #newPeople[y][x] = count
                        ##print(count, "= rightBottom")

                if y == 0 or y == n-1:
                    if x > 0 and x < m-1:
                        if y == 0:
                            count = topMid(people, cell, x, y)
                            genNewPeople(count, cell, newPeople, x, y)
                            #newPeople[y][x] = count
                            ##print(count, "= TopMid")
                        if y == n-1:
                            count = bottMid(people, cell, x, y)
                            genNewPeople(count, cell, newPeople, x, y)
                            #newPeople[y][x] = count
                            ##print(count, "= BottMid")
                
                elif y > 0 and y < n-1 and x > 0 and x < m-1:
                    count = middle(people, cell, x, y)
                    genNewPeople(count, cell, newPeople, x, y)
                    #newPeople[y][x] = count
                    ##print(count, "= Middle", "Y = ",y, "x =", x  )
                        #add checks here

    return newPeople



def main(stdscr):
    #curses.init_color(1, 0, 255, 0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.color_pair(1)
    map = genMap()
    #loopTrough(map)
    #print()
    people = genMap()
    #printMatrix(people)
    cpypeople = checkNeighbours(people)
    while  1:
        stdscr.clear()
        cpypeople = checkNeighbours(cpypeople)
        printMatrix(cpypeople,stdscr)
        stdscr.refresh()
        time.sleep(0.08)
        #stdscr.getch()
        #loopTrough(map)



wrapper(main)



"""{
    ground:[ 
        rocky = 1,
        muddy = 0,
        water = 0,
        field = 0,
        forest = 0,
        desert = 0 

    ],
    human:[
        stamina = 0,
        health = 0,
        speed = 0
    ],
    humanoid:[
        stamina = 0,
        health = 0,
        speed = 0
    ]
  
}"""