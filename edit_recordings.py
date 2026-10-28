"""Cut real OBS footage into a short walkthrough. Keep raw files in working/recordings.
Run: working/venv/bin/python edit_recordings.py
Requires ffmpeg and Pillow. Captions label cuts and playback speed.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
import shutil
ROOT=Path(__file__).resolve().parent
WORK=ROOT/'working'/'recordings'
WORK.mkdir(parents=True,exist_ok=True)
movies=Path.home()/'Movies'
for name in ['2026-10-28 18-30-28.mov','2026-10-28 18-31-49.mov']:
    target=WORK/name
    if not target.exists(): shutil.copy2(movies/name,target)
segments=[
 ('2026-10-28 18-30-28.mov',0,64,2,'1. Read the source: D2Q9 / TRT in jviquerat/lbm (2x)'),
 ('2026-10-28 18-31-49.mov',205,95,2,'2. Build the GH tool, inspect an error, and fix curve input (2x)'),
 ('2026-10-28 18-31-49.mov',630,38,1,'3. Read the connected GH inputs and solver report'),
 ('2026-10-28 18-31-49.mov',668,17,1,'4. Inspect the first flow field in Rhino'),
 ('2026-10-28 18-31-49.mov',747,48,1,'5. Export layout A; change the middle block from 0 to -12'),
 ('2026-10-28 18-31-49.mov',795,39,1,'6. Inspect the Python adapter, changed report, and layout B'),
]
clips=[]
for i,(source,start,duration,speed,title) in enumerate(segments):
    cap=Image.new('RGB',(1920,74),'#162029');d=ImageDraw.Draw(cap)
    font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',30)
    d.text((30,19),title,fill='white',font=font)
    label=WORK/f'caption-{i}.png';cap.save(label)
    clip=WORK/f'cut-{i}.mp4';clips.append(clip)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(start),'-t',str(duration),'-i',str(WORK/source),'-i',str(label),'-filter_complex',f'[0:v]setpts=PTS/{speed},fps=30[v];[v][1:v]overlay=0:0[out]','-map','[out]','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p',str(clip)],check=True)
concat=WORK/'concat.txt';concat.write_text(''.join(f"file '{p}'\n" for p in clips))
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(ROOT/'05-lbm-to-grasshopper.mp4')],check=True)
print(ROOT/'05-lbm-to-grasshopper.mp4')
