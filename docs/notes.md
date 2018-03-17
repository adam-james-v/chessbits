# Requirements

- callable from command line
- code useable in Jupyter notebooks (so that people can try it out online)
- should have some parametric ability 
    - specify the base radius (within a range)
    - specify the piece height (within a range)
        - if all pieces are being run, height given is the bishop's height
        - all other pieces have a modified height up or down from that only if heights are not explicitly specified
    - scale of the piece's top component relative to the base (maybe relative to something else relevant) ?
    - maybe the tesselation detail of an output file?
    - after parameters, you can specify the scale
- a preview of some kind is needed
- output files:
    - .stl
    - .step
    - .svg for preview purposes ?
- shareable ? some way to share to twitter, maybe Shapeways?
- easy to distribute
    - maybe one single file
    - if not one file, a very simple python package
    - either way, a clear README.md for running the script
- default run should generate an archive of all of the pieces with default values and default scale, for quick download.
    - this might need re-thinking
- code should be well commented so that people can understand the cadquery library


# Technical Requirements

- follow PEP8 as close as is reasonable
- use classes to better organize and re-use geometry
- do NOT create situations where details are stretched or squished. That is, do not use percent multipliers to parameterize variables from global params.
- the 'ring' details could be specified better. Use a loop and lists instead
- use proper pythonic design patterns
    - if name == main
    - classes
    - properties ?
- Command line version must accept:
    - piece type, if none, do all
    - params [b,h,top scale,total scale], individual piece height overrides
    - outputs [svg, stl, step, all] stl is default
- jupyter version must have:
    - drop down for which piece to view / generate
    - boxes for height, base, top scale params
    - scale output option
    - drop down for export type