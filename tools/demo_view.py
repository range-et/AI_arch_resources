"""Rhino viewport framing and readable on-screen labels for the OBS demos."""
import Rhino
import scriptcontext as sc
from System.Drawing import Color

class DemoLabel(Rhino.Display.DisplayConduit):
    def __init__(self,lines):
        super(DemoLabel,self).__init__()
        self.lines=lines
    def DrawForeground(self,e):
        for i,line in enumerate(self.lines):
            e.Display.Draw2dText(line,Color.FromArgb(18,30,44),Rhino.Geometry.Point2d(24,70+i*27),False,20)

def label(doc,*lines):
    old=sc.sticky.get('architecture_presentation_label')
    if old:old.Enabled=False
    hud=DemoLabel(lines);hud.Enabled=True
    sc.sticky['architecture_presentation_label']=hud
    doc.Views.Redraw()

def frame(doc,bounds,view='Perspective'):
    v=doc.Views.ActiveView.ActiveViewport
    projection=getattr(Rhino.Display.DefinedViewportProjection,view)
    v.SetProjection(projection,view,True)
    v.ConstructionGridVisible=False;v.ConstructionAxesVisible=False
    v.ZoomBoundingBox(bounds)
    doc.Views.Redraw()
