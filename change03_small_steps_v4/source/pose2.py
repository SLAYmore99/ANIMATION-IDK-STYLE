import cv2,numpy as np,json
GL={226:225,227:229,228:229}
orb=cv2.ORB_create(8000); bf=cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
def img(f): return cv2.imread(f'fr/f{GL.get(f,f):03d}.png',0)
def step(a,b):
    A,B=img(a),img(b)
    if np.abs(A.astype(int)-B).mean()<0.5: return np.eye(3),9999
    k1,d1=orb.detectAndCompute(A,None); k2,d2=orb.detectAndCompute(B,None)
    m=bf.match(d1,d2)
    p1=np.float32([k1[x.queryIdx].pt for x in m]); p2=np.float32([k2[x.trainIdx].pt for x in m])
    M,inl=cv2.estimateAffinePartial2D(p1,p2,ransacReprojThreshold=2.0,maxIters=10000,confidence=0.999)
    return np.vstack([M,[0,0,1]]),int(inl.sum())
# T[f]: maps frame-f coords -> frame-229 coords
T={229:np.eye(3)}
for f in range(228,186,-1):
    S,n=step(f,f+1); T[f]=T[f+1]@S
    s=np.hypot(T[f][0,0],T[f][1,0])
    print(f,'step_s %.4f'%np.hypot(S[0,0],S[1,0]),'t %.1f %.1f'%(S[0,2],S[1,2]),'inl',n,'| cum scale_to_229 %.4f'%s)
json.dump({k:v.tolist() for k,v in T.items()},open('poses.json','w'))
