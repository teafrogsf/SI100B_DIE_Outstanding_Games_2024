from .types import *
import math

def getLinearResult(st,ed,orix):
    l = (ed-st).length()
    scale = Vector2(l/orix,1)
    rotation = math.degrees(math.atan2(ed.y-st.y,ed.x-st.x))
    mid = (st+ed)/2
    #print(st(),ed())
    #print(scale,rotation,mid)
    return (scale,rotation,mid)