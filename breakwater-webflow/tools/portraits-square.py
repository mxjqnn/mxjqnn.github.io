# Square portraits for fellows and advisors, cut from supplied headshots to the team head size (see BUILD-SHEET.md).
# 1. put the headshots in src/ named <slug>.jpg|png   2. swift face-landmarks.swift src/* > lm.jsonl
# 3. python3 portraits-square.py ['<json tweaks>']  ->  out/person-<slug>.png (1080 x 1080) and contact sheets
# Tweaks per slug: "ell": 1 adds a head ellipse to the hair mask (low-contrast hair), "s" scales the head, "dy"/"dx" shift it.
import json, math, os, sys, cv2, numpy as np
S=os.getcwd(); R=0.315; DY=-0.15
ADJ=json.loads(sys.argv[1]) if len(sys.argv)>1 else {}
ORDER=['asad-ramzanali','sam-manning','ioana-marinescu','brad-littlejohn','will-raderman','sam-hiner','devesh-kodnani','mary-olson',
       'michael-toscano','ganesh-sitaraman','oren-cass','roy-bahat','don-gips','elizabeth-wilkins','sam-hammond']
def smooth(n):
    r=np.linspace(1,0,n); return r*r*(3-2*r)
def extend(im, side, pad, N, soften, zone=None):
    """Add `pad` px on one side by stretching the outer N px outward, cross-faded into the real pixels; optionally softened.
    zone=(c0,c1): columns that may hold the head (top side only, for photos whose hair touches the top edge). Hair pixels in
    the band are found by their difference from the background either side, filled from that background before stretching,
    and left untouched in the photo itself, so hair is never dragged upward."""
    if side in ('bottom','right'): im=im[::-1,::-1]            # work on top/left, flip back after
    if side in ('left','right'): im=im.transpose(1,0,2)
    H,Wd=im.shape[:2]; N=max(8,min(int(N),H-1)); t=int(math.ceil(pad))
    band=np.ascontiguousarray(im[:N]).astype(np.float32); hair=np.zeros((N,Wd),np.float32)
    if zone:
        c0,c1=max(0,int(zone[0])),min(Wd,int(zone[1])); k=max(4,int(0.04*Wd))
        L=band[:, max(0,c0-k):max(1,c0)].mean(axis=1,keepdims=True) if c0>2 else None
        Rr=band[:, min(Wd-1,c1):min(Wd,c1+k)].mean(axis=1,keepdims=True) if c1<Wd-2 else None
        if L is None: L=Rr
        if Rr is None: Rr=L
        u=np.linspace(0,1,max(1,c1-c0))[None,:,None]
        interp=band.copy(); interp[:, c0:c1]=L*(1-u)+Rr*u
        D=cv2.GaussianBlur(np.abs(band-interp).max(axis=2),(0,0),2)
        hm=(D>26).astype(np.uint8); hm[:, :c0]=0; hm[:, c1:]=0
        kk=max(3,int(0.012*Wd))|1
        hm=cv2.dilate(hm,np.ones((kk,kk),np.uint8))
        hair=cv2.GaussianBlur(hm.astype(np.float32),(0,0),max(1.5,0.004*Wd))
        band=band*(1-hair[...,None])+cv2.GaussianBlur(interp,(0,0),max(2,0.008*Wd))*hair[...,None]
    st=cv2.resize(band,(Wd,N+t),interpolation=cv2.INTER_CUBIC)
    full=np.vstack([st, im[N:].astype(np.float32)]); real=np.vstack([st[:t], im.astype(np.float32)])
    al=np.zeros((real.shape[0],Wd),np.float32); al[:t]=1; al[t:t+N]=smooth(N)[:,None]*(1-np.clip(hair*1.5,0,1))
    mix=full*al[...,None]+real*(1-al[...,None])
    if soften:
        bl=cv2.GaussianBlur(mix,(0,0),soften)
        g=np.clip((t+N*0.3-np.arange(real.shape[0]))/(t+N*0.3),0,1)[:,None]*np.ones((1,Wd),np.float32)
        g[t:t+N]*=(1-np.clip(hair*1.5,0,1))
        mix=mix*(1-g[...,None])+bl*g[...,None]
    out=np.clip(mix,0,255).astype(np.uint8)
    if side in ('left','right'): out=out.transpose(1,0,2)
    if side in ('bottom','right'): out=out[::-1,::-1]
    return np.ascontiguousarray(out)
def mirror(im, side, pad, soften):
    """Add `pad` px on the left or right by reflecting the edge, softened progressively towards the new edge."""
    t=int(math.ceil(pad)); l,r=(t,0) if side=='left' else (0,t)
    ext=cv2.copyMakeBorder(im,0,0,l,r,cv2.BORDER_REFLECT_101).astype(np.float32)
    bl=cv2.GaussianBlur(ext,(0,0),soften)
    g=np.zeros(ext.shape[1],np.float32); ramp=np.clip(np.arange(t,0,-1)/max(1,t)*1.2,0,1)
    if side=='left': g[:t]=ramp
    else: g[-t:]=ramp[::-1]
    g=cv2.GaussianBlur(g[None,:],(0,0),max(2,t*0.08))[0][None,:,None]
    return np.clip(ext*(1-g)+bl*g,0,255).astype(np.uint8)
def person_mask(im, cx, x, y, w, h, m):
    """Rough person-vs-background mask (GrabCut seeded from the face box), so the fill knows where the hair really is."""
    H,Wd=im.shape[:2]; sc=min(1.0,480/max(H,Wd))
    sm=cv2.resize(im,None,fx=sc,fy=sc,interpolation=cv2.INTER_AREA); hh,ww=sm.shape[:2]
    P=lambda v:int(round(v*sc))
    gm=np.full((hh,ww),cv2.GC_PR_BGD,np.uint8)
    cv2.ellipse(gm,(P(cx),P(y+0.45*h)),(P(0.85*m),P(0.45*h+0.8*m)),0,0,360,cv2.GC_PR_FGD,-1)
    gm[P(y+h):, max(0,P(cx-1.8*m)):P(cx+1.8*m)]=cv2.GC_PR_FGD
    gm[:max(0,P(y-0.9*m)), :]=cv2.GC_BGD
    top=P(y+0.3*h); gm[:top, :max(0,P(cx-1.5*m))]=cv2.GC_BGD; gm[:top, P(cx+1.5*m):]=cv2.GC_BGD
    gm[P(y+0.1*h):P(y+0.95*h), P(x+0.15*w):P(x+0.85*w)]=cv2.GC_FGD
    gm[P(y+h):P(y+h+0.6*m), P(cx-0.25*m):P(cx+0.25*m)]=cv2.GC_FGD
    bg=np.zeros((1,65),np.float64); fg=np.zeros((1,65),np.float64)
    cv2.grabCut(sm,gm,None,bg,fg,5,cv2.GC_INIT_WITH_MASK)
    pm=((gm==cv2.GC_FGD)|(gm==cv2.GC_PR_FGD)).astype(np.uint8)*255
    pm=cv2.resize(pm,(Wd,H),interpolation=cv2.INTER_LINEAR)
    k=max(3,int(0.05*m))|1
    return cv2.dilate((pm>100).astype(np.uint8)*255,np.ones((k,k),np.uint8))
def mirror_top(im, pad, soften, pm):
    """Add `pad` px above the photo by reflecting its top rows. pm is the person mask: any head or hair inside the reflected
    rows is painted out first, so no second head appears above the real one."""
    H,Wd=im.shape[:2]; t=min(int(math.ceil(pad)),H-2)
    src=np.ascontiguousarray(im[:t+2]).copy(); mask=np.ascontiguousarray(pm[:t+2])
    if mask.any():
        sc=min(1.0,700/max(src.shape[:2]))
        sm=cv2.resize(src,None,fx=sc,fy=sc,interpolation=cv2.INTER_AREA); mm=cv2.resize(mask,(sm.shape[1],sm.shape[0]),interpolation=cv2.INTER_NEAREST)
        rad=max(3,int(6*sc))
        # first pass finds what the background looks like; masked pixels that already match it are background, not hair
        f0=cv2.inpaint(sm,mm,rad,cv2.INPAINT_TELEA)
        D=cv2.GaussianBlur(np.abs(sm.astype(np.float32)-f0.astype(np.float32)).max(axis=2),(0,0),1.5)
        mm=((mm>0)&(D>12)).astype(np.uint8)*255
        mm=cv2.dilate(mm,np.ones((5,5),np.uint8))
        fill=cv2.inpaint(sm,mm,rad,cv2.INPAINT_TELEA)
        fill=cv2.GaussianBlur(cv2.resize(fill,(Wd,src.shape[0]),interpolation=cv2.INTER_CUBIC),(0,0),max(2,0.006*Wd))
        mask=cv2.resize(mm,(Wd,src.shape[0]),interpolation=cv2.INTER_LINEAR)
        f=np.clip(cv2.GaussianBlur(mask.astype(np.float32)/255,(0,0),max(1.5,0.004*Wd))*1.6,0,1)[...,None]
        src=(src*(1-f)+fill*f).astype(np.uint8)
    ext=np.vstack([src[1:t+1][::-1], im]).astype(np.float32)
    bl=cv2.GaussianBlur(ext,(0,0),soften)
    g=np.zeros(ext.shape[0],np.float32); g[:t]=np.clip(np.arange(t,0,-1)/max(1,t)*1.5,0,1)
    g=g[:,None,None]
    out=ext*(1-g)+bl*g
    if mask[0].any():                                       # hair cut off by the photo's top edge: soften the cut a little
        k=max(3,int(0.006*Wd)); r0,r1=max(0,t-3*k),t+3*k
        strip=cv2.GaussianBlur(out[r0:r1],(1,0),sigmaX=0.1,sigmaY=k)
        cw=np.clip(cv2.GaussianBlur((mask[0:1]>0).astype(np.float32),(0,0),k)*1.5,0,1)[0][None,:,None]
        rw=np.exp(-((np.arange(r0,r1)-t)/(1.5*k))**2)[:,None,None]
        out[r0:r1]=out[r0:r1]*(1-cw*rw)+strip*(cw*rw)
    return np.clip(out,0,255).astype(np.uint8)
os.makedirs(S+'/out',exist_ok=True); res={}
for line in open(S+'/lm.jsonl'):
    d=json.loads(line); who=os.path.splitext(d['file'])[0]; a=ADJ.get(who,{})
    x,y,w,h=d['box']; lp=d['leftPupil'][0]; rp=d['rightPupil'][0]
    eye=((lp[0]+rp[0])/2,(lp[1]+rp[1])/2); chin=max(d['contour'],key=lambda p:p[1])
    m=(w+(chin[1]-eye[1])/0.708)/2*a.get('s',1.0)
    cx=x+w/2+a.get('dx',0)*m; cy=y+h/2+a.get('dy',DY)*m; fw=m/R
    im=cv2.imread(S+'/src/'+d['file']); H,W=im.shape[:2]
    x0=cx-fw/2; y0=cy-fw/2
    pad={'left':max(0,-x0),'right':max(0,x0+fw-W),'top':max(0,-y0),'bottom':max(0,y0+fw-H)}
    soft=fw/90
    if pad['top']>0.5:
        m0=m/a.get('s',1.0); pm=person_mask(im,x+w/2,x,y,w,h,m0)
        if a.get('ell'):                                    # low-contrast hair: add a generous head ellipse (pruned again later)
            cv2.ellipse(pm,(int(x+w/2),int(y+0.45*h)),(int(0.80*m0),int(0.45*h+0.72*m0)),0,0,360,255,-1)
        cv2.imwrite(S+'/out/mask-%s.png'%who,cv2.resize(pm,None,fx=300/H,fy=300/H))
        im=mirror_top(im,pad['top'],fw/40,pm); y0+=min(int(math.ceil(pad['top'])),H-2)
    nb=max(pad['bottom']*1.5,0.08*fw)
    if pad['bottom']>0.5: im=extend(im,'bottom',pad['bottom'],a.get('NB',nb),0)
    if pad['left']>0.5: im=mirror(im,'left',pad['left'],soft); x0+=math.ceil(pad['left'])
    if pad['right']>0.5: im=mirror(im,'right',pad['right'],soft)
    xi,yi,si=int(round(x0)),int(round(y0)),int(round(fw))
    crop=im[yi:yi+si, xi:xi+si]
    out=cv2.resize(crop,(1080,1080),interpolation=cv2.INTER_AREA if si>1080 else cv2.INTER_LANCZOS4)
    cv2.imwrite(S+'/out/person-%s.png'%who,out); res[who]=out
    print('%-24s scale %.2f  pad%% of side T/B/L/R: %s' % (who,1080/fw,' '.join('%2d'%round(100*pad[k]/fw) for k in ('top','bottom','left','right'))))
tiles=[res[k] for k in ORDER if k in res]
def grid(ts,cols,gap=10):
    h,w=ts[0].shape[:2]; r=(len(ts)+cols-1)//cols
    g=np.full((r*h+(r+1)*gap, cols*w+(cols+1)*gap,3),43,np.uint8)
    for i,t in enumerate(ts):
        yy=gap+(i//cols)*(h+gap); xx=gap+(i%cols)*(w+gap); g[yy:yy+h,xx:xx+w]=t
    return g
cards=[]; modals=[]
for t in tiles:
    ch=int(round(1080/1.78)); c=t[(1080-ch)//2:(1080-ch)//2+ch].copy(); c[:int(ch*.22), int(1080*.8):]=(40,40,40)
    cards.append(cv2.resize(c,(420,int(420/1.78))))
    mw=int(round(1080*0.715)); modals.append(cv2.resize(t[:, (1080-mw)//2:(1080-mw)//2+mw],(250,350)))
cv2.imwrite(S+'/sheet-cards.jpg',grid(cards,4),[cv2.IMWRITE_JPEG_QUALITY,88])
cv2.imwrite(S+'/sheet-modals.jpg',grid(modals,9),[cv2.IMWRITE_JPEG_QUALITY,88])
