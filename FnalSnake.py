import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class brick(object):
    rows = 20
    w = 600
    def __init__(self,start,directionx=1,directiony=0,color=(0,0,255)):
        self.pos = start
        self.directionx = 1
        self.directiony = 0
        self.color = color

        
    def move(self, directionx, directiony):
        self.directionx = directionx
        self.directiony = directiony
        self.pos = (self.pos[0] + self.directionx, self.pos[1] + self.directiony)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
        



class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = brick(pos)
        self.body.append(self.head)
        self.directionx = 0
        self.directiony = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.directionx = -1
                    self.directiony = 0
                    self.turns[self.head.pos[:]] = [self.directionx, self.directiony]

                elif keys[pygame.K_RIGHT]:
                    self.directionx = 1
                    self.directiony = 0
                    self.turns[self.head.pos[:]] = [self.directionx, self.directiony]

                elif keys[pygame.K_UP]:
                    self.directionx = 0
                    self.directiony = -1
                    self.turns[self.head.pos[:]] = [self.directionx, self.directiony]

                elif keys[pygame.K_DOWN]:
                    self.directionx = 0
                    self.directiony = 1
                    self.turns[self.head.pos[:]] = [self.directionx, self.directiony]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.directionx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.directionx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.directiony == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.directiony == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.directionx,c.directiony)
        

    def reset(self, pos):
        self.head = brick(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.directionx = 0
        self.directiony = 1


    def addbrick(self):
        tail = self.body[-1]
        dx, dy = tail.directionx, tail.directiony

        if dx == 1 and dy == 0:
            self.body.append(brick((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(brick((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(brick((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(brick((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].directionx = dx
        self.body[-1].directiony = dy
        

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def gridgraphic(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
        

def regraphedWindow(surface):
    global rows, width, s, candy
    surface.fill((0,0,0))
    s.draw(surface)
    candy.draw(surface)
    gridgraphic(width,rows, surface)
    pygame.display.update()


def randomcandy(rows, item):

    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
        
    return (x,y)

def endofgame(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, candy
    width = 600
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((0,0,255), (10,10))
    candy = brick(randomcandy(rows, s), color=(0,255,0))
    flag = True

    clock = pygame.time.Clock()
    
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == candy.pos:
            s.addbrick()
            candy = brick(randomcandy(rows, s), color=(0,255,0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body))
                endofgame('You Lost!', 'Play again...')
                s.reset((10,10))
                break

            
        regraphedWindow(win)

        
    pass



main()

