"""Grasshopper Python 3. Inputs: floors, twist, storey_height.
Outputs: slabs, core, report. Dimensions are metres; twist is degrees.
Prompt: Make a tower with square floor plates. Add controls for floor count,
height per floor and total twist. Keep the slabs and core as closed solids.
"""
import math
import json
import Rhino.Geometry as rg
floors=int(floors)
twist=float(twist)
storey_height=float(storey_height)
if not 2<=floors<=30 or not 0<=twist<=90 or not 2.5<=storey_height<=5:
    raise ValueError('Use 2..30 floors, 0..90 degrees, and 2.5..5 m per floor')
slabs=[]
for i in range(floors):
    z=i*storey_height
    curve=rg.Rectangle3d(rg.Plane(rg.Point3d(0,0,z),rg.Vector3d.ZAxis),rg.Interval(-6,6),rg.Interval(-6,6)).ToNurbsCurve()
    curve.Transform(rg.Transform.Rotation(math.radians(twist)*i/(floors-1),rg.Vector3d.ZAxis,rg.Point3d(0,0,z)))
    slabs.append(rg.Extrusion.Create(curve,.25,True).ToBrep())
height=(floors-1)*storey_height+.25
core=rg.BoundingBox(-2,-2,0,2,2,height).ToBrep()
assert all(b.IsValid and b.IsSolid for b in slabs+[core])
report=json.dumps({'floors':floors,'total_twist_degrees':twist,'storey_height_m':storey_height,'overall_height_m':height,'slab_width_m':12,'valid_closed_slabs':len(slabs),'valid_closed_core':True,'scope':'Parametric geometry study; structure and circulation are not designed.'},indent=2)
ghenv.Component.Message='%d floors / %.0f deg'%(floors,twist)
