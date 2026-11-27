# Mike Kubzansky: the supplied photo is a tight 800 px crop in front of a sponsor wall, with another person's hair in the
# corner. To reach the common head size the frame has to be far bigger than the photo, so the wall's logos and the hair are
# painted out, the plain backdrop is continued on every side, and the shoulders and jacket are continued below.
# Run in a folder holding src/mike-kubzansky.png and lm.jsonl (from face-landmarks.swift); writes out/person-mike-kubzansky.png.
import cv2, numpy as np, json, math
im=cv2.imread('src/mike-kubzansky.png').astype(np.float32); H,W=im.shape[:2]; k=W/600.0
P=lambda v:int(round(v*k))
yy,xx=np.mgrid[0:H,0:W]
bg=np.median(im[P(150):P(215),P(8):P(40)].reshape(-1,3),axis=0)
notbg=np.abs(im-bg).max(axis=2)>16
navyish=(im.max(axis=2)<125)&(im[...,0]>=im[...,2]-4)
def zone(x0,x1,y0,y1):
    z=np.zeros((H,W),bool); z[P(y0):P(y1),P(x0):P(x1)]=True; return z
b,g,r=im[...,0],im[...,1],im[...,2]
orange=(r>170)&(r-b>45); blue=(b-r>18)&(b>80)
mask=np.zeros((H,W),bool)
mask|=zone(0,58,0,385)&notbg                                   # everything at the left edge above the shoulder (wall text)
mask|=zone(58,92,285,380)&blue                                 # the ends of "Newh" and "Public" next to his cheek
mask|=(zone(383,600,0,62)|zone(418,600,62,118))&notbg          # logo block, top right
mask|=zone(448,600,495,572)&notbg&~navyish&orange              # "Syracuse", bottom right
mask=cv2.dilate(mask.astype(np.uint8),np.ones((P(5)|1,P(5)|1),np.uint8))>0
clean=cv2.inpaint(im.astype(np.uint8),mask.astype(np.uint8)*255,P(6),cv2.INPAINT_TELEA).astype(np.float32)
navy=np.median(clean[P(575):P(598),P(105):P(150)].reshape(-1,3),axis=0)
# shoulder lines: left one starts where his jacket disappears behind the other person's hair, right one follows the jacket edge
AX,AY,SL=P(96),P(548),0.36
dkc=(clean.max(axis=2)<125)
x2=W-P(6); x1=W-P(50)
t1=np.argmax(dkc[:,x1]) if dkc[:,x1].any() else H; t2=np.argmax(dkc[:,x2]) if dkc[:,x2].any() else H
SR=float(np.clip((t2-t1)/max(1,x2-x1),0.3,0.8))
def sil(X,Y,ox,oy):                                             # True where a pixel at canvas (X,Y) belongs to the jacket continuation
    xs=X-ox; ys=Y-oy
    f=np.where(xs<AX, AY+(AX-xs)*SL, np.where(xs>x2, t2+(xs-x2)*SR, H))
    return ys>f
# the other person's hair, bottom left: backdrop above the shoulder line, jacket below it
hair=(xx<P(80))&(yy>P(383))&(clean.max(axis=2)<190)&~((clean[...,0]-clean[...,2]>18)&(xx>P(62)))
hair=cv2.dilate(hair.astype(np.uint8),np.ones((P(7)|1,P(7)|1),np.uint8))>0
hair&=(xx<AX)&(yy>P(375))
fill=np.where(sil(xx,yy,0,0)[...,None],navy,bg).astype(np.float32)
soft=cv2.GaussianBlur(hair.astype(np.float32),(0,0),P(2.5))[...,None]
clean=clean*(1-soft)+cv2.GaussianBlur(fill,(0,0),P(1.5))*soft
cv2.imwrite('mike-clean.jpg',clean.astype(np.uint8))
# frame at the common head size (same rule as portraits-square.py)
d=[json.loads(l) for l in open('lm.jsonl') if 'mike' in l][0]
x,y,w,h=d['box']; lp=d['leftPupil'][0]; rp=d['rightPupil'][0]; eye=((lp[0]+rp[0])/2,(lp[1]+rp[1])/2); chin=max(d['contour'],key=lambda p:p[1])
m=(w+(chin[1]-eye[1])/0.708)/2; fw=m/0.315; cx=x+w/2; cy=y+h/2-0.15*m
x0=cx-fw/2; y0=cy-fw/2
pl,pr,pt,pb=[int(math.ceil(max(0,v))) for v in (-x0, x0+fw-W, -y0, y0+fw-H)]
print('frame',round(fw),'added L R T B',pl,pr,pt,pb)
IN=P(4)                                                         # the file has a dark line on its border: stay a few pixels inside
def backdrop(band, axis):                                       # an even backdrop gradient taken from a band at the photo's edge
    p=np.median(band,axis=axis); light=p.max(axis=1)>190
    ref=np.median(p[light],axis=0) if light.any() else bg
    p=np.where((np.abs(p-ref).max(axis=1)>14)[:,None],ref,p)
    return cv2.GaussianBlur(p[None].astype(np.float32),(0,0),P(45))[0]
Lp=backdrop(clean[:, IN:IN+P(6)],1); Rp=backdrop(clean[:, W-IN-P(6):W-IN],1)
CW,CH=pl+W+pr,pt+H+pb
Tp=backdrop(clean[IN:IN+P(6)],0)                               # backdrop along the photo's top edge
canvas=np.zeros((CH,CW,3),np.float32)
# backdrop: each added area takes the colour of the photo edge it touches, so there is no step at the join
canvas[pt:pt+H, :pl]=Lp[:,None,:]; canvas[pt:pt+H, pl+W:]=Rp[:,None,:]
Trow=np.vstack([np.repeat(Lp[:1],pl,axis=0),Tp,np.repeat(Rp[:1],pr,axis=0)]); Trow=cv2.GaussianBlur(Trow[None],(0,0),P(30))[0]
canvas[:pt]=Trow[None]
uu=np.linspace(0,1,W)[:,None]
Brow=np.vstack([np.repeat(Lp[-1:],pl,axis=0),Lp[-1:]*(1-uu)+Rp[-1:]*uu,np.repeat(Rp[-1:],pr,axis=0)])
canvas[pt+H:]=Brow[None]
# jacket continuation: every column keeps the colour the jacket has where the photo ends (the lit lapel stays lighter)
Bp=np.median(clean[H-IN-P(3):H-IN],axis=0); dk=Bp.max(axis=1)<140; cols=np.where(dk)[0]; jl,jr=cols.min(),cols.max()
openc=np.where(~dk[jl:jr+1])[0]+jl; ol,orr=openc.min(),openc.max()
jc=Bp.copy(); vv=np.linspace(0,1,orr-ol+1)[:,None]
jc[ol:orr+1]=Bp[max(jl,ol-P(4))]*(1-vv)+Bp[min(jr,orr+P(4))]*vv
jc[:jl]=Bp[jl+P(3)]; jc[jr+1:]=Bp[jr-P(3)]
jcol=np.vstack([np.repeat(jc[:1],pl,axis=0),jc,np.repeat(jc[-1:],pr,axis=0)]); jcol=cv2.GaussianBlur(jcol[None],(0,0),P(5))[0]
Y,X=np.mgrid[0:CH,0:CW]
canvas=np.where(sil(X,Y,pl,pt)[...,None],np.broadcast_to(jcol[None],canvas.shape),canvas)
# the open collar narrows to a point below the photo
close=int(0.5*pb); c=(ol+orr)/2
for j in range(close):
    f=1-j/close; a_=int(round(c-f*(orr-ol)/2)); b_=int(round(c+f*(orr-ol)/2))
    if b_-a_>=2: canvas[pt+H+j, pl+a_:pl+b_]=cv2.resize(Bp[None, ol:orr+1].astype(np.float32),(b_-a_,1),interpolation=cv2.INTER_AREA)[0]
# the photo's own border strip (dark line) is replaced by what lies just inside it
inner=clean.copy()
inner[:, :IN]=inner[:, IN:IN+1]; inner[:, W-IN:]=inner[:, W-IN-1:W-IN]; inner[:IN]=inner[IN:IN+1]; inner[H-IN:]=inner[H-IN-1:H-IN]
canvas[pt:pt+H, pl:pl+W]=inner
outer=cv2.GaussianBlur(canvas,(0,0),P(2))
canvas=outer; canvas[pt:pt+H, pl:pl+W]=inner
seam=np.zeros((CH,CW),np.float32); seam[pt:pt+H, pl:pl+W]=1                      # feather the join
edge=cv2.GaussianBlur(seam,(0,0),P(3)); ring=(np.abs(edge-0.5)<0.48).astype(np.float32)
ring=cv2.GaussianBlur(ring,(0,0),P(1.5))[...,None]
canvas=canvas*(1-ring)+cv2.GaussianBlur(canvas,(0,0),P(2.5))*ring
xi,yi,si=int(round(x0+pl)),int(round(y0+pt)),int(round(fw))
out=cv2.resize(np.clip(canvas[yi:yi+si, xi:xi+si],0,255).astype(np.uint8),(1080,1080),interpolation=cv2.INTER_AREA)
cv2.imwrite('out/person-mike-kubzansky.png',out)
