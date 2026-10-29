# Demo plan

The work followed this order: clean the repository, record the real Rhino MCP installation, record the LBM adaptation, then finish the other slide demos. The deck and guides are at the root. Final artifacts are grouped in numbered demo folders. Older attempts and working notes are in the ignored `working/` folder.

## Slide inventory and run order

| Explanation / video slide | Starting material | Finished demo | Teaching point |
| --- | --- | --- | --- |
| 15 / 16 | Rhino MCP setup diagram | Actual Package Manager installation, Rhino restart, connection and torus check | Connect the design application and confirm that a tool call changes its model. |
| 17 / 18 | Target sketch and suggested command list | Radial profile, Revolve, Cap, Check | Choose native CAD operations for a stated form. |
| 19 / 20 | “Build Habitat 67” and direct coordinate generation | Python script, approximate massing and closed-mesh check | Geometric validity and architectural fidelity require separate checks. |
| 21 / 22 | Prompt and parametric-script placeholders | 12-floor tower, Python component, twist 0 to 60 degrees | A script can expose parameters that the CAD engine evaluates. |
| 23 / 24 | Airflow slice | GitHub source, NumPy port, GH adapter, two solved layouts | Relevant source code can become a design tool after adapting inputs and outputs and testing the result. |
| 25 / 26 | Regulatory text to envelope diagram | Official Toronto clauses, fictional lot assumptions, working GH model and depth change | Check clause conditions before turning values into geometry. |
| 27 / 28 | Autodesk foundation-model diagram and keynote link | Source-checked Building Layout Explorer description and attributed vendor excerpt | Compare a documented product example with the locally tested tools. |

## Playback

The seven added video slides contain native Drive MP4 video objects. Play them in Google Slides after each explanation. The deck has 37 slides. The source files are in the UofT Drive folder. Use the videos in the README table in slide order. Total playback is about nine minutes. Pause after each clip for discussion. Keep the GH files available for changing inputs during questions.

For the LBM clip, point out the source credit, the retained TRT routines, the footprint mask and the report. Compare layouts with the same numerical settings and colour scale. The reports confirm that the changed footprint changes the field. The numerical checks establish reproduction and input response. They do not establish physical accuracy.

For Toronto, state the fictional zone and lot first. Show the selected clause conditions and declared assumptions before the model. Reducing depth changes both the rear setback and the permitted floor-area calculation.

The Autodesk clip is a published vendor demonstration. It was not run independently in a local Forma account. The local Rhino and Grasshopper clips show software execution from prepared commands and scripts, including parameter changes and saved results. They are edited OBS captures with labelled cuts and speeds.
