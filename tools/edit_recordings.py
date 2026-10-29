"""Edit real OBS recordings using recordings.json. Requires ffmpeg and Pillow.
Run python edit_recordings.py. Original MOV files belong in working/recordings.
If absent there, the script copies them from ~/Movies. No UI is reconstructed.
"""
from pathlib import Path
import json,subprocess,shutil,sys
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent.parent
WORK=ROOT/'working'/'recordings';WORK.mkdir(exist_ok=True,parents=True)
manifest=json.loads((ROOT/'tools'/'recordings.json').read_text())
fontpath='/System/Library/Fonts/Supplemental/Arial.ttf'
font=ImageFont.truetype(fontpath,28) if Path(fontpath).exists() else ImageFont.truetype('DejaVuSans.ttf',28)
for video in manifest['videos']:
    if len(sys.argv)>1 and sys.argv[1] not in video['output']:continue
    cuts=[]
    for i,(name,start,duration,speed,title) in enumerate(video['segments']):
        src=WORK/name
        if not src.exists():shutil.copy2(Path.home()/'Movies'/name,src)
        stem=Path(video['output']).stem
        cap=Image.new('RGB',(1920,74),'#162029');ImageDraw.Draw(cap).text((26,20),title,font=font,fill='white')
        label=WORK/f'{stem}-{i}.png';cap.save(label)
        cut=WORK/f'{stem}-{i}.mp4';cuts.append(cut)
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(start),'-t',str(duration),'-i',str(src),'-i',str(label),'-filter_complex',f'[0:v]setpts=PTS/{speed},fps=30,scale=1920:1080[v];[v][1:v]overlay=0:0[out]','-map','[out]','-an','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',str(cut)],check=True)
    concat=WORK/f'{stem}-concat.txt';concat.write_text(''.join(f"file '{p}'\n" for p in cuts))
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(ROOT/video['output'])],check=True)
    print(video['output'],flush=True)
