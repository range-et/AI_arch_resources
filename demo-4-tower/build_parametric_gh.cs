// Run through Rhino MCP. Creates a NEW definition. Edit root for another computer.
using System;
using System.Linq;
var root="/Users/r2d2/Desktop/AI_arch_resources/demo-4-tower";
var canvas=Grasshopper.Instances.ActiveCanvas;
var doc=new Grasshopper.Kernel.GH_Document();
// Shared construction helpers for the teaching GH definitions.
var proxy=Grasshopper.Instances.ComponentServer.ObjectProxies.First(p=>p.Guid==new Guid("719467e6-7cf5-4848-99b0-c5dd57e5442c"));
Grasshopper.Kernel.GH_Component MakeScript(string name,string file,string[] inputs,string[] outputs,int x,int y){
 var comp=(Grasshopper.Kernel.GH_Component)Grasshopper.Instances.ComponentServer.EmitObjectProxy(proxy.Guid).CreateInstance();
 comp.CreateAttributes();comp.Name=name;comp.NickName=name;comp.Attributes.Pivot=new System.Drawing.PointF(x,y);
 var paramType=comp.Params.Input[0].GetType();
 foreach(var p in comp.Params.Input.ToArray())comp.Params.UnregisterInputParameter(p,true);
 foreach(var p in comp.Params.Output.Skip(1).ToArray())comp.Params.UnregisterOutputParameter(p,true);
 foreach(var n in inputs){var p=(Grasshopper.Kernel.IGH_Param)Activator.CreateInstance(paramType);p.Name=n;p.NickName=n;p.Description=n;p.Optional=false;p.Access=n=="footprints"?Grasshopper.Kernel.GH_ParamAccess.list:Grasshopper.Kernel.GH_ParamAccess.item;comp.Params.RegisterInputParam(p);}
 foreach(var n in outputs){var p=(Grasshopper.Kernel.IGH_Param)Activator.CreateInstance(paramType);p.Name=n;p.NickName=n;p.Description=n;p.Access=Grasshopper.Kernel.GH_ParamAccess.list;comp.Params.RegisterOutputParam(p);}
 comp.Params.OnParametersChanged();doc.AddObject(comp,false);
 var iface=comp.GetType().GetInterface("RhinoCodePlatform.GH.IScriptComponent");
 iface.GetProperty("MarshGuids").SetValue(comp,false);
 iface.GetProperty("Text").SetValue(comp,System.IO.File.ReadAllText(System.IO.Path.Combine(root,file)));
 comp.ExpireSolution(false);
 return comp;
}
Grasshopper.Kernel.Special.GH_NumberSlider Slider(string name,decimal min,decimal max,decimal value,int x,int y,int decimals){
 var s=new Grasshopper.Kernel.Special.GH_NumberSlider();s.CreateAttributes();s.NickName=name;
 s.Slider.Minimum=min;s.Slider.Maximum=max;s.Slider.DecimalPlaces=decimals;s.SetSliderValue(value);
 s.Attributes.Pivot=new System.Drawing.PointF(x,y);doc.AddObject(s,false);return s;
}
Grasshopper.Kernel.Special.GH_Panel Panel(string text,int x,int y,int width,int height){
 var p=new Grasshopper.Kernel.Special.GH_Panel();p.CreateAttributes();p.UserText=text;p.Attributes.Pivot=new System.Drawing.PointF(x,y);p.Attributes.Bounds=new System.Drawing.RectangleF(x,y,width,height);doc.AddObject(p,false);return p;
}
doc.FilePath=System.IO.Path.Combine(root,"04-parametric-tower.gh");canvas.Document=doc;
Panel("PROMPT\nCreate a tower with 12 square floor plates.\nAdd floor-count, storey-height and twist controls.\nKeep slabs and core as closed solids.\n\nCHANGE\nTotal twist: 0 to 60 degrees.",20,20,510,140);
var tower=MakeScript("Parametric tower","parametric_tower.py",new[]{"floors","twist","storey_height"},new[]{"slabs","core","report"},490,260);
var floors=Slider("Floors",6,20,12,40,220,0);
var twist=Slider("Total twist",0,90,0,40,270,0);
var height=Slider("Storey height",2.5m,5,3.2m,40,320,1);
tower.Params.Input[0].AddSource(floors);tower.Params.Input[1].AddSource(twist);tower.Params.Input[2].AddSource(height);
var report=Panel("",680,160,480,340);report.AddSource(tower.Params.Output[3]);

var io=new Grasshopper.Kernel.GH_DocumentIO();io.Document=doc;if(!io.SaveQuiet(doc.FilePath))throw new Exception("GH save failed");
canvas.Viewport.Zoom=1f;canvas.Viewport.Target=new System.Drawing.Point(0,0);canvas.Refresh();doc.NewSolution(false);
Console.WriteLine("Saved "+doc.FilePath);
