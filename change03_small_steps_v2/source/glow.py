import numpy as np, cv2, sys, os
# house screen glow: tight bloom + wide halo, faint scanlines, hue-preserving tonemap
K_CORE,K_H1,K_H2=[float(x) for x in os.environ.get('GLOW','0.7,0.6,0.42').split(',')]
SCAN=np.ones((1080,1,1),np.float32); SCAN[2::3]=0.90
def glow(rgb):
    cv=rgb.astype(np.float32)
    core=cv2.GaussianBlur(cv,(0,0),1.6)*K_CORE
    halo=cv2.GaussianBlur(cv,(0,0),9)*K_H1+cv2.GaussianBlur(cv,(0,0),28)*K_H2
    out=(cv+core+halo)*SCAN
    m=out.max(2,keepdims=True); return out/np.maximum(1.0,m/255.0)
def to_rgba(rgb):
    a=np.clip(rgb.max(2)/255.0,0,1)
    col=np.where(a[...,None]>1e-4,rgb/np.maximum(a[...,None],1e-4),0)
    return np.dstack([np.clip(col,0,255),a*255]).astype(np.uint8)
if __name__=='__main__':
    src,dst=sys.argv[1],sys.argv[2]; os.makedirs(dst,exist_ok=True)
    rgba=len(sys.argv)>4 and sys.argv[4]=='rgba'
    if rgba: os.makedirs(dst+'_a',exist_ok=True)
    fs=[int(x) for x in sys.argv[3].split(',')] if len(sys.argv)>3 and sys.argv[3]!='all' else range(1,306)
    for f in fs:
        im=cv2.imread(f'{src}/c{f:03d}.png')[...,::-1]
        o=glow(im)
        cv2.imwrite(f'{dst}/f{f:03d}.png',np.clip(o,0,255).astype(np.uint8)[...,::-1])
        if rgba:
            q=to_rgba(o); cv2.imwrite(f'{dst}_a/f{f:03d}.png',q[...,[2,1,0,3]])
