"""Create a Rhino teaching model from the declared fictional Toronto lot."""
import json
from pathlib import Path
import rhino3dm as r

HERE = Path(__file__).resolve().parent
p = json.loads((HERE/'toronto-lot.json').read_text())
rules = p['rules']
def v(k): return rules[k]['value']
width, depth = p['lot_width'], p['lot_depth']
lot_area = width*depth
build_width = width-2*v('side_setback')
setback_depth = depth-v('front_setback')-v('rear_setback')
base_length = min(setback_depth, v('building_length'))
# Assume equal rectangular floor plates with no floor-area exclusions.
footprint = min(build_width*base_length, lot_area*v('coverage'),
                lot_area*v('floor_space_index')/p['assumptions']['storeys'])
length = footprint/build_width
height = p['assumptions']['storeys']*p['assumptions']['floor_to_floor']
assert height <= min(v('overall_height'), v('flat_roof_main_wall_height'))
model = r.File3dm()
model.Settings.ModelUnitSystem = r.UnitSystem.Meters

def layer(name, colour):
    l = r.Layer(); l.Name=name; l.Color=colour
    return model.Layers.Add(l)

def attr(name, index):
    a=r.ObjectAttributes();a.Name=name;a.LayerIndex=index
    return a

def box(name, index, x0,y0,z0,x1,y1,z1):
    b=r.BoundingBox(r.Point3d(x0,y0,z0),r.Point3d(x1,y1,z1))
    return model.Objects.AddBrep(r.Brep.CreateFromBox(r.Box(b)),attr(name,index))

lot_layer=layer('Lot', (65,65,65,255))
limit_layer=layer('Selected geometric limits', (60,100,220,255))
house_layer=layer('Example house', (215,100,55,255))
pts=[r.Point3d(x,y,0) for x,y in [(0,0),(width,0),(width,depth),(0,depth),(0,0)]]
model.Objects.AddPolyline(pts,attr('15 x 36 metre fictional lot',lot_layer))
x0,y0=v('side_setback'),v('front_setback')
box('Geometric limits before coverage and FSI',limit_layer,
    x0,y0,0,width-x0,y0+base_length,v('flat_roof_main_wall_height'))
box('Example two storey house',house_layer,x0,y0,0,width-x0,y0+length,height)
path=HERE/'20-toronto-lot.3dm'
assert model.Write(str(path),8)
readback=r.File3dm.Read(str(path))
assert len(readback.Objects)==3
report={'lot_area_m2':lot_area,'buildable_width_m':build_width,
        'setback_depth_m':setback_depth,'length_cap_m':base_length,
        'coverage_cap_m2':lot_area*v('coverage'),
        'gross_floor_area_cap_m2':lot_area*v('floor_space_index'),
        'example_footprint_m2':footprint,'example_length_m':length,
        'example_height_m':height,'example_floor_area_m2':footprint*p['assumptions']['storeys'],
        'objects_after_readback':len(readback.Objects),
        'scope':'Selected rules only. No parcel-specific approval or full compliance check.'}
(HERE/'20-zoning-calculation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
