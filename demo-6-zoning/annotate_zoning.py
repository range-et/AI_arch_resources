"""Annotate the baked zoning solution. Run after tools/export_gh_result.cs in Rhino.
Blue volume: selected geometric limits. Orange solid: example house.
Creates a separate annotated model and keeps the three-object geometry exports intact.
"""
import json,sys
from pathlib import Path
import Rhino
import Grasshopper
import System.Drawing as sd
root=Path('/Users/r2d2/Desktop/AI_arch_resources/demo-6-zoning')
sys.path.insert(0,str(root.parent/'tools'))
from demo_view import label,frame
doc=globals().get('__rhino_doc__') or Rhino.RhinoDoc.ActiveDoc
gh=Grasshopper.Instances.ActiveCanvas.Document
c=next(o for o in gh.Objects if o.Name=='Toronto RD envelope')
data=json.loads(next(iter(c.Params.Output[4].VolatileData.AllData(True))).ToString())
w,d=data['lot_width_m'],data['lot_depth_m'];front=data['front_setback_m'];rear=data['rear_setback_m'];side=data['side_setback_m'];length=data['geometric_length_cap_m'];height=data['flat_roof_height_cap_m']
for o in list(doc.Objects):
    if o.Attributes.Name.startswith('Constraint:'):doc.Objects.Delete(o,True)
colour=sd.Color.FromArgb(35,64,85)
def attr(name):
    a=Rhino.DocObjects.ObjectAttributes();a.Name='Constraint: '+name;a.ObjectColor=colour;a.ColorSource=Rhino.DocObjects.ObjectColorSource.ColorFromObject;return a
def line(a,b,name):doc.Objects.AddLine(Rhino.Geometry.Point3d(*a),Rhino.Geometry.Point3d(*b),attr(name))
def dot(text,p):
    t=Rhino.Geometry.TextDot(text,Rhino.Geometry.Point3d(*p));t.FontHeight=16;doc.Objects.AddTextDot(t,attr(text))
def measure(a,b,text,p):line(a,b,text);dot(text,p)
# Show the selected yard boundaries independently of the house footprint.
line((0,front,.04),(w,front,.04),'front yard limit')
line((0,d-rear,.04),(w,d-rear,.04),'rear yard limit')
line((side,0,.04),(side,d,.04),'left side yard limit')
line((w-side,0,.04),(w-side,d,.04),'right side yard limit')
measure((-3,0,0),(-3,front,0),'Front %.1f m'%front,(-3,front/2,0))
measure((-3,d-rear,0),(-3,d,0),'Rear %.1f m'%rear,(-3,d-rear/2,0))
measure((w-side,2,0),(w,2,0),'Side %.1f m'%side,(w+3,2,0))
measure((w+3,front,0),(w+3,front+length,0),'Length cap %.1f m'%length,(w+3,front+length/2,0))
measure((w+2,front+length,0),(w+2,front+length,height),'Wall cap %.1f m'%height,(w+2,front+length,height+1))
dot('LOT %.0f x %.0f m'%(w,d),(w/2,-3,0))
dot('Example: %.0f m2 on two floors'%data['example_floor_area_m2'],(w/2,front+data['example_length_m']/2,7))
# A floor division helps students read the orange solid as two storeys.
front=data['example_front_setback_m'];side=data['example_side_setback_m']
house_end=front+data['example_length_m']
for a,b in [((side,front,3),(w-side,front,3)),((w-side,front,3),(w-side,house_end,3)),((w-side,house_end,3),(side,house_end,3)),((side,house_end,3),(side,front,3))]:line(a,b,'first floor')
label(doc,'Toronto RD. Fictional %.0f x %.0f m lot'%(w,d),'Translucent blue: selected limits. Solid orange: example house.','Rear %.1f m. Floor area %.0f m2. Coverage 35%% and FSI 0.6 assumed.'%(rear,data['example_floor_area_m2']))
frame(doc,Rhino.Geometry.BoundingBox(Rhino.Geometry.Point3d(-8,-6,0),Rhino.Geometry.Point3d(w+8,d+5,11)),'Perspective')
f=Rhino.FileIO.File3dm();f.Settings.ModelUnitSystem=Rhino.UnitSystem.Meters
for m in doc.Materials:f.Materials.Add(m)
for o in doc.Objects:
    if not o.IsHidden:f.Objects.Add(o.Geometry,o.Attributes)
suffix='a' if d==36 else 'b'
assert f.Write(str(root/('20-toronto-annotated-'+suffix+'.3dm')),8)
doc.Views.Redraw()
print('Annotated zoning model '+suffix+' saved. Envelope material transparency: 82%.')
