from .types import *
from enum import Enum

SPOTS = 100

def bezier_curve(start, end,height=-200):
    lis = []
    for i in range(SPOTS+1):
        t = i/SPOTS
        v = bezier_curve_spot(start,end,t,height)
        lis.append((v.x,v.y))
    return lis

def slice_bezier_curve(curve):
    lis = []
    for i in range(len(curve)//10):
        lis.append(curve[i*10:i*10+8])
    lis.append(curve[i*(len(curve)//10):])
    return lis

def bezier_curve_spot(start,end,t,height=-200):
    mid = (start()+end())/2+Vector2(0,height)
    x = (1-t)**2 * start().x + 2*(1-t)*t * mid.x + t**2 * end().x
    y = (1-t)**2 * start().y + 2*(1-t)*t * mid.y + t**2 * end().y
    return Vector2(x,y)

class triType(Enum):
    Start = 1
    End = -1

def triangle(start,end,typ):
    if start().x > end().x:
        modify = -1
    else:
        modify = 1
    p = bezier_curve_spot(start,end,(0.1 if typ == triType.Start else 0.9))
    q = start() if typ == triType.Start else end()
    if p.x == q.x:
        k = 1
    else:
        k = (p.y-q.y)/(p.x-q.x)
    if k == 0:
        k1 = -100000000000000000
    else:
        k1 = -1/k
    l1 = 60*typ.value*modify
    l2 = 10
    l3 = 40*typ.value*modify
    basx = l1/math.sqrt(k**2+1)
    basy = l1*k/math.sqrt(k**2+1)
    innerx = l3/math.sqrt(k**2+1)
    innery = l3*k/math.sqrt(k**2+1)
    dx = l2/math.sqrt(k1**2+1)
    dy = l2*k1/math.sqrt(k1**2+1)
    p2 = ((start().x if typ == triType.Start else end().x),
          (start().y if typ == triType.Start else end().y))
    p3 = (p2[0]+basx+dx,p2[1]+basy+dy)
    p4 = (p2[0]+basx-dx,p2[1]+basy-dy)
    p5 = (p2[0]+innerx,p2[1]+innery)
    return [p2,p3,p5,p4]