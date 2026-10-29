"""PROMPT: Build Habitat 67.
Interpretation: a small massing study of stepped modules, made from raw mesh coordinates.
This is an approximation. Module dimensions and arrangement below are assumptions.
Reference for comparison: https://www.safdiearchitects.com/projects/habitat-67
"""
import Rhino
import System.Drawing as sd
import json
import sys
from pathlib import Path
doc=globals().get('__rhino_doc__') or Rhino.RhinoDoc.ActiveDoc
root=Path('/Users/r2d2/Desktop/AI_arch_resources/demo-3-habitat')
if str(root) not in sys.path:sys.path.insert(0,str(root))
sys.path.insert(0,str(root.parent/'tools'))
from demo_view import label,frame
mesh=Rhino.Geometry.Mesh()
count=0
for cluster in range(3):
    for level in range(6):
        for bay in range(6-level):
            for row in range(2):
                x=cluster*86+(bay+level*.5)*12.1
                y=row*5.7+(level%2)*2.7
                z=level*3.4
                # Eight explicit coordinates and six quad faces for each assumed box.
                v=mesh.Vertices.Count
                for dx,dy,dz in [(0,0,0),(11.7,0,0),(11.7,5.3,0),(0,5.3,0),(0,0,3),(11.7,0,3),(11.7,5.3,3),(0,5.3,3)]:
                    mesh.Vertices.Add(x+dx,y+dy,z+dz)
                for f in [(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]:
                    mesh.Faces.AddFace(*[v+i for i in f])
                count+=1
mesh.Normals.ComputeNormals();mesh.Compact()
assert mesh.IsValid and mesh.IsClosed
li=doc.Layers.FindByFullPath('03 Habitat massing',-1)
if li<0:li=doc.Layers.Add('03 Habitat massing',sd.Color.FromArgb(210,202,185))
for o in doc.Objects.FindByLayer('03 Habitat massing'):doc.Objects.Delete(o,True)
a=Rhino.DocObjects.ObjectAttributes();a.LayerIndex=li;a.Name='Approximate stepped massing - assumed module layout'
doc.Objects.AddMesh(mesh,a)
report={'prompt':'Build Habitat 67','interpretation':'Approximate stepped massing using assumed module dimensions and layout','modules':count,'mesh_vertices':mesh.Vertices.Count,'quad_faces':mesh.Faces.Count,'valid_mesh':bool(mesh.IsValid),'closed_mesh':bool(mesh.IsClosed),'fidelity_checked':False,'scope':'No reconstruction of original plans, circulation, structure or dwelling layouts. Geometric validity does not establish architectural accuracy.','reference':'https://www.safdiearchitects.com/projects/habitat-67'}
(root/'03-habitat-checks.json').write_text(json.dumps(report,indent=2))
label(doc,'PROMPT: Build Habitat 67','INTERPRETATION: Approximate stepped massing | 126 assumed modules','CHECK: Valid closed mesh. Original plans and building systems are not reconstructed.')
frame(doc,mesh.GetBoundingBox(True),'Perspective')
print(json.dumps(report,indent=2))

# Save only this demo geometry, including when other models are open.
f=Rhino.FileIO.File3dm()
f.Settings.ModelUnitSystem=Rhino.UnitSystem.Meters
f.Objects.AddMesh(mesh,a)
assert f.Write(str(root/'03-habitat-massing.3dm'),8)
