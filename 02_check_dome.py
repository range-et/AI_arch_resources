"""Run after native Revolve and Cap. Inspect and save the actual result."""
import Rhino
import json
import sys
from pathlib import Path
doc=globals().get('__rhino_doc__') or Rhino.RhinoDoc.ActiveDoc
root=Path('/Users/r2d2/Desktop/AI_arch_resources')
if str(root) not in sys.path:sys.path.insert(0,str(root))
from demo_view import label,frame
breps=[o for o in doc.Objects if isinstance(o.Geometry,Rhino.Geometry.Brep)]
assert len(breps)==1
b=breps[0].Geometry
assert b.IsValid and b.IsSolid
for o in doc.Objects:
    if isinstance(o.Geometry,Rhino.Geometry.Curve):doc.Objects.Hide(o.Id,True)
doc.Objects.UnselectAll()
checks={'command_sequence':['Revolve','Cap','Check'],'valid':bool(b.IsValid),'closed_solid':bool(b.IsSolid),'face_count':b.Faces.Count,'volume_m3':Rhino.Geometry.VolumeMassProperties.Compute(b).Volume}
(root/'02-command-checks.json').write_text(json.dumps(checks,indent=2))
label(doc,'RESULT: One valid closed dome','Native Revolve > native Cap > geometry check','Faces: %d | Volume: %.2f m3'%(b.Faces.Count,checks['volume_m3']))
frame(doc,b.GetBoundingBox(True),'Perspective')
print(json.dumps(checks,indent=2))
