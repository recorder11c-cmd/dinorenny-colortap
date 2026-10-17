# api/gallery の作品画像を 320px 正方形のカードにして <出力dir>/img/ に保存し、cards.json を書く
import json,urllib.request,sys,io,os,concurrent.futures
from PIL import Image, ImageOps
S=sys.argv[1] if len(sys.argv)>1 else os.path.dirname(os.path.abspath(__file__)); os.makedirs(S+'/img',exist_ok=True)
g=json.load(urllib.request.urlopen('https://charamarl.com/api/gallery'))['list']
items=[it for it in g if it.get('status')=='approved' and it.get('cat')!='INTERVIEW' and it.get('artist')!='CHARAMARL' and it.get('img')]
def fetch(it):
    try:
        b=urllib.request.urlopen(urllib.request.Request(it['img'],headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read()
        im=ImageOps.exif_transpose(Image.open(io.BytesIO(b)).convert('RGB')); w,h=im.size; s=min(w,h)
        im.crop(((w-s)//2,(h-s)//2,(w-s)//2+s,(h-s)//2+s)).resize((320,320),Image.LANCZOS).save(f"{S}/img/{it['id']}.jpg",quality=88); return it['id']
    except Exception: return None
with concurrent.futures.ThreadPoolExecutor(8) as ex: ids=[i for i in ex.map(fetch,items) if i]
json.dump([{'id':i,'artist':next(x['artist'] for x in items if x['id']==i)} for i in ids],open(f'{S}/cards.json','w'),ensure_ascii=False)
print('cards',len(ids))
