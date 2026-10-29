import cv2,numpy as np
im=cv2.imread('head_ref.jpg',0).astype(float)
im[800:,1450:]=0  # drop gemini sparkle
p=13.45
best=None
for ox in np.arange(0,p,0.25):
  for oy in np.arange(0,p,0.25):
    xs=ox+p*np.arange(int((1599-ox)/p)); ys=oy+p*np.arange(int((887-oy)/p))
    # sample 3x3 inner around centres; score = mean distance from 0/255 decision
    cx=(xs[:-1]+p/2).astype(int); cy=(ys[:-1]+p/2).astype(int)
    v=im[np.ix_(cy,cx)]
    s=np.abs(v-128).mean()
    if best is None or s>best[0]: best=(s,ox,oy)
print(best)
s,ox,oy=best
nx=int((1599-ox)/p)-1; ny=int((887-oy)/p)-1
G=np.zeros((ny,nx),np.uint8)
for j in range(ny):
  for i in range(nx):
    x0=int(ox+i*p+p*0.3); x1=int(ox+i*p+p*0.7); y0=int(oy+j*p+p*0.3); y1=int(oy+j*p+p*0.7)
    G[j,i]=im[y0:y1,x0:x1].mean()>128
ys,xs=np.where(G); G=G[ys.min():ys.max()+1, xs.min():xs.max()+1]
print(G.shape)
np.save('head_grid.npy',G)
cv2.imwrite('head_grid_x10.png',cv2.resize(G*255,None,fx=10,fy=10,interpolation=cv2.INTER_NEAREST))
for r in G: print(''.join('#' if c else '.' for c in r))
