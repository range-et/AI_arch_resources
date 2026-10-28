// Run inside Rhino MCP's run_csharp tool. Rebuilds the teaching definition in a NEW GH document.
// All code and the GH file stay at the repository root.
var root="/Users/r2d2/Desktop/AI_arch_resources";
var canvas=Grasshopper.Instances.ActiveCanvas;
var doc=new Grasshopper.Kernel.GH_Document();
doc.FilePath=System.IO.Path.Combine(root,"05-lbm-tool.gh");
canvas.Document=doc;
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
var goal=Panel("SOURCE: github.com/jviquerat/lbm\nD2Q9 / TRT\n\nTASK\nAdapt this code into a GH tool.\nClosed footprints become obstacles.\nMove one footprint and solve again.\n\nLattice units. 2D laminar teaching model.\nSee lbm_prompt.txt for the full prompt.",20,20,360,230);
var geometry=MakeScript("Building footprints","lbm_footprints.py",new[]{"shift"},new[]{"footprints","buildings"},440,250);
var solver=MakeScript("LBM flow slice","lbm_grasshopper.py",new[]{"footprints","steps","inlet","tau"},new[]{"mesh","vectors","report"},800,250);
var shift=Slider("Middle block shift",-15,4,0,180,285,0);
var steps=Slider("Time steps",100,6000,1800,480,420,0);
var inlet=Slider("Inlet speed",.01m,.06m,.03m,480,470,3);
var tau=Slider("Tau",.55m,1.2m,.65m,480,520,2);
geometry.Params.Input[0].AddSource(shift);
solver.Params.Input[0].AddSource(geometry.Params.Output[1]);
solver.Params.Input[1].AddSource(steps);solver.Params.Input[2].AddSource(inlet);solver.Params.Input[3].AddSource(tau);
var report=Panel("",1100,190,430,570);report.AddSource(solver.Params.Output[3]);
var io=new Grasshopper.Kernel.GH_DocumentIO();io.Document=doc;
if(!io.SaveQuiet(doc.FilePath))throw new Exception("GH save failed");
canvas.Viewport.Zoom=0.9f;
canvas.Viewport.Target=new System.Drawing.Point(0,0);
canvas.Refresh();
Console.WriteLine("Saved new GH tool: "+doc.FilePath+". Solver="+solver.InstanceGuid+". Shift="+shift.InstanceGuid);
doc.NewSolution(false);
