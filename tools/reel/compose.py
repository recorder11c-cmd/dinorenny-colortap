# frames/g_*.jpg を縦1080x1920に組む。使い方: python3 compose.py cfg.json
import sys, json, glob
from PIL import Image, ImageDraw, ImageFont
cfg=json.load(open(sys.argv[1],encoding='utf-8'))
W,H=1080,1920; INK=(27,27,31); FPS=30
F1=ImageFont.truetype('mplus900.ttf', cfg.get('titleSize',94)); F2=ImageFont.truetype('mplus900.ttf', 62); F3=ImageFont.truetype('mplus900.ttf', 48); F4=ImageFont.truetype('mplus700.ttf', 40)
hero=Image.open(cfg['hero']).convert('RGBA')
if cfg.get('flip'): hero=hero.transpose(Image.FLIP_LEFT_RIGHT)
hero=hero.resize((400,400), Image.NEAREST if cfg.get('pixel') else Image.LANCZOS)
c0=tuple(cfg.get('bg0',[255,224,241])); c1=tuple(cfg.get('bg1',[255,110,185])); dot=tuple(cfg.get('dot',[255,180,220]))
def base():
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/H; d.line([(0,y),(W,y)], fill=tuple(int(c0[i]+(c1[i]-c0[i])*t) for i in range(3)))
    for x in range(30,W,72):
        for y in range(30,H,72): d.ellipse([x-4,y-4,x+4,y+4], fill=dot)
    return im,d
def outlined(d,txt,x,y,font,fill,stroke=10,shadow=(6,6)):
    d.text((x+shadow[0],y+shadow[1]), txt, font=font, fill=INK, stroke_width=stroke, stroke_fill=INK); d.text((x,y), txt, font=font, fill=fill, stroke_width=stroke, stroke_fill=INK)
def center(d,txt,y,font,fill,stroke=10,shadow=(6,6)):
    w=d.textlength(txt,font=font); outlined(d,txt,(W-w)/2,y,font,fill,stroke,shadow)
def pill(d,txt,y,font=F2):
    w=d.textlength(txt,font=font)+80; x=(W-w)/2
    d.rounded_rectangle([x,y,x+w,y+font.size+44], 46, fill='white', outline=INK, width=7); d.text((x+40,y+20), txt, font=font, fill=INK)
GW=1040; GX=(W-GW)//2; GY=790
def frame(game_img, caption, sub=None, dim=False):
    im,d=base(); im.paste(hero,(40,200),hero)
    tx=450; outlined(d,cfg['title1'],tx,275,F1,'white',11,(6,6)); outlined(d,cfg['title2'],tx,385,F1,(255,224,0),11,(6,6))
    center(d,cfg['subtitle'],660,F3,'white',7,(4,4))
    g=Image.open(game_img).convert('RGB'); gh=int(g.height*GW/g.width); g=g.resize((GW,gh), Image.LANCZOS)
    d.rounded_rectangle([GX-10,GY-10,GX+GW+10,GY+gh+10], 40, fill=INK)
    mask=Image.new('L',(GW,gh),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,GW,gh],30,fill=255); im.paste(g,(GX,GY),mask)
    if dim:
        ov=Image.new('RGBA',(W,H),(27,27,31,150)); im=Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB'); d=ImageDraw.Draw(im)
    if caption: pill(d,caption,GY+gh+80)
    if sub: center(d,sub,GY+gh+240,F3,'white',7,(4,4))
    center(d,cfg['url'],H-260,F4,'white',6,(3,3)); center(d,'プロフのリンクから走れる',H-190,F4,(255,224,0),6,(3,3))
    return im
games=sorted(glob.glob('frames/g_*.jpg'))
timeline=[(0,3.0,'ログイン不要・タップで走るだけ'),(3.0,5.5,'タップでジャンプ ↓でしゃがむ'),(5.5,7.2,'100点ごとに世界の色がかわる'),(7.2,11,'★を取ると15秒 空を飛べる')]
idx=0
for i in range(int(1.0*FPS)): frame(games[0],'ログイン不要・タップで走るだけ').save(f'out/f_{idx:04d}.jpg',quality=92); idx+=1
for k,gpath in enumerate(games):
    t=k/FPS; cap=next((c for a,b,c in timeline if a<=t<b), timeline[-1][2]); frame(gpath,cap).save(f'out/f_{idx:04d}.jpg',quality=92); idx+=1
for i in range(int(2.5*FPS)): frame(games[-1],'ランキングに名前をのこそう',cfg['endSub'],dim=True).save(f'out/f_{idx:04d}.jpg',quality=92); idx+=1
print('frames',idx,'sec',idx/FPS)
picks=[0,int(4*FPS),int(11*FPS),idx-1]; sheet=Image.new('RGB',(4*270,480),(255,255,255))
for j,p in enumerate(picks): sheet.paste(Image.open(f'out/f_{p:04d}.jpg').resize((270,480)),(j*270,0))
sheet.save('sheet.png')
