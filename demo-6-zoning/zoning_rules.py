"""Selected Toronto RD rules for a fictional lot. Pure calculation shared by GH and checks."""
import json
from pathlib import Path

def calculate(width,depth,config=None):
    if config is None:
        config=json.loads(Path(__file__).with_name('toronto-lot.json').read_text())
    width,depth=float(width),float(depth)
    r=config['rules'];a=config['assumptions']
    front=r['front_setback']['value'];side=r['side_setback']['value']
    rear=max(7.5,.25*depth)
    minimum_frontage=15.;minimum_area=minimum_frontage*30.
    if width<minimum_frontage or width*depth<minimum_area:
        raise ValueError('The fictional f15 lot needs width >=15 m and area >=450 m2')
    build_width=width-2*side
    length_cap=min(depth-front-rear,r['building_length']['value'])
    if length_cap<=0: raise ValueError('No positive depth remains after setbacks')
    area=width*depth;storeys=a['storeys']
    # Leave a 0.1 m inset so the opaque house and translucent envelope do not share faces.
    house_width=build_width-.2
    house_front=front+.1
    house_side=side+.1
    footprint=min(house_width*(length_cap-.2),area*r['coverage']['value'],area*r['floor_space_index']['value']/storeys)
    length=footprint/house_width
    height=storeys*a['floor_to_floor']
    max_height=min(r['overall_height']['value'],r['flat_roof_main_wall_height']['value'])
    if height>max_height:raise ValueError('Assumed storeys exceed selected height limits')
    return {'lot_width_m':width,'lot_depth_m':depth,'lot_area_m2':area,'minimum_lot_area_m2':minimum_area,
            'front_setback_m':front,'rear_setback_m':rear,'side_setback_m':side,
            'buildable_width_m':build_width,'geometric_length_cap_m':length_cap,'flat_roof_height_cap_m':max_height,
            'coverage_cap_m2':area*r['coverage']['value'],'floor_area_cap_m2':area*r['floor_space_index']['value'],
            'example_front_setback_m':house_front,'example_side_setback_m':house_side,'example_width_m':house_width,'example_footprint_m2':footprint,'example_length_m':length,'example_height_m':height,
            'example_floor_area_m2':footprint*storeys,'checks_passed':{'frontage':width>=minimum_frontage,'lot_area':area>=minimum_area,'setbacks':house_front+length<=depth-rear and house_side>=side,'length':length<=r['building_length']['value'],'height':height<=max_height,'coverage':footprint<=area*r['coverage']['value']+1e-9,'floor_area':footprint*storeys<=area*r['floor_space_index']['value']+1e-9},
            'scope':'Selected zoning rules for an assumed RD(f15)(d0.6) lot. Coverage 35% is assumed. Full zoning and Building Code compliance are outside this example.'}
