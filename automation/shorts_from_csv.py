import csv, os, subprocess, random
ROOT=os.path.dirname(os.path.dirname(__file__))
DATA=[os.path.join(ROOT,'data','video_scripts_batch1.csv'), os.path.join(ROOT,'data','video_scripts_batch2.csv')]
SLIDES=os.path.join(ROOT,'shorts','slides'); AUDIO=os.path.join(ROOT,'shorts','audio'); OUT=os.path.join(ROOT,'shorts','exports_pending')
os.makedirs(AUDIO, exist_ok=True); os.makedirs(OUT, exist_ok=True)
def has_cmd(c): from shutil import which; return which(c) is not None
def tts(text,out):
    if has_cmd('say'): subprocess.run(['say','-v','Samantha','-r','200',text,'-o',out],check=True)
    else: subprocess.run(['ffmpeg','-f','lavfi','-i','anullsrc=r=44100:cl=mono','-t','1','-q:a','9',out],check=True)
slides=[f for f in os.listdir(SLIDES) if f.lower().endswith(('.png','.jpg','.jpeg'))]
if not slides:
    subprocess.run(['ffmpeg','-f','lavfi','-i','color=c=black:s=1080x1920','-frames:v','1', os.path.join(SLIDES,'bg1.png')], check=True)
    slides=['bg1.png']
def cap(text):
    import textwrap; return "drawtext=text='{}':x=(w-text_w)/2:y=h*0.2:fontsize=48:fontcolor=white:box=1:boxcolor=0x000000AA:boxborderw=12".format("\n".join(textwrap.wrap(text, width=24)))
rows=[]
for p in DATA:
    if os.path.exists(p):
        with open(p,newline='',encoding='utf-8') as f: rows+=list(csv.DictReader(f))
for r in rows:
    vid=r['id']; hook=r['hook']; b=[r['b1'],r['b2'],r['b3']]; cta=r['cta']
    script=f"{hook}. {b[0]}. {b[1]}. {b[2]}. {cta}"
    aud=os.path.join(AUDIO,f"{vid}.aiff"); tts(script,aud)
    bg=os.path.join(SLIDES, random.choice(slides)); out=os.path.join(OUT,f"{vid}.mp4")
    fg="[0:v]scale=1080:1920,format=yuv420p[v0];[v0]{}[v1]".format(cap(hook))
    subprocess.run(['ffmpeg','-loop','1','-t','26','-i',bg,'-i',aud,'-filter_complex',fg,'-map','[v1]','-map','1:a','-shortest','-r','30','-y',out], check=True)
print("Shorts rendered -> shorts/exports_pending/")