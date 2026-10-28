// Run in Rhino MCP after solving 05-lbm-tool.gh. Export the current GH outputs.
var doc=Grasshopper.Instances.ActiveCanvas.Document;
var solver=(Grasshopper.Kernel.GH_Component)doc.Objects.First(o=>o.Name=="LBM flow slice");
var buildings=(Grasshopper.Kernel.GH_Component)doc.Objects.First(o=>o.Name=="Building footprints");
var shift=(Grasshopper.Kernel.Special.GH_NumberSlider)doc.Objects.First(o=>o.NickName=="Middle block shift");
var suffix=shift.CurrentValue==0?"a":"b";
var root=System.IO.Path.GetDirectoryName(doc.FilePath);
var file=new Rhino.FileIO.File3dm();
var layer=new Rhino.DocObjects.Layer();layer.Name="LBM current result";layer.Color=System.Drawing.Color.DimGray;
int li=__rhino_doc__.Layers.FindByFullPath(layer.Name,-1);if(li<0)li=__rhino_doc__.Layers.Add(layer);
foreach(var o in __rhino_doc__.Objects.FindByLayer("LBM current result"))__rhino_doc__.Objects.Delete(o,false);
var a=new Rhino.DocObjects.ObjectAttributes();a.LayerIndex=li;
foreach(var p in new[]{solver.Params.Output[1],solver.Params.Output[2],buildings.Params.Output[2]}){
 foreach(var goo in p.VolatileData.AllData(true)){
  var geometry=goo.ScriptVariable() as Rhino.Geometry.GeometryBase;
  if(geometry==null && goo.ScriptVariable() is Rhino.Geometry.Line line)geometry=new Rhino.Geometry.LineCurve(line);
  if(geometry==null)continue;
  if(geometry is Rhino.Geometry.Mesh m)file.Objects.AddMesh(m,new Rhino.DocObjects.ObjectAttributes());
  else if(geometry is Rhino.Geometry.Curve c)file.Objects.AddCurve(c,new Rhino.DocObjects.ObjectAttributes());
  else if(geometry is Rhino.Geometry.Brep b)file.Objects.AddBrep(b,new Rhino.DocObjects.ObjectAttributes());
  else if(geometry is Rhino.Geometry.Extrusion e)file.Objects.AddBrep(e.ToBrep(),new Rhino.DocObjects.ObjectAttributes());
  __rhino_doc__.Objects.Add(geometry,a);
 }
}
file.Write(System.IO.Path.Combine(root,"05-lbm-layout-"+suffix+".3dm"),8);
System.IO.File.WriteAllText(System.IO.Path.Combine(root,"05-lbm-layout-"+suffix+".json"),solver.Params.Output[3].VolatileData.AllData(true).First().ToString());
__rhino_doc__.Views.Redraw();Console.WriteLine("Exported actual GH outputs for layout "+suffix+"; shift="+shift.CurrentValue);
