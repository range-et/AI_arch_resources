"""Reproduce both layouts and compare them with reports saved from Grasshopper."""
from pathlib import Path
import json
import numpy as np
from lbm_solver import solve
root=Path(__file__).resolve().parent
results={}; fields=[]
for suffix,shift in [('a',0),('b',-12)]:
    solid=np.zeros((160,64),bool)
    for x,y,w,h in [(40,16,12,14),(75,40+shift,12,14),(110,12,12,12)]:
        solid[x:x+w,y:y+h]=True
    ux,uy,rho,report=solve(solid)
    actual=json.loads((root/f'05-lbm-layout-{suffix}.json').read_text())
    assert report['finite'] and report['positive_density']
    assert np.allclose(report['max_speed'],actual['max_speed'],rtol=1e-10)
    assert actual['mesh_faces']==10240 and actual['footprint_count']==3
    fields.append(np.hypot(ux,uy))
    results[suffix]={'shift':shift,'peak_speed':report['max_speed'],'matches_Grasshopper':True}
assert not np.allclose(*fields)
results['maximum_field_change']=float(np.max(np.abs(fields[1]-fields[0])))
results['scope']='Reproduction and input response checks. Physical accuracy and grid convergence were not assessed.'
(root/'05-lbm-checks.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
