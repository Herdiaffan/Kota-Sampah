from PIL import Image, ImageDraw, ImageFilter
import numpy as np, random, os, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent/'assets'/'materials'
ROOT.mkdir(parents=True,exist_ok=True)
S=1024
# Each atlas is a real, used 4x4 tileable material set. High-resolution files are streamed only in HIGH mode.
PAGES={
'city':[
('grass',(76,135,71),'grass'),('asphalt',(56,62,65),'asphalt'),('concrete',(153,157,148),'concrete'),('stucco',(194,178,150),'stucco'),
('brick',(158,82,61),'brick'),('glass-facade',(70,139,163),'glass'),('roof-tile',(150,77,52),'roof'),('water-ripple',(43,118,153),'water'),
('stone-pavers',(154,162,148),'pavers'),('soil',(101,76,53),'soil'),('painted-wall',(124,166,132),'paint'),('granite',(137,143,139),'granite'),
('lane-marking',(67,74,77),'roadmark'),('gravel',(125,120,106),'gravel'),('curb-stone',(169,169,153),'curb'),('drain-metal',(75,84,82),'drain')],
'props':[
('wood-grain',(123,83,50),'wood'),('brushed-metal',(137,151,154),'metal'),('uniform-fabric',(56,129,84),'fabric'),('scuffed-plastic',(64,151,105),'plastic'),
('rubber',(45,49,47),'rubber'),('foliage',(48,132,68),'foliage'),('painted-steel',(82,119,98),'paintedmetal'),('aluminum',(172,181,181),'aluminum'),
('bottle-glass',(71,158,173),'bottleglass'),('corrugated-cardboard',(164,120,72),'cardboard'),('paper-fiber',(218,213,194),'paper'),('ceramic-tile',(198,211,194),'ceramic'),
('reflective-tape',(210,221,163),'reflective'),('grip-rubber',(54,57,56),'rubber'),('recycled-flakes',(116,151,106),'flakes'),('woven-mat',(143,119,84),'weave')],
'waste':[
('pet-bottle',(73,166,181),'bottle'),('plastic-wrapper',(71,164,113),'wrapper'),('box-cardboard',(158,115,67),'box'),('crumpled-paper',(220,215,198),'paper'),
('aluminum-can',(170,181,184),'can'),('glass-fragments',(85,157,163),'glass'),('organic-leaves',(82,135,61),'organic'),('circuit-board',(39,96,71),'circuit'),
('textile-scrap',(76,118,86),'fabric'),('mixed-litter',(116,120,104),'mixed'),('blue-pet',(63,133,191),'bottle'),('food-container',(211,201,177),'container'),
('e-waste-board',(43,80,65),'circuit'),('compost',(111,88,52),'soil'),('recycling-bin-polymer',(56,138,92),'plastic'),('recycled-pellets',(95,131,87),'pellets')]
}

def seamless(a, band=24):
    # Blend the border into the opposite border so the shader can tile a texture without obvious seams.
    a=a.astype(np.float32,copy=False)
    h,w,_=a.shape
    for i in range(band):
        t=(i+1)/(band+1)
        mix=(a[i,:,:]*(t)+a[h-band+i,:,:]*(1-t))
        a[i,:,:]=mix
        a[h-band+i,:,:]=(a[h-band+i,:,:]*(t)+a[i,:,:]*(1-t))
    for i in range(band):
        t=(i+1)/(band+1)
        mix=a[:,i,:]*t+a[:,w-band+i,:]*(1-t)
        a[:,i,:]=mix
        a[:,w-band+i,:]=a[:,w-band+i,:]*t+a[:,i,:]*(1-t)
    return np.clip(a,0,255).astype(np.uint8)

def make_tile(base,style,seed):
    rng=np.random.default_rng(seed)
    # Correlated macro variation plus high-frequency surface granularity; these are surface textures, not padding.
    coarse=rng.normal(0,11,(64,64,3)).astype(np.float32)
    coarse_img=Image.fromarray(np.uint8(np.clip(coarse+128,0,255)),'RGB').resize((S,S),Image.Resampling.BICUBIC)
    c=np.asarray(coarse_img).astype(np.float32)-128
    fine=rng.normal(0,7.2,(S,S,3)).astype(np.float32)
    yy,xx=np.mgrid[0:S,0:S]
    xf=xx/S; yf=yy/S
    a=np.empty((S,S,3),dtype=np.float32); a[:]=np.array(base,dtype=np.float32)
    a+=c*.55+fine
    # Material-specific periodic structure.
    if style in ('grass','foliage','organic'):
        waves=(np.sin(xx*.11+np.sin(yy*.013)*3)+np.sin(yy*.14+np.cos(xx*.017)*2)) * 5
        a[:,:,1]+=waves*1.5; a[:,:,0]+=waves*.4; a[:,:,2]+=waves*.25
        mask=((xx*17+yy*31+seed)%137)<3
        a[mask,0]*=.63; a[mask,1]=np.minimum(255,a[mask,1]*1.13); a[mask,2]*=.58
    elif style in ('asphalt','concrete','granite','gravel','soil','curb','drain'):
        period={'asphalt':19,'concrete':31,'granite':13,'gravel':22,'soil':27,'curb':41,'drain':12}.get(style,23)
        dots=((xx*37+yy*19+seed*7)%period)==0
        a[dots]=np.clip(a[dots]-rng.integers(12,48,(dots.sum(),1)),0,255)
        if style=='asphalt':
            grain=((xx*13+yy*7+seed)%73)<4; a[grain]+=13
        if style=='drain':
            lines=(xx%37<3)|(yy%37<3); a[lines]*=.53
    elif style in ('brick','box'):
        row=72; col=150
        ry=yy%row; stagger=((yy//row)%2)*(col//2); rx=(xx+stagger)%col
        mortar=(ry<5)|(rx<6)
        a[mortar]*=.48
        grain=((xx*13+yy*17+seed)%101)<6; a[grain]*=.82
    elif style in ('glass','bottleglass','bottle'):
        panel=((xx%256)<6)|((yy%256)<6)
        a[panel]*=.67
        gloss=((xx+yy*2+seed)%211)<4; a[gloss]=np.clip(a[gloss]+36,0,255)
        streak=(np.sin(xf*34+seed)*.5+.5)>.94; a[streak]*=1.08
    elif style in ('roof','pavers','ceramic','roadmark','container'):
        px=xx%128; py=yy%96
        seam=(px<4)|(py<4)|((yy//96)%2==1)&(px>62)&(px<68)
        a[seam]*=.50
        if style=='roadmark':
            stripe=((xx%256)<36); a[stripe]=np.clip(a[stripe]+43,0,255)
    elif style in ('stucco','paint','paintedmetal'):
        scratch=((xx*11+yy*23+seed)%173)<2; a[scratch]*=.71
        speckle=((xx*7+yy*3+seed)%89)<3; a[speckle]=np.clip(a[speckle]-15,0,255)
    elif style in ('wood','cardboard','weave','fabric','rubber','reflective'):
        if style=='wood': stripe=np.sin(yy*.08+np.sin(xx*.006)*4)+.38*np.sin(yy*.21); a+=stripe[:,:,None]*10
        elif style=='cardboard':
            stripe=np.sin(yy*.24)+.3*np.sin(yy*.72); a+=stripe[:,:,None]*8
            seam=(yy%128)<2; a[seam]*=.65
        elif style in ('weave','fabric'):
            weave=((xx%12)<2)|((yy%12)<2); a[weave]*=.80
            checker=((xx//12+yy//12)%2)==0; a[checker]*=1.035
        elif style=='rubber':
            grooves=(xx%32<3)&(yy%32<16); a[grooves]*=.72
        else:
            band=((yy%96)<23); a[band]=np.clip(a[band]+15,0,255)
    elif style in ('metal','aluminum'):
        stripe=np.sin(xx*.55)*7+np.sin(xx*1.6)*2; a+=stripe[:,:,None]
        scratches=((xx*19+yy*29+seed)%229)<2; a[scratches]=np.clip(a[scratches]+30,0,255)
    elif style=='water':
        wave=np.sin(yy*.055+np.sin(xx*.009)*4)+np.sin(yy*.12+xx*.018); a+=wave[:,:,None]*12
        glint=(np.sin(xx*.19+yy*.07)>0.985); a[glint]=np.clip(a[glint]+28,0,255)
    elif style=='circuit':
        trace=((xx%128)<4)|((yy%128)<4); a[trace,1]=np.clip(a[trace,1]+36,0,255);a[trace,0]=np.clip(a[trace,0]+13,0,255)
        pads=((xx%128>22)&(xx%128<45)&(yy%128>20)&(yy%128<42));a[pads]=np.clip(a[pads]+38,0,255)
    elif style in ('paper',):
        fiber=((xx*23+yy*41+seed)%167)<2;a[fiber]*=.88
    elif style in ('plastic','wrapper','mixed','flakes','pellets'):
        scratch=((xx*29+yy*13+seed)%191)<2;a[scratch]=np.clip(a[scratch]+24,0,255)
        fleck=((xx*11+yy*17+seed)%61)<4;a[fleck]=np.clip(a[fleck]+rng.integers(-18,22,(fleck.sum(),1)),0,255)
    elif style=='bottle':
        streak=(xx%180)<2;a[streak]=np.clip(a[streak]+20,0,255)
    # High-detail but restrained unique pixel grain; preserves material appearance while adding micro-detail.
    a=seamless(a,20)
    return Image.fromarray(a,'RGB')

for page,items in PAGES.items():
    print('Generating atlas',page,flush=True)
    atlas=Image.new('RGB',(4096,4096))
    for i,(name,base,style) in enumerate(items):
        t0=time.time();tile=make_tile(base,style,1000+sum(map(ord,page))+i*37)
        x=(i%4)*S;y=(i//4)*S
        atlas.paste(tile,(x,y))
        print(f'  {i+1:02}/16 {name}: {time.time()-t0:.1f}s',flush=True)
    hi=ROOT/f'{page}-atlas-4096.png'
    atlas.save(hi,format='PNG',compress_level=1,optimize=False)
    print('  saved',hi.stat().st_size/1024/1024,'MiB',flush=True)
    med=atlas.resize((2048,2048),Image.Resampling.LANCZOS)
    med.save(ROOT/f'{page}-atlas-2048.png',format='PNG',compress_level=1,optimize=False)
    low=atlas.resize((1024,1024),Image.Resampling.LANCZOS)
    low.save(ROOT/f'{page}-atlas-1024.png',format='PNG',compress_level=1,optimize=False)
    print('  medium/low sizes', (ROOT/f'{page}-atlas-2048.png').stat().st_size/1024/1024, (ROOT/f'{page}-atlas-1024.png').stat().st_size/1024/1024, 'MiB',flush=True)
print('Done; total atlas size',sum(p.stat().st_size for p in ROOT.glob('*.png'))/1024/1024,'MiB')
