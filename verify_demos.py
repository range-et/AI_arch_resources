"""Check saved demo geometry and the shared zoning calculation.
Run with Python, rhino3dm and NumPy installed. See check_lbm.py for solver checks.
"""
from pathlib import Path
import json,subprocess,zipfile,xml.etree.ElementTree as ET
import rhino3dm as r
from zoning_rules import calculate
ROOT=Path(__file__).resolve().parent
checks={}
for name,count in [('01-install-check.3dm',1),('02-command-selection.3dm',2),('03-habitat-massing.3dm',1),('04-tower-a.3dm',13),('04-tower-b.3dm',13),('20-toronto-lot-a.3dm',3),('20-toronto-lot-b.3dm',3)]:
    f=r.File3dm.Read(str(ROOT/name));assert f and len(f.Objects)==count,(name,len(f.Objects))
    for o in f.Objects:
        assert o.Geometry.IsValid,name
        if isinstance(o.Geometry,r.Brep):assert o.Geometry.IsSolid,name
        if isinstance(o.Geometry,r.Mesh):assert o.Geometry.IsClosed,name
    checks[name]={'objects':len(f.Objects),'all_valid':True,'breps_closed':True}
a,b=calculate(15,36),calculate(15,30)
assert (a['rear_setback_m'],b['rear_setback_m'])==(9,7.5)
assert (a['example_floor_area_m2'],b['example_floor_area_m2'])==(324,270)
for depth,result in [(36,a),(30,b)]:
    assert all(result['checks_passed'].values())
    stored=json.loads((ROOT/f"20-toronto-lot-{'a' if depth==36 else 'b'}.json").read_text())
    assert result==stored
for w,d in [(14,36),(15,29)]:
    try:calculate(w,d)
    except ValueError:pass
    else:raise AssertionError('Invalid fictional lot accepted')
checks['zoning']={'A_reproduced':True,'B_reproduced':True,'invalid_lots_rejected':True}
z=zipfile.ZipFile(ROOT/'AI in Architecture - Presentation.pptx');ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
slides=[n for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')];assert len(slides)==30
for i,needle in [(16,'Radial Profile'),(17,'Generated Mesh Checks'),(18,'12 closed slabs'),(19,'Adapt existing LBM code'),(20,'Toronto RD Zoning Rules'),(21,'Published Demo')]:
    text=' '.join(t.text or '' for t in ET.fromstring(z.read(f'ppt/slides/slide{i}.xml')).findall('.//a:t',ns));assert needle in text,(i,needle)
    notes=' '.join(t.text or '' for t in ET.fromstring(z.read(f'ppt/notesSlides/notesSlide{i}.xml')).findall('.//a:t',ns));assert '.mp4' in notes,i
checks['presentation']={'slides':30,'demo_labels_and_notes_present':True}
for p in sorted(ROOT.glob('*.mp4')):
    data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height','-of','json',str(p)],text=True));s=data['streams'][0]
    assert (s['codec_name'],s['width'],s['height'])==('h264',1920,1080),p
    assert float(data['format']['duration'])>10
    checks[p.name]={'duration_seconds':round(float(data['format']['duration']),2),'codec':'h264','dimensions':'1920x1080'}
(ROOT/'demo-checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2))
