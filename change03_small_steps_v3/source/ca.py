import numpy as np, cv2
# radial lateral chromatic aberration: zero in the centre, grows with r^2 to MAXPX at the corners
H,W=1080,1920
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
cx,cy=(W-1)/2,(H-1)/2
r2=((xx-cx)**2+(yy-cy)**2)/(cx**2+cy**2)
def maps(px):
    k=px*r2/np.sqrt(cx**2+cy**2)          # fractional radial scale per pixel
    return [((cx+(xx-cx)*(1+s*k)).astype(np.float32), (cy+(yy-cy)*(1+s*k)).astype(np.float32)) for s in (-1,1)]
_cache={}
def ca(rgb,px=3.0):
    if px<=0: return rgb
    if px not in _cache: _cache[px]=maps(px)
    (rx,ry),(bx,by)=_cache[px]
    rgb=np.ascontiguousarray(rgb,np.float32); out=rgb.copy()
    out[...,0]=cv2.remap(rgb[...,0],rx,ry,cv2.INTER_LINEAR)   # red pushed outward
    out[...,2]=cv2.remap(rgb[...,2],bx,by,cv2.INTER_LINEAR)   # blue pulled inward
    return out
