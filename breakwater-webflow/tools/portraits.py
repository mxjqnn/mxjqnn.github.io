# Team portraits with every head the same size: python3 portraits.py [R] ['<json tweaks>']
# 1. swift face-landmarks.swift <source photos> > lm.jsonl   (macOS Vision face box and landmarks)
# 2. run this in the folder holding lm.jsonl. It writes out/person-<slug>.png (1080 x 1350) plus contact sheets of the
#    card crop (sheet-cards.jpg) and pop-up crop (sheet-modals.jpg); save the PNGs as WebP quality 82 into assets/people/.
# R is the head measure (mean of the face box width and eye-to-chin / 0.708) as a share of the frame width: 0.315.
# Tweaks per slug: dy (frame shift in head measures, -0.15 lifts the frame so hair clears the card top), s (scale), N
# (rows of real background stretched upward when the photo has too little room above the head).
import json, math, os, sys, cv2, numpy as np
S=os.getcwd()   # work folder: holds lm.jsonl (from face-landmarks.swift) and receives out/ and the contact sheets
D='/Users/max/Dropbox/Work/Breakwater Initiative/01. Images/Staff-Team-Portraits/'
WHO={'2664':'molly-kinder','0292':'gretchen-phillips','0555':'palak-shah','2046':'anmol-chaddha','0976':'mayu-takeuchi','2257':'diana-degnan','1670':'samuel-thorpe'}
R=float(sys.argv[1]) if len(sys.argv)>1 else 0.315
ADJ=json.loads(sys.argv[2]) if len(sys.argv)>2 else {}   # per-person scale / dy tweaks
out=S+'/out'; os.makedirs(out,exist_ok=True); rows=[]
for line in open(S+'/lm.jsonl'):
    d=json.loads(line); k=d['file'][-8:-4]; who=WHO[k]
    x,y,w,h=d['box']; lp=d['leftPupil'][0]; rp=d['rightPupil'][0]
    eye=((lp[0]+rp[0])/2,(lp[1]+rp[1])/2); chin=max(d['contour'],key=lambda p:p[1])
    m=(w+(chin[1]-eye[1])/0.708)/2
    a=ADJ.get(who,{})
    m*=a.get('s',1.0)
    cx=x+w/2+a.get('dx',0)*m; cy=y+h/2+a.get('dy',0)*m
    fw=m/R; fh=fw*1.25
    x0=cx-fw/2; y0=cy-fh/2; x1=x0+fw; y1=y0+fh
    im=cv2.imread(D+d['file']); H,W=im.shape[:2]
    pad=[max(0,-y0),max(0,y1-H),max(0,-x0),max(0,x1-W)]
    info={'who':who,'src':k,'frame':[round(v) for v in (x0,y0,fw,fh)],'pad_px':[round(p) for p in pad],'scale':round(1080/fw,3)}
    assert pad[1]<0.5 and pad[2]<0.5 and pad[3]<0.5, (who,pad)
    if pad[0]>0.5:
        # not enough photo above the head: stretch the out-of-focus band at the top upward and soften it
        t=int(math.ceil(pad[0])); N=a.get('N',300)
        st=cv2.resize(im[:N],(W,N+t),interpolation=cv2.INTER_CUBIC)
        full=np.vstack([st, im[N:]]).astype(np.float32); real=np.vstack([st[:t], im]).astype(np.float32)
        al=np.zeros(real.shape[0],np.float32); al[:t]=1; r_=np.linspace(1,0,N); al[t:t+N]=r_*r_*(3-2*r_)
        mix=full*al[:,None,None]+real*(1-al[:,None,None])
        bl=cv2.GaussianBlur(mix,(0,0),40)
        g=np.clip((t+N*0.3-np.arange(real.shape[0]))/(t+N*0.3),0,1)[:,None,None]
        im=(mix*(1-g)+bl*g).astype(np.uint8); y0+=t
    xi,yi=int(round(x0)),int(round(y0)); wi,hi=int(round(fw)),int(round(fh))
    crop=im[yi:yi+hi, xi:xi+wi]
    res=cv2.resize(crop,(1080,1350),interpolation=cv2.INTER_AREA if wi>1080 else cv2.INTER_LANCZOS4)
    cv2.imwrite(out+'/person-%s.png'%who,res)
    rows.append((who,res)); print(json.dumps(info))
order=['molly-kinder','gretchen-phillips','palak-shah','anmol-chaddha','mayu-takeuchi','diana-degnan','samuel-thorpe']
rows.sort(key=lambda t:order.index(t[0]))
# contact sheets: card strip (1.78, with the notch) and pop-up (0.715)
cards=[]; modals=[]; fulls=[]
for who,res in rows:
    ch=int(round(1080/1.78)); c=res[(1350-ch)//2:(1350-ch)//2+ch].copy()
    c[:int(ch*.22), int(1080*.8):]=(40,40,40)
    cards.append(cv2.resize(c,(480,int(480/1.78))))
    mw=int(round(1350*0.715)); mm=res[:, (1080-mw)//2:(1080-mw)//2+mw]
    modals.append(cv2.resize(mm,(343,480)))
    fulls.append(cv2.resize(res,(384,480)))
def grid(tiles,cols,gap=12):
    h,w=tiles[0].shape[:2]; n=len(tiles); r=(n+cols-1)//cols
    g=np.full((r*h+(r+1)*gap, cols*w+(cols+1)*gap,3),43,np.uint8)
    for i,t in enumerate(tiles):
        yy=gap+(i//cols)*(h+gap); xx=gap+(i%cols)*(w+gap); g[yy:yy+h,xx:xx+w]=t
    return g
cv2.imwrite(S+'/sheet-cards.jpg',grid(cards,3),[cv2.IMWRITE_JPEG_QUALITY,88])
cv2.imwrite(S+'/sheet-modals.jpg',grid(modals,7),[cv2.IMWRITE_JPEG_QUALITY,88])
