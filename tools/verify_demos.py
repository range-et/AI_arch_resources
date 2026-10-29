"""Check saved demo geometry and the shared zoning calculation.
Run with Python, rhino3dm and NumPy installed. See check_lbm.py for solver checks.
"""
from pathlib import Path
import json,subprocess,zipfile,xml.etree.ElementTree as ET
import rhino3dm as r
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'demo-6-zoning'))
from zoning_rules import calculate
ROOT=Path(__file__).resolve().parent.parent
checks={}
for name,count in [('demo-1-install/01-install-check.3dm',1),('demo-2-commands/02-command-selection.3dm',2),('demo-3-habitat/03-habitat-massing.3dm',1),('demo-4-tower/04-tower-a.3dm',13),('demo-4-tower/04-tower-b.3dm',13),('demo-6-zoning/20-toronto-lot-a.3dm',3),('demo-6-zoning/20-toronto-lot-b.3dm',3)]:
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
    stored=json.loads((ROOT/'demo-6-zoning'/f"20-toronto-lot-{'a' if depth==36 else 'b'}.json").read_text())
    assert result==stored
for w,d in [(14,36),(15,29)]:
    try:calculate(w,d)
    except ValueError:pass
    else:raise AssertionError('Invalid fictional lot accepted')
checks['zoning']={'A_reproduced':True,'B_reproduced':True,'invalid_lots_rejected':True}
z=zipfile.ZipFile(ROOT/'AI in Architecture - Presentation.pptx');ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
slides=[n for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')];assert len(slides)==37
for i,needle in [(17,'Radial Profile'),(19,'Generated Mesh Checks'),(21,'12 closed slabs'),(23,'Adapt existing LBM code'),(25,'Toronto RD Zoning Rules'),(27,'Published Demo')]:
    text=' '.join(t.text or '' for t in ET.fromstring(z.read(f'ppt/slides/slide{i}.xml')).findall('.//a:t',ns));assert needle in text,(i,needle)
    notes=' '.join(t.text or '' for t in ET.fromstring(z.read(f'ppt/notesSlides/notesSlide{i}.xml')).findall('.//a:t',ns));assert '.mp4' in notes,i
pns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
expected={16:'01-rhino-mcp-install.mp4',18:'02-command-selection.mp4',20:'03-habitat-prompt.mp4',22:'04-parametric-tower.mp4',24:'05-lbm-to-grasshopper.mp4',26:'20-toronto-zoning.mp4',28:'21-autodesk-published-demo.mp4'}
for i,name in expected.items():
    slide=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
    assert name in [t.get('title') for t in slide.findall('.//p:cNvPr',pns)]
checks['presentation']={'slides':37,'demo_labels_and_notes_present':True,'seven_video_slides_in_order':True,'export_media':'Drive-linked posters. Google Slides contains native playable videos.'}
for suffix in ['a','b']:
    f=r.File3dm.Read(str(ROOT/'demo-6-zoning'/f'20-toronto-annotated-{suffix}.3dm'))
    envelope=next(o for o in f.Objects if o.Attributes.Name=='envelope')
    assert abs(f.Materials[envelope.Attributes.MaterialIndex].Transparency-.82)<1e-8
    labels=[o.Geometry.Text for o in f.Objects if isinstance(o.Geometry,r.TextDot)]
    assert len(labels)==7
    assert any(('9.0 m' if suffix=='a' else '7.5 m') in t for t in labels)
    assert any('Front 6.0 m' in t for t in labels)
checks['zoning_display']={'envelope_transparency':.82,'labels_per_case':7,'annotated_models_checked':True}
for p in sorted(ROOT.glob('demo-*/*.mp4')):
    data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height','-of','json',str(p)],text=True));s=data['streams'][0]
    assert (s['codec_name'],s['width'],s['height'])==('h264',1920,1080),p
    assert float(data['format']['duration'])>10
    checks[p.name]={'duration_seconds':round(float(data['format']['duration']),2),'codec':'h264','dimensions':'1920x1080'}
(ROOT/'tools/demo-checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2))
