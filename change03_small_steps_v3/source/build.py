import numpy as np, cv2, os, sys
from scipy import ndimage as ndi
FR='fr'; OUT=sys.argv[1] if len(sys.argv)>1 else 'comp'
os.makedirs(OUT,exist_ok=True)
N=305
def load(f): return cv2.imread(f'{FR}/f{f:03d}.png')[...,::-1].astype(np.float32)   # RGB

# ---------- clean black floor (kill h264 noise so alpha stays clean) ----------
def floor(im): return np.clip((im-6.0)*255/249,0,255)

# ---------- new head ----------
A=np.load('head_A.npy'); B=np.load('head_B.npy')
GH,GW=A.shape; CELL=4.5
X0=503.5-GW*CELL/2; Y1=648.0; Y0=Y1-GH*CELL          # same centre + baseline as the old bust
BOX=(395,612,380,712)                                 # x0,x1,y0,y1 erase box of old character
def head_mask(grid, dy=0):
    """grid -> float mask on the full frame (nearest cells, 2x supersampled edges)"""
    S=2; c=CELL*S
    big=np.zeros((1080*S,1920*S),np.float32)
    ys=(np.arange(GH+1)*c+(Y0+dy)*S).round().astype(int); xs=(np.arange(GW+1)*c+X0*S).round().astype(int)
    for j in range(GH):
        row=grid[j]
        for i in np.where(row)[0]:
            big[ys[j]:ys[j+1], xs[i]:xs[i+1]]=1
    return cv2.resize(big,(1920,1080),interpolation=cv2.INTER_AREA)
def native_glow(m):      # match the soft edge glow the rest of the clip already has
    return np.clip(m+cv2.GaussianBlur(m,(0,0),1.0)*0.12,0,1.2)

def boil_state(f):
    if f>=142: f=141
    return ((f-1)//6)%2
ENTRY={2:56,3:56,4:56,5:20,6:20,7:20,8:4,9:4,10:4}   # stepped rise, measured (old top 496/460/444/440)

# ---------- reference of the old clean character for glitch-shift measurement ----------
x0,x1,y0,y1=BOX
ref=load(113)[y0:y1,x0:x1].max(2)>110
BAND=9
def row_shifts(old):
    """horizontal offset of each 9-px band of the old character vs its clean drawing"""
    on=old.max(2)>90
    dx=np.zeros(y1-y0,int); bands=[]
    for b0 in range(0,y1-y0,BAND):
        r=ref[b0:b0+BAND]; o=on[b0:b0+BAND]
        if r.sum()<20 or o.sum()<20: bands.append(0); continue
        e0=np.logical_xor(r,o).sum()
        es=[(np.logical_xor(np.roll(r,s,axis=1),o).sum(),abs(s),s) for s in range(-40,41)]
        e,_,s=min(es)
        bands.append(s if e<e0*0.7 else 0)
    bands=ndi.median_filter(np.array(bands),3,mode='nearest')
    for i,s in enumerate(bands): dx[i*BAND:(i+1)*BAND]=s
    return dx

def small_components(on,maxarea=90):
    lab,n=ndi.label(on); sizes=ndi.sum(on,lab,range(1,n+1))
    keep=np.zeros_like(on)
    for k,s in enumerate(sizes,1):
        if s<=maxarea: keep|=lab==k
    return keep

WHITE=np.array([236,236,232],np.float32)
RED=np.array([250,73,67],np.float32)
def char_colour(old_box, ref_lum):
    px=old_box[old_box.max(2)>170]
    if len(px)<50: return WHITE,0
    col=np.median(px,0)
    lum=old_box.max(2)[old_box.max(2)>40].sum()
    return col, lum/ref_lum
RED_LUM=load(139)[y0:y1,x0:x1].max(2); RED_LUM=RED_LUM[RED_LUM>40].sum()

def do_head(f, im):
    old=im[y0:y1,x0:x1].copy()
    oldon=old.max(2)>60
    if not oldon.any(): return im
    parts=small_components(oldon)             # particles of the scramble: keep them
    col={114:np.array([238,180,170],np.float32),115:np.array([240,150,140],np.float32)}.get(f, RED if f>=116 else WHITE)
    grid=B if boil_state(f) else A
    m=head_mask(grid,ENTRY.get(f,0))
    if 114<=f<=161:
        dx=row_shifts(old)
        mb=m[y0:y1,x0:x1].copy(); sh=np.zeros_like(mb)
        for y in range(y1-y0): sh[y]=np.roll(mb[y],dx[y])
        if f in (140,141):                     # the old bust dithers dim for two frames
            yy,xx=np.mgrid[0:y1-y0,0:x1-x0]; sh*=0.55+0.45*((yy//2+xx//2)%2==0)
        m=np.zeros_like(m); m[y0:y1,x0:x1]=sh
        lum=old.max(2); lum=lum[lum>40].sum()/RED_LUM
        k=min(1.0,lum/0.98) if f not in (140,141) else 1.0
        col=col*k
    g=native_glow(m)
    keep=im.copy()
    region=im[y0:y1,x0:x1]
    region[~parts]=0                          # erase the old character, keep scramble particles
    im[y0:y1,x0:x1]=region
    hc=g[...,None]*col[None,None,:]
    hc=hc/np.maximum(1.0,hc.max(2,keepdims=True)/255.0)     # hue-preserving, red stays red
    im=np.maximum(im, hc)
    return np.clip(im,0,255)

# ---------- ending: remove glitch bursts, continue the zoom-out ----------
GLITCH={226:225,227:229,228:229, 243:242,244:246,245:246, 271:270,272:274,273:274, 288:287,289:291,290:291}
Z0=228; TAU=80.0; AMP=0.21           # starts at the measured end rate (~0.26 %/f), 0.87 by the last frame
def zoom_scale(f):
    t=max(0,f-Z0); return 1-AMP*(1-np.exp(-t/TAU))
def do_zoom(im,s):
    if s>=0.99999: return im
    feather=2.5*(1-s)*540             # fade the plate's cut edges as they come on screen
    yy=np.arange(1080)[:,None]; xx=np.arange(1920)[None,:]
    d=np.minimum(np.minimum(yy,1079-yy),np.minimum(xx,1919-xx)).astype(np.float32)
    w=np.clip(d/max(feather,1),0,1); w=w*w*(3-2*w)
    im=im*w[...,None]
    M=np.float32([[s,0,960*(1-s)],[0,s,540*(1-s)]])
    return cv2.warpAffine(im,M,(1920,1080),flags=cv2.INTER_AREA if s<1 else cv2.INTER_LINEAR,borderValue=0)

frames=range(1,N+1) if len(sys.argv)<3 else [int(x) for x in sys.argv[2].split(',')]
for f in frames:
    src=GLITCH.get(f,f)
    im=floor(load(src))
    if 2<=f<=161: im=do_head(f,im)
    if f>=Z0: im=do_zoom(im,zoom_scale(f))
    np.save(f'{OUT}/c{f:03d}.npy',im.astype(np.float16)) if False else cv2.imwrite(f'{OUT}/c{f:03d}.png',np.clip(im,0,255).astype(np.uint8)[...,::-1])
    print(f,end=' ',flush=True)
