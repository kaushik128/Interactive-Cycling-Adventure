from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import time

from inputs import *

from drawHere import drawHere


def draw_point(x, y):
      glPointSize(5)
      glEnable(GL_POINT_SMOOTH)
      glBegin(GL_POINTS)
      glVertex2f(x,y)
      glEnd()

def iterate():
      glViewport(0, 0, 1265, 645) # keep it same as window size
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      glOrtho(0.0, 1000, 0.0, 500, 0.0, 1.0)
      glMatrixMode(GL_MODELVIEW)
      glLoadIdentity()

def getZone(x1, y1, x2, y2):
      dx=x2-x1
      dy=y2-y1
      if abs(dx)>=abs(dy) and dx>=0 and dy>=0: return 0
      if abs(dy)>=abs(dx) and dx>=0 and dy>=0: return 1
      if abs(dy)>=abs(dx) and dx<=0 and dy>=0: return 2
      if abs(dx)>=abs(dy) and dx<=0 and dy>=0: return 3
      if abs(dx)>=abs(dy) and dx<=0 and dy<=0: return 4
      if abs(dy)>=abs(dx) and dx<=0 and dy<=0: return 5
      if abs(dy)>=abs(dx) and dx>=0 and dy<=0: return 6
      if abs(dx)>=abs(dy) and dx>=0 and dy<=0: return 7

def changingZone0toX(zone, x, y):
      if zone==0:
            x_=x
            y_=y
      if zone==1:
            x_=y
            y_=x
      if zone==2:
            x_=-y
            y_=x
      if zone==3:
            x_=-x
            y_=y
      if zone==4:
            x_=-x
            y_=-y
      if zone==5:
            x_=-y
            y_=-x
      if zone==6:
            x_=y
            y_=-x
      if zone==7:
            x_=x
            y_=-y
      return (x_, y_)

def changingZoneXto0(zone, x, y):
      if zone==0:
            x_=x
            y_=y
      if zone==1:
            x_=y
            y_=x
      if zone==2:
            x_=y
            y_=-x
      if zone==3:
            x_=-x
            y_=y
      if zone==4:
            x_=-x
            y_=-y
      if zone==5:
            x_=-y
            y_=-x
      if zone==6:
            x_=-y
            y_=x
      if zone==7:
            x_=x
            y_=-y
      return (x_, y_)

def getIntermediatePoints(x1, y1, x2, y2):
      dx=x2-x1
      dy=y2-y1
      d=2*dy-dx
      incE=2*dy
      incNE=2*(dy-dx)
      y=y1
      x=x1
      intPoints=[]
      while x<=x2:
            intPoints.append( (x, y) )
            
            if d>0:
                  d=d+incNE
                  y=y+1
            else:
                  d=d+incE
            
            x=x+1

      return intPoints      

def newDrawLine(x1, y1, x2, y2):
      zone=getZone(x1, y1, x2, y2)

      p1=changingZoneXto0(zone, x1, y1)
      x1_=p1[0]
      y1_=p1[1]
      p2=changingZoneXto0(zone, x2, y2)
      x2_=p2[0]
      y2_=p2[1]

      intPoints=getIntermediatePoints(x1_, y1_, x2_, y2_)

      for i in range(0, len(intPoints)):
            x=intPoints[i][0]
            y=intPoints[i][1]

            p=changingZone0toX(zone, x, y)
            x=p[0]
            y=p[1]

            draw_point(x, y)

def drawCircle(xc, yc, r):
      d = 1-r
      x = 0
      y = r

      while x<y:
            if d<0: #E
                  d = d+2*x+3
                  x = x+1
            
            else: #SE
                  d = d+2*x-2*y+5
                  x = x+1
                  y = y-1

            zoneChange(x, y, xc, yc)

def zoneChange(x, y, xc, yc):
      new_x = x + xc
      new_y = y + yc
      draw_point(new_x, new_y)

      new_x = y + xc
      new_y = x + yc
      draw_point(new_x, new_y)

      new_x = -1 * y + xc
      new_y = x + yc
      draw_point(new_x, new_y)

      new_x = -1 *x + xc
      new_y = y + yc
      draw_point(new_x, new_y)

      new_x = -1 * x + xc
      new_y = -1 * y + yc
      draw_point(new_x, new_y)

      new_x = -1 * y + xc
      new_y = -1 * x + yc
      draw_point(new_x, new_y)

      new_x = y + xc
      new_y = -1 * x + yc
      draw_point(new_x, new_y)

      new_x = x+ xc
      new_y = -1 * y + yc
      draw_point(new_x, new_y)

def showScreen():
      glClearColor(1.0, 1.0, 1.0, 0.0)
      if weather=='night': glClearColor(0.0, 0.0, 0.0, 0.0)
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      glLoadIdentity()
      iterate()
      drawHere(glColor3f, newDrawLine, drawCircle, time, glutSwapBuffers, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT)
      glutSwapBuffers()
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1265, 645) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"CSE423 Project") #window name
glutDisplayFunc(showScreen)
glutMainLoop()