"""Generate the project's original deterministic pixel assets.
Standard library only; no downloads and no third-party character art.

Fish atlas layout:
- rows: Goldfish, Tetra, Angelfish, Guppy
- direction groups: Left, Right, TowardViewer, AwayFromViewer
- two 40x24 animation cells per direction
"""
from pathlib import Path
import struct, zlib

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'src/Aquarium.Windows/Assets'
OUT.mkdir(parents=True,exist_ok=True)

def png(w,h,pixels):
    def chunk(t,b):
        return struct.pack('>I',len(b))+t+b+struct.pack('>I',zlib.crc32(t+b)&0xffffffff)
    raw=b''.join(b'\0'+bytes(v for px in pixels[y*w:(y+1)*w] for v in px) for y in range(h))
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b'')

class Canvas:
    def __init__(self,w,h):
        self.w=w; self.h=h; self.p=[(0,0,0,0)]*(w*h)
    def dot(self,x,y,color):
        if 0<=x<self.w and 0<=y<self.h:
            self.p[y*self.w+x]=tuple(color)+(255,) if len(color)==3 else tuple(color)
    def rect(self,x,y,w,h,c):
        for yy in range(y,y+h):
            for xx in range(x,x+w):
                self.dot(xx,yy,c)
    def poly(self,points,col):
        min_y=max(0,int(min(p[1] for p in points)))
        max_y=min(self.h,int(max(p[1] for p in points))+1)
        min_x=max(0,int(min(p[0] for p in points)))
        max_x=min(self.w,int(max(p[0] for p in points))+1)
        for y in range(min_y,max_y):
            for x in range(min_x,max_x):
                inside=False; j=len(points)-1
                for i in range(len(points)):
                    xi,yi=points[i]; xj,yj=points[j]
                    if (yi>y+.5)!=(yj>y+.5) and x+.5<(xj-xi)*(y+.5-yi)/(yj-yi)+xi:
                        inside=not inside
                    j=i
                if inside:self.dot(x,y,col)
    def paste(self,other,x,y):
        for yy in range(other.h):
            for xx in range(other.w):
                p=other.p[yy*other.w+xx]
                if p[3]:self.dot(x+xx,y+yy,p)
    def mirror_h(self):
        c=Canvas(self.w,self.h)
        for y in range(self.h):
            for x in range(self.w):
                p=self.p[y*self.w+x]
                if p[3]:c.dot(self.w-1-x,y,p)
        return c
    def outline(self,color):
        old=self.p[:]
        for y in range(self.h):
            for x in range(self.w):
                if old[y*self.w+x][3]:continue
                if any(0<=x+dx<self.w and 0<=y+dy<self.h and old[(y+dy)*self.w+x+dx][3]
                       for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]):
                    self.dot(x,y,color)
    def save(self,path):
        path.write_bytes(png(self.w,self.h,self.p))

OUTLINE=(24,42,56)
EYE=(23,36,46)
EYE_GLINT=(248,245,218)
SPECIES=[
    # base, light, shade, accent
    ((232,141,54),(255,202,96),(168,72,34),(247,230,142)),     # goldfish
    ((42,157,176),(125,224,216),(28,91,116),(242,92,91)),      # tetra
    ((129,126,218),(213,204,251),(76,68,137),(239,193,88)),    # angelfish
    ((87,181,109),(180,229,135),(44,105,79),(235,111,159)),    # guppy
]

def side_cell(species,frame):
    base,light,shade,accent=SPECIES[species]
    c=Canvas(40,24)
    wag=1 if frame else -1
    if species==0: # rounded goldfish, broad split tail
        c.poly([(4,5+wag),(13,9),(13,15),(4,20-wag),(7,13)],shade)
        c.poly([(5,6+wag),(12,10),(12,13),(5,18-wag),(8,12)],accent)
        c.poly([(11,7),(18,4),(28,5),(35,9),(37,12),(35,16),(28,19),(18,20),(11,16),(9,12)],base)
        c.poly([(15,8),(21,5),(29,7),(33,9),(22,8)],light)
        c.poly([(18,18),(25,21),(30,18),(27,16)],shade)
    elif species==1: # slim tetra
        c.poly([(4,8+wag),(13,11),(13,14),(4,17-wag),(8,12)],shade)
        c.poly([(11,8),(19,6),(31,7),(37,11),(37,13),(31,17),(19,18),(11,15),(8,12)],base)
        c.poly([(17,8),(29,8),(34,11),(20,10)],light)
        c.rect(17,11,14,2,accent)
        c.poly([(20,17),(24,20),(28,17)],shade)
    elif species==2: # tall angelfish diamond
        c.poly([(4,9+wag),(13,11),(13,14),(4,16-wag),(8,12)],shade)
        c.poly([(13,12),(20,4),(29,7),(35,12),(29,17),(20,20)],base)
        c.poly([(20,4),(23,1),(25,7)],shade)
        c.poly([(20,20),(22,23),(25,17)],shade)
        c.poly([(18,8),(27,7),(31,10),(23,9)],light)
        c.rect(18,11,2,7,accent)
        c.rect(24,8,2,10,accent)
    else: # guppy, small body + huge fan tail
        c.poly([(2,4+wag),(15,9),(15,15),(2,20-wag),(7,12)],accent)
        c.poly([(5,6+wag),(14,10),(14,14),(5,18-wag),(9,12)],shade)
        c.poly([(13,9),(20,7),(29,8),(36,11),(37,13),(30,16),(20,17),(13,15),(11,12)],base)
        c.poly([(18,9),(27,9),(32,11),(21,10)],light)
        c.poly([(19,16),(23,20),(27,16)],shade)
    c.rect(31 if species!=2 else 28,10,3,3,EYE)
    c.dot(32 if species!=2 else 29,10,EYE_GLINT)
    c.outline(OUTLINE)
    return c

def front_cell(species,frame,away=False):
    base,light,shade,accent=SPECIES[species]
    c=Canvas(40,24)
    fin=1 if frame else 0
    if species==0:
        c.poly([(20,3),(27,6),(31,11),(30,17),(24,21),(16,21),(10,17),(9,11),(13,6)],base)
        c.poly([(9-fin,8),(3,5),(7,13),(3,19),(11+fin,16)],shade)
        c.poly([(31+fin,8),(37,5),(33,13),(37,19),(29-fin,16)],shade)
        c.poly([(16,5),(20,3),(24,5),(22,10),(18,10)],light)
    elif species==1:
        c.poly([(20,5),(26,7),(29,12),(26,17),(20,19),(14,17),(11,12),(14,7)],base)
        c.poly([(12-fin,10),(5,8),(9,13),(5,17),(13,15)],shade)
        c.poly([(28+fin,10),(35,8),(31,13),(35,17),(27,15)],shade)
        c.rect(17,10,6,3,accent)
    elif species==2:
        c.poly([(20,2),(27,8),(29,13),(25,19),(20,22),(15,19),(11,13),(13,8)],base)
        c.poly([(13-fin,7),(7,3),(10,12),(6,20),(15,17)],shade)
        c.poly([(27+fin,7),(33,3),(30,12),(34,20),(25,17)],shade)
        c.poly([(18,3),(20,0),(22,3)],accent)
        c.poly([(18,20),(20,24),(22,20)],accent)
    else:
        c.poly([(20,6),(26,8),(29,12),(26,17),(20,19),(14,17),(11,12),(14,8)],base)
        c.poly([(13-fin,8),(4,4),(8,12),(4,20),(14,16)],accent)
        c.poly([(27+fin,8),(36,4),(32,12),(36,20),(26,16)],accent)
        c.poly([(17,8),(23,8),(25,11),(15,11)],light)
    if away:
        c.rect(18,6,4,2,shade)
        c.rect(16,11,8,2,accent)
        c.dot(20,16,light)
    else:
        c.rect(14,10,3,3,EYE); c.rect(23,10,3,3,EYE)
        c.dot(15,10,EYE_GLINT); c.dot(24,10,EYE_GLINT)
        c.rect(18,15,4,2,shade)
    c.outline(OUTLINE)
    return c

atlas=Canvas(320,96)
for species in range(4):
    for frame in range(2):
        right=side_cell(species,frame)
        left=right.mirror_h()
        toward=front_cell(species,frame,False)
        away=front_cell(species,frame,True)
        for facing,cell in enumerate([left,right,toward,away]):
            atlas.paste(cell,(facing*2+frame)*40,species*24)
atlas.save(OUT/'fish-atlas.png')

# Solid, opaque food canister: no glass/window-through treatment inside the body.
jar=Canvas(40,48)
jar.rect(8,5,24,4,(88,136,145))
jar.rect(6,9,28,30,(41,72,82))
jar.rect(8,10,24,28,(76,128,137))
jar.rect(10,12,4,23,(174,218,204))
jar.rect(30,12,2,22,(31,83,99))
jar.rect(11,16,18,13,(241,196,101))
jar.rect(13,18,14,2,(91,80,62))
jar.rect(14,23,12,2,(91,80,62))
jar.rect(9,36,22,5,(226,135,54))
jar.rect(8,39,24,4,(246,171,68))
jar.rect(15,43,10,4,(55,69,72))
jar.rect(17,46,6,2,(30,44,52))
jar.outline(OUTLINE)
jar.save(OUT/'feeder.png')

# 32-bit DIB icon derived from the same solid canister.
icon=Canvas(32,32)
for y in range(30):
    for x in range(25):
        sx=int(x*40/25); sy=int(y*48/30)
        p=jar.p[sy*40+sx]
        if p[3]:icon.dot(x+3,y+1,p)
raw=b''.join(bytes((b,g,r,a)) for y in reversed(range(32)) for r,g,b,a in icon.p[y*32:(y+1)*32])
mask=b'\0'*(4*32)
dib=struct.pack('<IIIHHIIIIII',40,32,64,1,32,0,len(raw),0,0,0,0)+raw+mask
(OUT/'feeder.ico').write_bytes(struct.pack('<HHH',0,1,1)+struct.pack('<BBBBHHII',32,32,0,0,1,32,len(dib),22)+dib)
print('Generated fish atlas: 4 species x 4 directions x 2 frames, plus solid feeder assets.')
