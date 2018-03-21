

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
        .faces('<Y').fillet(notch)
        .faces('>Y').fillet(notch)
    )

    return result

def neck(bottom_d, top_d, height):
    'create neck with bottom diameter, top diameter, and height'
    if bottom_d < top_d:
        raise ValueError('Bottom Diameter cannot be less than top diameter')

    bottom_r = bottom_d/2.0
    top_r = top_d/2.0
    thickness = height*0.05

    ringlist = [
        {'diameter': bottom_d + thickness/2.0, 'thickness': thickness, 'pos': 0.0},
        {'diameter': bottom_d - thickness*0.85, 'thickness': thickness, 'pos': height*0.08},
        {'diameter': top_d + thickness/2.0, 'thickness': thickness, 'pos': height*0.92},
        {'diameter': top_d + thickness/1.75, 'thickness': thickness, 'pos': height},
    ]

    ring_set = add_rings(ringlist)

    base = (cq.Workplane('XY')
        .lineTo(bottom_r, 0.0)
        .threePointArc(
            ((bottom_r-top_r)/3.0 + top_r, height/3.0),
            (top_r, height)
        )
        .lineTo(0.0, height).close()
        .revolve()
    )

    result = base.union(ring_set)

    return result

def top(diameter, piece):

    temp = (cq.Workplane('ZX')
        .box(1.0, 1.0, 1.0)
        .translate((0, 0.5, 0))
    )

    def pawn():
        sphere = (cq.Workplane('XY')
            .sphere(0.5)
            .translate((0, 0.505, 0))
        )

        cyl = (cq.Workplane('ZX')
            .circle(0.375)
            .extrude(0.25)
        )

        ring_spec = [
            {'diameter': 1.05, 'thickness': 0.125, 'pos': 0.0625},        
        ]
        ring = add_rings(ring_spec)

        result = (cyl
            .union(ring)
            .union(sphere)
        )

        return result

    def rook():
        thickness = 0.08
        height = 0.75

        base = (cq.Workplane('ZX')
            .circle(0.5).extrude(height)
            .faces('>Y').circle(0.5 - thickness).cutBlind(-height*0.45)
            .faces('<Y').fillet(thickness*0.85)
            .faces('<Y[-2]').fillet(thickness*0.65)
        )

        notch01 = (cq.Workplane('XY')
            .box(thickness, 2*thickness, 1.1)
            .translate((0, height-thickness, 0))
        )
        notch02 = notch01.rotate((0, 0, 0), (0, 1, 0), 120)
        notch03 = notch01.rotate((0, 0, 0), (0, 1, 0), 240)

        result = (base
            .cut(notch01)
            .cut(notch02)
            .cut(notch03)
        )

        return result

    def knight():
        pass

    def bishop():
        height = 1.0

        top = (cq.Workplane('XY')
            .lineTo(0.25, 0.0)
            .threePointArc((0.425, 0.0875), (0.5, height*0.35))
            # .lineTo(0.0, height)
            .threePointArc((0.15, height*0.85), (0, height))
            .close()
            .revolve()
            .edges().fillet(0.2) #TODO: filter the bottom edge out
        )

        sphere = (cq.Workplane('XY')
            .sphere(0.1125)
            .translate((0.0, height*0.95, 0.0))
        )

        slot_w = 0.1

        top_slice = (cq.Workplane('ZX')
            .workplane(offset=height*0.2)
            .box(0.75, 2.0, slot_w)
            .moveTo(0.0, 0.0).findSolid()
            .rotate((0,0,0), (1,0,0), -55)
            .translate((0, 0.55, 0.5))
        )

        result = top.union(sphere).cut(top_slice)

        return result

    def queen():
        height = 1.05
        
        outer = (cq.Workplane('XY')
            .lineTo(0.5625, 0.0)
            .threePointArc((0.475, height*0.5), (0.675, height))
            .lineTo(0.6, height)
            .threePointArc((0.375, height*0.75), (0.325, height*0.5))
            .lineTo(0, height*0.5)
            .close()
            .revolve()
        )

        cyl_rad = 0.125

        cyl = (cq.Workplane('XY')
            .circle(cyl_rad)
            .extrude(1.0, both=True)
            .translate((0, height, 0))
        )

        angles = range(0, 360, (360/5))

        for angle in angles:
            temp_cyl = cyl.rotate((0, 0, 0), (0, 1, 0), angle)

            outer = outer.cut(temp_cyl)

        fill_sphere = (cq.Workplane('XY')
            .sphere(0.5)
            .translate((0, height*0.65, 0))
        )

        top_sphere = (cq.Workplane('XY')
            .sphere(cyl_rad)
            .translate((0, height + cyl_rad*0.8, 0))
        )

        result = (outer
            .union(fill_sphere)
            .union(top_sphere)
        )

        return result

    def king():
        height = 1.1
        pts = [
            (0.5625, 0.0),
            (0.675, height*0.875),
            (0.3125, height),
            (0.0, height),
        ]
        
        base = (cq.Workplane('XY')
            .polyline(pts)
            .close()
            .revolve()
            .edges('>Y')
            .fillet(0.325)
        )

        top_sphere = (cq.Workplane('XY')
            .sphere(0.235)
            .translate((0, height*0.9, 0))
        ) 

        cr_l, cr_d = 0.35, 0.1
        cross_h = cq.Workplane('XY').box(cr_l, cr_d, cr_d)
        cross_v = cq.Workplane('XY').box(cr_d, cr_l+0.05, cr_d)

        cross = (cross_h
            .union(cross_v)
            .translate((0, height + 0.25, 0))
        )
        
        result = base.union(top_sphere).union(cross)

        return result

        

    # TODO: Find cleaner way to write this?
    if piece == 'pawn':
        result = pawn()
    if piece == 'rook':
        result = rook()
    if piece == 'bishop':
        result = bishop()
    if piece == 'queen':
        result = queen()
    if piece == 'king':
        result = king()
    else:
        result = temp

    result = result.findSolid().scale(diameter)

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
        'base': {'diameter': 40.0, 'height': 12.0},
        'neck': {'bottom_d': 37.0, 'top_d': 17.0, 'height': 45.0},
        'top': {'diameter': 22.0, 'piece': 'king'},
    }

    result = build_piece(spec)
    cqv.show_object(result)
