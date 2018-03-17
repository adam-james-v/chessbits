

import cadquery as cq
import cqmods.cqview as cqv

def ring(diameter, thickness):
    'create a horizontal ring with diameter and thickness'
    
    result = (cq.Workplane('ZX')
        .workplane(offset=-thickness/2.0)
        .circle(diameter/2.0).extrude(thickness)
        .edges().fillet(thickness/2.05)
    )
    
    return result

def base(diameter, height):
    'create a base with diameter and height'
    # TODO: add validation to params here?
    radius = diameter/2.0
    notch = height * 0.1

    pts = [
        (radius, 0.0),
        (radius, (2.0/3.0)*height - notch),        
        (radius - notch, (2.0/3.0)*height),        
        (radius, (2.0/3.0)*height + notch),        
        (radius, height),        
        (0.0, height),        
    ]
    
    result = (cq.Workplane('XY')
        .polyline(pts).close()
        .revolve()
        .faces('|Z').fillet(notch)
    )

    return result

def neck(bottom_d, top_d, height):
    'create neck with bottom diameter, top diameter, and height'
    if bottom_d < top_d:
        raise ValueError('Bottom Diameter cannot be less than top diameter')

    bottom_r = bottom_d/2.0
    top_r = top_d/2.0
    
    result = (cq.Workplane('XY')
        .lineTo(bottom_r, 0.0)
        .threePointArc(
            ((bottom_r-top_r)/3.0 + top_r, height/3.0), 
            (top_r, height) 
        )
        .lineTo(0.0, height).close()
        .revolve()
    )

    return result

def top(diameter, piece):
    
    result = (cq.Workplane('ZX')
        .box(diameter, diameter, diameter)
        .translate((0, diameter/2.0, 0))
    )

    def pawn():
        pass
    
    def rook():
        pass

    def knight():
        pass

    def bishop():
        pass

    def queen():
        pass

    def king():
        pass
    
    return result

def add_rings(rings):
    'return a stack of rings to be added to the result'
    result = cq.Workplane('ZX')
    for spec in rings:
        h = spec.pop('pos', 0)
        result = result.union(ring(**spec).translate((0, h, 0)))
    return result

def build_piece(specs):
    'build a piece based on specs given'
    result = cq.Workplane('ZX')
    base_h = specs['base']['height']
    neck_h = base_h + specs['neck']['height']

    for part in specs:
        spec = specs[part]
        if part == 'base':
            result = result.union(base(**spec))
        if part == 'neck':
            result = result.union(neck(**spec).translate((0, base_h, 0)))
        if part == 'top':
            result = result.union(top(**spec).translate((0, neck_h, 0)))
    return result

def build_set():
    pass


if __name__ == '__main__':

    spec = {
        'base': {'diameter': 50.0, 'height': 20.0},
        'neck': {'bottom_d': 45.0, 'top_d': 25.0, 'height': 70.0},
        'top': {'diameter': 32.0, 'piece': 'blah'},
    }

    # result = build_piece(spec)

    ringlist = [
        {'diameter': 20.0, 'thickness': 2.0, 'pos': 10.0},
        {'diameter': 30.0, 'thickness': 2.0, 'pos': 20.0},
        {'diameter': 40.0, 'thickness': 2.0, 'pos': 30.0},
    ]

    result = add_rings(ringlist)
    cqv.show_object(result)