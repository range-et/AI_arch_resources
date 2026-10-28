"""Grasshopper Python 3 component. Input: shift. Outputs: footprints, buildings."""
import Rhino.Geometry as rg
footprints=[]
buildings=[]
for x,y,w,h in [(40,16,12,14),(75,40+float(shift),12,14),(110,12,12,12)]:
    rectangle=rg.Rectangle3d(rg.Plane.WorldXY,rg.Interval(x,x+w),rg.Interval(y,y+h))
    curve=rectangle.ToNurbsCurve()
    footprints.append(curve)
    buildings.append(rg.Extrusion.Create(curve,6,True).ToBrep())
ghenv.Component.Message='Middle footprint shift: %.1f'%float(shift)
