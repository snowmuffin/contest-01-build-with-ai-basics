"""Original small pixel assets for this project. Standard library only; no downloads.
Not a species catalogue or a reusable third-party desktop-pet asset.
"""
from pathlib import Path
import math, struct, zlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'src/Aquarium.Windows/Assets'
OUT.mkdir(parents=True,exist_ok=True)

def png(w,h,pixels):
    def chunk(t,b):return struct.pack('>I',len(b))+t+b+struct.pack('>I',zlib.crc32(t+b)&0xffffffff)
    raw=b''.join(b'\0'+bytes(v for px in pixels[y*w:(y+1)*w] for v in px) for y in range(h))
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b'')
class Canvas:
    def __init__(self,w,h):self.w=w;self.h=h;self.p=[(0,0,0,0)]*(w*h)
    def dot(self,x,y,color):
        if 0<=x<self.w and 0<=y<self.h:self.p[y*self.w+x]=tuple(color)+(255,) if len(color)==3 else tuple(color)
    def rect(self,x,y,w,h,c):
        for yy in range(y,y+h):
            for xx in range(x,x+w):self.dot(xx,yy,c)
    def poly(self,points,col):
        for y in range(max(0,int(min(p[1] for p in points))),min(self.h,int(max(p[1] for p in points))+1)):
            for x in range(max(0,int(min(p[0] for p in points))),min(self.w,int(max(p[0] for p in points))+1)):
                inside=False;j=len(points)-1
                for i in range(len(points)):
                    xi,yi=points[i];xj,yj=points[j]
                    if (yi>y+.5)!=(yj>y+.5) and x+.5<(xj-xi)*(y+.5-yi)/(yj-yi)+xi:inside=not inside
                    j=i
                if inside:self.dot(x,y,col)
    def paste(self,other,x,y):
        for yy in range(other.h):
            for xx in range(other.w):
                p=other.p[yy*other.w+xx]
                if p[3]:self.dot(x+xx,y+yy,p)
    def outline(self,color):
        old=self.p[:]
        for y in range(self.h):
            for x in range(self.w):
                if old[y*self.w+x][3]:continue
                if any(0<=x+dx<self.w and 0<=y+dy<self.h and old[(y+dy)*self.w+x+dx][3] for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]):self.dot(x,y,color)
    def save(self,path):path.write_bytes(png(self.w,self.h,self.p))

palettes=[((235,151,58),(251,203,104),(176,84,36)),((50,158,169),(138,224,212),(32,87,113)),((127,137,217),(207,203,251),(76,70,129))]
atlas=Canvas(160,72)
for row,(base,light,shade) in enumerate(palettes):
    for frame in range(4):
        c=Canvas(40,24);s=[0,1,0,-1][frame]
        c.poly([(3+s,5),(13,10),(15,13),(12,16),(3-s,21),(5,13)],shade)
        c.poly([(4+s,7),(11,11),(11,15),(4-s,19),(6,13)],base)
        c.poly([(14,8),(19,3),(27,5),(24,10)],shade)
        c.poly([(18,8),(20,4),(24,5),(23,8)],light)
        c.poly([(19,17),(25,21),(29,19),(27,16)],shade)
        c.poly([(11,10),(17,6),(25,6),(31,8),(36,10),(38,13),(35,17),(29,19),(20,19),(14,16)],base)
        c.poly([(14,10),(19,7),(26,7),(31,9),(32,10),(22,9)],light)
        c.poly([(14,14),(21,17),(30,17),(34,15),(33,18),(28,19),(20,19)],shade)
        c.poly([(21,11),(27,13+s),(25,16),(23,15)],light)
        c.rect(32,10,3,4,(27,45,60));c.dot(33,10,(248,247,220))
        c.dot(37,13,(27,45,60));c.dot(35,15,light)
        c.dot(18,11,light);c.dot(18,14,shade);c.dot(28,11,shade)
        c.outline((26,47,61));atlas.paste(c,frame*40,row*24)
atlas.save(OUT/'fish-atlas.png')

jar=Canvas(32,40)
jar.rect(6,7,20,25,(35,66,81));jar.rect(7,8,18,23,(76,128,138))
jar.rect(9,9,3,21,(181,225,209));jar.rect(23,10,2,19,(42,94,113))
jar.rect(10,12,13,14,(250,212,122));jar.rect(12,15,9,2,(82,92,84));jar.rect(12,20,7,2,(82,92,84))
jar.rect(8,30,16,5,(235,149,62));jar.rect(7,32,18,3,(239,173,75));jar.rect(12,35,8,3,(62,77,78))
jar.rect(9,5,14,3,(105,163,170));jar.outline((25,42,58));jar.save(OUT/'feeder.png')
# 32-bit DIB icon, so the shortcut/tray icon does not depend on a PNG ICO decoder.
icon=Canvas(32,32)
for y in range(30):
    for x in range(24):
        p=jar.p[int(y*40/30)*32+int(x*32/24)]
        if p[3]:icon.dot(x+4,y+1,p)
raw=b''.join(bytes((b,g,r,a)) for y in reversed(range(32)) for r,g,b,a in icon.p[y*32:(y+1)*32])
mask=b'\0'*(4*32)
dib=struct.pack('<IIIHHIIIIII',40,32,64,1,32,0,len(raw),0,0,0,0)+raw+mask
(OUT/'feeder.ico').write_bytes(struct.pack('<HHH',0,1,1)+struct.pack('<BBBBHHII',32,32,0,0,1,32,len(dib),22)+dib)
print('Generated original fish-atlas.png (3 palettes, 4 poses), feeder.png and feeder.ico.')
