import numpy as np,cv2
from scipy import ndimage as ndi
G=np.load('head_grid.npy').astype(bool)          # 47x37, True = lit
H,W=G.shape
sil=ndi.binary_fill_holes(G)
# hair zone: everything outside the face box, above the jaw
r,c=np.mgrid[0:H,0:W]
face=(r>=9)&(c>=13)&(c<=31)
hair=(~face)&(r<36) | (r<9)
inner=sil&~G&hair                               # dark curl strokes inside the hair
lab,n=ndi.label(inner)
B=G.copy()
rng=np.random.default_rng(3)
for k in range(1,n+1):
    m=lab==k
    if m.sum()>14: continue                     # leave big gaps alone
    d=[(0,1),(1,0),(0,-1),(-1,0)][rng.integers(4)]
    sm=np.roll(m,d,axis=(0,1))
    if (sm&~sil).any() or (sm&~hair).any(): continue
    B[m]=True; B[sm]=False                      # stroke steps one art pixel
np.save('head_A.npy',G); np.save('head_B.npy',B)
viz=np.hstack([G,np.zeros((H,2),bool),B,np.zeros((H,2),bool),G^B])
cv2.imwrite('boil_new.png',cv2.resize(viz.astype(np.uint8)*255,None,fx=8,fy=8,interpolation=cv2.INTER_NEAREST))
print('changed cells',(G^B).sum(), 'components',n)
