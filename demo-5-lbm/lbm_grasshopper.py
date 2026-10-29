# r: numpy
"""Grasshopper Python 3 component. Inputs: footprints, steps, inlet, tau.
Outputs: mesh, vectors, report. Keep lbm_core.py and lbm_solver.py beside the GH file.
Source: jviquerat/lbm, commit 64023fc76db2ddb681b2d4d24306a433e85f9555.
"""
import os
import sys
import json
import time
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
from System.Drawing import Color
import numpy as np

folder=os.path.dirname(ghenv.Component.OnPingDocument().FilePath)
if not folder:
    raise ValueError('Save the GH definition beside lbm_solver.py first')
if folder not in sys.path:
    sys.path.insert(0,folder)
from lbm_solver import solve

started=time.time()
nx,ny=160,64
solid=np.zeros((nx,ny),dtype=bool)
curves=[]
for curve in footprints or []:
    if hasattr(curve,'Value'):
        curve=curve.Value
    if not hasattr(curve,'IsClosed'):
        curve=rs.coercecurve(curve)
    if curve is None:
        raise ValueError('A footprint could not be read as a curve')
    if not curve.IsClosed or not curve.IsPlanar():
        raise ValueError('Each footprint must be a closed planar curve')
    bb=curve.GetBoundingBox(True)
    if abs(bb.Min.Z)>0.001 or abs(bb.Max.Z)>0.001:
        raise ValueError('Place footprint curves on the World XY plane')
    if bb.Min.X<2 or bb.Min.Y<2 or bb.Max.X>nx-2 or bb.Max.Y>ny-2:
        raise ValueError('Keep footprints two cells inside the 160 x 64 domain')
    curves.append(curve)
    for i in range(max(1,int(bb.Min.X)),min(nx-1,int(bb.Max.X)+1)):
        for j in range(max(1,int(bb.Min.Y)),min(ny-1,int(bb.Max.Y)+1)):
            if curve.Contains(rg.Point3d(i+.5,j+.5,0),rg.Plane.WorldXY,.001)!=rg.PointContainment.Outside:
                solid[i,j]=True
ux,uy,rho,checks=solve(solid,int(steps),float(inlet),float(tau))
mesh=rg.Mesh()
vectors=[]
# Shared scale for both layouts. Blue is slow. Yellow is fast.
palette=[(34,30,110),(33,105,166),(29,164,166),(123,207,124),(253,231,37)]
def colour(value):
    value=max(0.,min(1.,value/2.0))*(len(palette)-1)
    k=min(int(value),len(palette)-2);f=value-k
    return Color.FromArgb(*[int(palette[k][a]*(1-f)+palette[k+1][a]*f) for a in range(3)])
for i in range(nx):
    for j in range(ny):
        c=Color.FromArgb(40,40,40) if solid[i,j] else colour(float(np.hypot(ux[i,j],uy[i,j]))/float(inlet))
        v=mesh.Vertices.Count
        for x,y in [(i,j),(i+1,j),(i+1,j+1),(i,j+1)]:
            mesh.Vertices.Add(x,y,0)
            mesh.VertexColors.Add(c)
        mesh.Faces.AddFace(v,v+1,v+2,v+3)
        if i%8==4 and j%8==4 and not solid[i,j]:
            p=rg.Point3d(i+.5,j+.5,.2)
            vectors.append(rg.Line(p,p+rg.Vector3d(float(ux[i,j])/float(inlet)*3,float(uy[i,j])/float(inlet)*3,0)))
mesh.Normals.ComputeNormals();mesh.Compact()
checks['footprint_count']=len(curves)
checks['elapsed_seconds']=round(time.time()-started,3)
checks['mesh_faces']=mesh.Faces.Count
checks['vectors']=len(vectors)
report=json.dumps(checks,indent=2)
ghenv.Component.Message='D2Q9 TRT / %d steps'%int(steps)
print('Flow solved. %d footprint cells, %d mesh faces.'%(int(solid.sum()),mesh.Faces.Count))
