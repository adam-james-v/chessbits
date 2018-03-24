import os
import sys
import cadquery as cq
import cqview as cqv

try:
    import config
    config_exists = True
except:
    config_exists = False
    pass


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

    if diameter > 100.0 or diameter < 5.0:
        raise ValueError("Diameter must be between 5 and 100 (inclusive)")
    if height < diameter / 5.0:
        raise ValueError("Height must be greater than %f" % (diameter/5.0))

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

    if bottom_d > 100.0 or bottom_d < 5.0 or top_d > 100.0 or top_d < 5.0:
        raise ValueError('Diameter must be between 5 and 100 (inclusive)')
    if bottom_d < top_d:
        raise ValueError('Bottom Diameter cannot be less than top diameter')
    if height > 200.0 or height < 10.0:
        raise ValueError('Height must be between 10 and 200 (inclusive)')

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

    valid_pieces = ['pawn', 'rook', 'knight', 'bishop', 'king', 'queen']

    if diameter > 100.0 or diameter < 5.0:
        raise ValueError("Diameter must be between 5 and 100 (inclusive)")
    if piece not in valid_pieces:
        raise ValueError("Invalid piece type. Valid entries are : pawn, rook, knight, bishop, king, queen")

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
        base_radius = 12.5

        pts =[
            (10.0, 0.0),
            (9.5, 7.35),
            (6.35, 14.325),
            (0.0, 20.0),
            (3.5, 21.0),
            (7.65, 20.0),
            (10.75, 16.5),
            (17.135, 16.75),
            (19.0, 22.0),
            (0.5, 40.0),
            (-7.5, 40.0),
            (-13.25, 37.0),
            (-15.8, 33.60),
            (-18.675, 25.325),
            (-15.31, 11.0),
            (-13.5, 0.0),
        ]

        body = (cq.Workplane('XY').workplane(offset=-base_radius*0.75)
            .polyline(pts).close()
            .extrude(base_radius*1.5)
            .edges('|Z').fillet(1.75)
        )

        left_cyl_cut = (cq.Workplane('ZY').workplane(offset=-50)
            .moveTo(-256.0, 40).circle(250.0).extrude(100.0)
        )
        right_cyl_cut = (cq.Workplane('ZY').workplane(offset=-50)
            .moveTo(256.0, 40).circle(250.0).extrude(100.0)
        )

        left_box_cut = (cq.Workplane('XY').box(100,20,10)
            .rotate((0, 0, 0), (0, 1, 0), 4.5)
            .rotate((0, 0, 0), (0, 0, 1), -29)
            .translate((0, 34, 11.5))
        )

        right_box_cut = (cq.Workplane('XY').box(100,20,10)
            .rotate((0, 0, 0), (0, 1, 0), -4.5)
            .rotate((0, 0, 0), (0, 0, 1), -29)
            .translate((0, 34, -11.5))
        )

        ring01 = ring(15.75, 4.5)
        base_ring = ring(32.0, 4.5)

        slicer = (cq.Workplane('XY')
            .box(32,32,32)
            .translate((0,0,16))
        )

        mohawk = (ring01.cut(slicer)
            .rotate((0,0,0), (1,0,0), 90)
            .rotate((0,0,0), (0,0,1), 53)
            .translate((-6.5,25,0))
        )

        left_ear = (cq.Workplane('ZY')
            .lineTo(4.0, 0.0)
            .lineTo(0.0, 6.5)
            .close()
            .extrude(4.5)
            .translate((0,37.5,-2.1))
            .rotate((0,0,0), (0,1,0), -6)
            .rotate((0,0,0), (1,0,0), -5)
        )

        right_ear = (cq.Workplane('ZY')
            .lineTo(-4.0, 0.0)
            .lineTo(0.0, 6.5)
            .close()
            .extrude(4.5)
            .translate((0,37.5,2.1))
            .rotate((0,0,0), (0,1,0), 6)
            .rotate((0,0,0), (1,0,0), 5)
        )

        ear_slice = (cq.Workplane('XY')
            .box(11,11,50)
            .rotate((0,0,0), (0,0,1), 45)
            .translate((-4.8,48.75,0))
        )

        result = (body
            .cut(left_cyl_cut)
            .cut(right_cyl_cut)
            .cut(left_box_cut)
            .cut(right_box_cut)
            .union(mohawk)
            .union(left_ear)
            .union(right_ear)
            .cut(ear_slice)
            .translate((1.5,0,0))
            .union(base_ring)
            .findSolid().scale(0.0267)
        )

        return result

    def bishop():
        height = 1.0

        top = (cq.Workplane('XY')
            .lineTo(0.25, 0.0)
            .threePointArc((0.425, 0.0875), (0.5, height*0.35))
            # .lineTo(0.0, height)
            .threePointArc((0.15, height*0.85), (0, height))
            .close()
            .revolve()
            .edges().fillet(0.2)
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

    # set result equal to the function with name matching piece
    result = locals()[piece]()

    try:
        # Fails on knight() due to knight already being scaled
        result = result.findSolid().scale(diameter)
    except:
        # For knight, skip .findSolid()
        result = result.scale(diameter)

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

    # For Knight, no 'neck' exists, so instead set neck_h to base_h
    try:
        neck_h = base_h + specs['neck']['height']
    except:
        neck_h = base_h

    for part in specs:
        spec = specs[part]
        if part == 'base':
            result = result.union(base(**spec))
        if part == 'neck':
            result = result.union(neck(**spec).translate((0, base_h, 0)))
        if part == 'top':
            result = result.union(top(**spec).translate((0, neck_h, 0)))
    return result

def specs(piece, std_d=40.0, std_h=48.0, std_top=22.0):

    pawn = {
        'base': {'diameter': std_d, 'height': std_h/4.0},
        'neck': {'bottom_d': std_d*0.925, 'top_d': std_d*0.4, 'height': std_h*0.65},
        'top': {'diameter': std_top*0.95, 'piece': 'pawn'},
        }

    rook = {
        'base': {'diameter': std_d, 'height': std_h/4.0},
        'neck': {'bottom_d': std_d*0.95, 'top_d': std_d*0.425, 'height': std_h*0.85},
        'top': {'diameter': std_top, 'piece': 'rook'},
        }

    knight = {
        'base': {'diameter': std_d, 'height': std_h/4.0},
        'top': {'diameter': std_top*2.1, 'piece': 'knight'},
        }

    bishop = {
        'base': {'diameter': std_d, 'height': std_h/4.0},
        'neck': {'bottom_d': std_d*0.95, 'top_d': std_d*0.425, 'height': std_h},
        'top': {'diameter': std_top, 'piece': 'bishop'},
        }

    queen = {
        'base': {'diameter': std_d, 'height': std_h/4.0},
        'neck': {'bottom_d': std_d*0.95, 'top_d': std_d*0.425, 'height': std_h*1.3},
        'top': {'diameter': std_top, 'piece': 'queen'},
        }

    king = {
        'base': {'diameter': std_d, 'height': std_h/4.0},
        'neck': {'bottom_d': std_d*0.95, 'top_d': std_d*0.425, 'height': std_h*1.3},
        'top': {'diameter': std_top, 'piece': 'king'},
        }
    return locals()[piece]


def output(pieces=None, custom=False, STL=True, WEB=False, STEP=False):
    if not any([STL, WEB, STEP]):
        print("Sorry, you have not specified any output format. Doing nothing instead.")
    else:
        path = os.path.join(os.getcwd(), 'output')
        try:
            os.makedirs(path)
        except OSError:
            if not os.path.isdir(path):
                raise

        if not pieces:
            pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']

        result = cq.Workplane('XY')

        for idx, piece in enumerate(pieces):
            spacing = 50.0
            start = -((len(pieces) - 1) * spacing)/2.0
            if custom:
                temp = build_piece(getattr(config, piece))
            else:
                temp = build_piece(specs(piece))
            if STL:
                out = temp.rotate((0,0,0), (1,0,0), 90).findSolid().exportStl(('output/%s.stl' % piece), 0.01)
                print('Created file: output/%s.stl' % piece)
            temp = temp.translate((start + idx*spacing, 0, 0,))
            result = result.union(temp)

        if WEB:
            cqv.show_object(result)
            print('Created file: web_view/assembly.json')
            print('--- To view the web output, please start a server in the web_view/ folder ---')
        if STEP:
            result.findSolid().exportStep('output/pieces.step')
            print('Created file: output/pieces.step')

        print('Your files have been generated successfully.')
    return

def user_build():
    to_build = []
    for val in dir(config):
        if val in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']:
            to_build.append(val)
    output(to_build, custom=True, STL=config.STL, WEB=config.WEB, STEP=config.STEP)
    return


if __name__ == '__main__':

    if len(sys.argv) < 2:
        output()
    else:
        to_build = []
        STL_arg = True
        WEB_arg = False
        STEP_arg = False
        for arg in sys.argv:
            if arg in ['custom', 'use_specs']:
                if config_exists:
                    user_build()
                else:
                    print('You have indicated that you wish to build with custom specifications but no specs.py file was found. Could there be a typo?')
                quit()
            elif arg in ['pawn', 'rook', 'knight', 'bishop', 'king', 'queen']:
                to_build.append(arg)
            elif arg in ['noSTL', 'nostl']:
                STL_arg = False
            elif arg in ['WEB', 'web']:
                WEB_arg = True
            elif arg in ['STEP', 'step', 'stp']:
                STEP_arg = True
            elif not arg.endswith('.py'):
                print("Ignoring invalid input: %s. Perhaps there was a typo?" % arg)
        output(to_build, STL=STL_arg, WEB=WEB_arg, STEP=STEP_arg)
