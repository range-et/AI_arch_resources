# Demo plan

The priority order is repository cleanup, recorded installation, then the LBM port. The first three steps are now complete. This inventory records what the existing slides contain and what still needs a recording.

| Slide | Existing material | Demo and check | State |
| --- | --- | --- | --- |
| 15 | Rhino MCP setup | Install from Package Manager; restart Rhino; connect Codex; start listener; make and inspect a torus. | OBS video and saved model ready. |
| 16 | Target sketch and command sequence | Show the sketch, retrieve relevant Rhino commands, execute the chosen sequence, inspect the resulting surfaces. Check the command choice against the actual sketch. | Recording pending. |
| 17 | Prompt: “Build Habitat 67” | Run the prompt once. Inspect the actual result, its object types and validity. Report the observed limitations. The slide's claim that direct coordinates always produce irregular geometry needs revision based on that result. | Recording pending. |
| 18 | Placeholder prompt and GH script diagram | Use a specific prompt for a parametric building study. Show generated code in the Python editor, connect sliders, change a parameter, and check changed geometry. The footprint component in the LBM demo is already one working example. | Separate recording pending. |
| 19 | Horizontal airflow slice | Read jviquerat/lbm, adapt the D2Q9/TRT code, connect closed footprints, solve, move one block, solve again, inspect reports and export both results. | OBS walkthrough, full session, GH file, code, two models and checks ready. |
| 20 | Regulatory text to building envelope | Show the official Toronto RD clauses, list lot assumptions, extract numbers with clause references, build the envelope in GH, and change lot depth. Check setbacks, height, coverage and FSI separately. | Fictional lot data and Rhino model exist; GH workflow and recording pending. |
| 21 | Autodesk AEC foundation model diagram | Use a documented Autodesk example or an accessible product session. Check the stated LOD and editability claims against the source before presenting them. | Source check and demo pending. |

For slide 19, the teaching point is that students can find useful research code and adapt it into a tool with inputs they can control. Show the source and licence before showing the GH result. Keep both layouts on the same grid, time steps, inlet speed, viscosity and colour scale. The saved reports show that moving one footprint changes the solution.

Use the short recordings during the talk. Keep the continuous OBS session available for questions about the build process. All future recordings should show the actual prompt, code or command, input change and visible result.
