"""Grasshopper Python 3. Inputs: lot_width, lot_depth. Outputs: lot, envelope, house, report.
Prompt: Read the selected Toronto RD rules. Build a lot, the geometric limits,
and a two-storey house capped by setbacks, height, coverage and FSI. Add a lot-depth slider.
"""
import os
import sys
import json
import Rhino.Geometry as rg
folder=os.path.dirname(ghenv.Component.OnPingDocument().FilePath)
if folder not in sys.path:sys.path.insert(0,folder)
if 'zoning_rules' in sys.modules and os.path.dirname(sys.modules['zoning_rules'].__file__)!=folder:
    del sys.modules['zoning_rules']
import importlib
import zoning_rules
importlib.reload(zoning_rules)
from zoning_rules import calculate
c=calculate(lot_width,lot_depth)
w,d=c['lot_width_m'],c['lot_depth_m']
s,f=c['side_setback_m'],c['front_setback_m']
lot=rg.PolylineCurve([rg.Point3d(x,y,0) for x,y in [(0,0),(w,0),(w,d),(0,d),(0,0)]])
envelope=rg.BoundingBox(s,f,0,w-s,f+c['geometric_length_cap_m'],c['flat_roof_height_cap_m']).ToBrep()
hs,hf=c['example_side_setback_m'],c['example_front_setback_m']
house=rg.BoundingBox(hs,hf,0,w-hs,hf+c['example_length_m'],c['example_height_m']).ToBrep()
assert envelope.IsValid and envelope.IsSolid and house.IsValid and house.IsSolid
report=json.dumps(c,indent=2)
ghenv.Component.Message='Lot depth %.1f m / rear %.1f m'%(d,c['rear_setback_m'])
