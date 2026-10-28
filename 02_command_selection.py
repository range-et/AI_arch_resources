"""Run in Rhino 8 Script Editor. Create the profile. Then run Revolve and Cap in the Rhino command line.
Prompt: Turn this radial section into a closed dome using Rhino commands.
"""
import Rhino
import System
import System.Drawing as sd
import math
import json
from pathlib import Path
doc=globals().get('__rhino_doc__') or Rhino.RhinoDoc.ActiveDoc
layer='02 Command selection'
li=doc.Layers.FindByFullPath(layer,-1)
if li<0:li=doc.Layers.Add(layer,sd.Color.SteelBlue)
for o in doc.Objects.FindByLayer(layer):doc.Objects.Delete(o,True)
a=Rhino.DocObjects.ObjectAttributes();a.LayerIndex=li;a.Name='Radial profile'
points=[Rhino.Geometry.Point3d(0,0,12),Rhino.Geometry.Point3d(6,0,12),Rhino.Geometry.Point3d(10,0,6),Rhino.Geometry.Point3d(10,0,0)]
curve=Rhino.Geometry.NurbsCurve.Create(False,3,points)
profile_id=doc.Objects.AddCurve(curve,a)
doc.Objects.UnselectAll();doc.Objects.Select(profile_id)
print('PROMPT: Turn a radial profile into a closed dome.')
print('COMMAND CHOICE: Revolve, then Cap. The profile rotates about the Z axis.')
import sys
root=Path('/Users/r2d2/Desktop/AI_arch_resources')
if str(root) not in sys.path:sys.path.insert(0,str(root))
from demo_view import label,frame
label(doc,'PROMPT: Turn this radial section into a closed dome.','CHOSEN COMMANDS: Revolve > Cap > Check','Rotate the profile about the vertical Z axis.')
frame(doc,Rhino.Geometry.BoundingBox(-2,-2,-1,12,2,14),'Front')
