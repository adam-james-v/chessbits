import cadquery as cq
from cqview import show_object
from cqview import show_svg


# NOTES:
# GLTF EXPORT WORKS WITH CQPARTS
# TODO: properly install cqparts, not just run from src folder
# TODO: Take this prototype code and re-factor to use classes as per cqparts
# TODO: study the GLTF format to see if I can add lights, edges, etc.


# THIS WHOLE SCRIPT IS A MESS
# CONSIDER IT ONLY A PROTOTYPE
# TODO: figure out a good way to make things actually parametric. Suggestion: don't. Just allow scaling
# TODO: come up with a class structure (possibly use pen and paper for architecting this)
# See CQPARTS for inspiration.

# PARAMETERS (ASSUME UNITS IN mm)

base_r = 12.5
base_h = 10.0
standard_h = 56.0 # ASSUME THIS IS A MEDIAN HEIGHT SO, PAWNS WILL BE SHORTER AND KING WILL BE TALLER

# neck_r = base_r*0.9 #TODO: make 'secondary  variables'


def base(radius, height):
    
    pts = [
        (radius, 0.0),
        (radius, (2.0/3.0)*height - 1),        
        (radius - 1, (2.0/3.0)*height),        
        (radius, (2.0/3.0)*height + 1),        
        (radius, height),        
        (0.0, height),        
    ]
    
    result = (cq.Workplane('XY')
        .polyline(pts).close()
        .revolve()
        .faces('|Z').fillet(0.75)
    )

    return result

def neck(bottom_radius, top_radius, height):
    result = (cq.Workplane('XY')
        .lineTo(bottom_radius, 0.0)
        .threePointArc(( (bottom_radius-top_radius)/3.0 + top_radius, height*0.9/2.85), 
                         (top_radius, height) )
        .lineTo(0.0, height).close()
        .revolve()
    )

    return result


def ring(radius, thickness):
    result = (cq.Workplane('ZX')
        .workplane(offset=-thickness/2.0)
        .circle(radius).extrude(thickness)
        .edges().fillet(thickness/2.05)
    )

    return result


def pawn(base_radius=base_r, base_height=base_h, total_height=standard_h*0.7):

    def pawn_top(radius):
        pawn_top_sphere = (cq.Workplane('XY')
            .sphere(radius)
            .translate((0.0, radius, 0.0))
        )
        pawn_top_base = (cq.Workplane('ZX')
            .circle(radius*0.4)
            .extrude(radius)
        )

        result = pawn_top_base.union(pawn_top_sphere)

        return result

    pawn_base = base(base_radius, base_height)

    # Should I make a 'top height' instead?
    top_radius = base_radius*0.5
    pawn_top = pawn_top(top_radius).translate((0, total_height - 2*top_radius, 0))

    neck_height = total_height - base_height - 2*top_radius
    pawn_neck = neck(base_radius*0.90, base_radius*0.35, neck_height).translate((0, base_height, 0))

    pawn_ring_01 = ring(base_radius*0.45, total_height*0.05).translate((0, total_height - 1.9*top_radius, 0))
    pawn_ring_02 = ring(base_radius*0.65, total_height*0.065).translate((0, total_height*0.34, 0))
    
    result = (pawn_base
        .union(pawn_neck)
        .union(pawn_top)
        .union(pawn_ring_01)
        .union(pawn_ring_02)
    )

    return result

def bishop(base_radius=base_r, base_height=base_h, total_height=standard_h):

    def bishop_top(radius, height):
        # If I can find a skew transformation matrix, try to use that instead.
        # TODO: FIX up multipliers on the radius inside this function
        bishop_top_shape = (cq.Workplane('XY')
            .lineTo(radius*0.5, 0.0)
            .threePointArc((radius*0.85, height*0.175), (radius, height*0.35))
            # .lineTo(0.0, height)
            .threePointArc((radius*0.3, height*0.85), (0, height))
            .close()
            .revolve()
            .edges().fillet(radius*0.65) #TODO: filter the bottom edge out
        )
        bishop_top_sphere = (cq.Workplane('XY')
            .sphere(radius*0.2)
            .translate((0.0, height*0.95, 0.0))
        )

        slot_w = total_height*0.02

        bishop_slice = (cq.Workplane('ZX')
            .workplane(offset=height*0.2)
            .moveTo(-total_height*0.15, 0.0)
            .box(total_height*0.2, total_height*0.2, slot_w)
            .moveTo(0.0, 0.0).findSolid()
            .rotate((0,0,0), (1,0,0), 55)
        )

        result = bishop_top_shape.cut(bishop_slice).union(bishop_top_sphere)

        # result = result.findSolid().transformGeometry(Base.Matrix) #This needs work
        return result
    
    bishop_base = base(base_radius, base_height)

    top_height = total_height*0.225
    bishop_top = bishop_top(base_radius*0.5, top_height).translate((0, total_height - top_height, 0))

    neck_height = total_height - base_height - top_height
    bishop_neck = neck(base_radius*0.90, base_radius*0.3, neck_height).translate((0, base_height, 0))

    bishop_ring_01 = ring(base_radius*0.45, total_height*0.04).translate((0,total_height - top_height,0))
    bishop_ring_02 = ring(base_radius*0.35, total_height*0.03).translate((0, total_height*0.7, 0))
    bishop_ring_03 = ring(base_radius*0.65, total_height*0.065).translate((0, total_height*0.295, 0))
    bishop_ring_04 = ring(base_radius*0.95, total_height*0.06).translate((0, base_height, 0))

    result = (bishop_base
        .union(bishop_neck)
        .union(bishop_top)
        .union(bishop_ring_01)
        .union(bishop_ring_02)
        .union(bishop_ring_03)
        .union(bishop_ring_04)
    )

    return result


def rook(base_radius=base_r, base_height=base_h, total_height=standard_h*0.85):

    def rook_top(radius, height): #TODO : Don't have variable names share function names

        inner_radius = (radius - radius*0.2)
        thickness = (radius - inner_radius)

        result = (cq.Workplane('ZX')
            .circle(radius).extrude(height)
            .faces('>Y').circle(inner_radius).cutBlind(-height*0.4)
            .faces('<Y').fillet(radius*0.08)
        )

        rook_slice = cq.Workplane('XY').box(thickness, 2*thickness, 2*radius).translate((0, height-thickness, 0))
        rook_slice_02 = rook_slice.rotate((0, 0, 0), (0, 1, 0), 120)
        rook_slice_03 = rook_slice.rotate((0, 0, 0), (0, 1, 0), 240)

        result = result.cut(rook_slice).cut(rook_slice_02).cut(rook_slice_03)

        return result

    rook_base = base(base_radius, base_height)

    top_height = total_height*0.2
    rook_top = rook_top(base_radius*0.6, top_height).translate((0, total_height - top_height, 0)) #IS IT BETTER TO MULTIPLY A FLOAT OR DIVIDE??
    
    neck_height = total_height - base_height - top_height
    rook_neck = neck(base_radius*0.9, base_radius*0.4, neck_height).translate((0, base_height, 0))

    # TODO: maybe make a 'ring builder' taht takes a list of ring radii, thicknesses, and height
    rook_ring_01 = ring(base_radius*0.55, total_height*0.075).translate((0, total_height*0.8, 0))
    rook_ring_02 = ring(base_radius*0.465, total_height*0.04).translate((0, total_height*0.7125, 0))
    rook_ring_03 = ring(base_radius*0.95, total_height*0.06).translate((0, base_height, 0))

    result = (rook_base
        .union(rook_neck)
        .union(rook_top)
        .union(rook_ring_01)
        .union(rook_ring_02)
        .union(rook_ring_03)
    )
    # result = rook_top

    return result

def knight(base_radius=base_r, base_height=base_h, total_height=standard_h*0.85):

    def knight_top(height): #TODO : Don't have variable names share function names
        
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
            .edges('|Z').fillet(1.5)
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

        ring01 = (ring(15.75, 4.5)
        )

        slicer = (cq.Workplane('XY')
            .box(32,32,32)
            .translate((0,0,16))
        )

        mohawk = (ring01
            .cut(slicer)
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
            .findSolid().scale(0.8)
        )

        return result

    knight_base = base(base_radius, base_height)

    top_height = total_height - base_height
    knight_top = knight_top(top_height).translate((0, base_height, 0)) #IS IT BETTER TO MULTIPLY A FLOAT OR DIVIDE??
    
    result = (knight_base
        .union(knight_top)
    )

    return result


def king(base_radius=base_r, base_height=base_h, total_height=standard_h*1.225):

    def king_top(radius, height):
        # If I can find a skew transformation matrix, try to use that instead.
        # TODO: FIX up multipliers on the radius inside this function
        pts = [
            (radius*1.125, 0.0),
            (radius*1.35, height*0.875),
            (radius*0.625, height),
            (0.0, height),
        ]
        
        main = (cq.Workplane('XY')
            .polyline(pts)
            .close()
            .revolve()
            .edges('>Y')
            .fillet(3.0)
        )

        king_top_sphere = (cq.Workplane('XY')
            .sphere(3.25)
            .translate((0, height*0.9, 0))
        ) 

        cross_h = cq.Workplane('XY').box(8,2.5,2.5)
        cross_v = cq.Workplane('XY').box(2.5,9,2.5)

        cross = cross_h.union(cross_v).translate((0, height + 5, 0))
        
        result = main.union(king_top_sphere).union(cross)

        return result
    
    king_base = base(base_radius, base_height)

    top_height = total_height*0.225
    king_top = king_top(base_radius*0.5, top_height).translate((0, total_height - top_height, 0))

    neck_height = total_height - base_height - top_height
    king_neck = neck(base_radius*0.90, base_radius*0.4, neck_height).translate((0, base_height, 0))

    king_ring_01 = ring(base_radius*0.45, total_height*0.04).translate((0,total_height - top_height,0))
    king_ring_02 = ring(base_radius*0.425, total_height*0.035).translate((0, total_height*0.75, 0))
    king_ring_03 = ring(base_radius*0.65, total_height*0.065).translate((0, total_height*0.295, 0))
    king_ring_04 = ring(base_radius*0.95, total_height*0.0525).translate((0, base_height, 0))
    king_ring_05 = ring(base_radius*0.61, 1.7).translate((0, total_height - top_height + 0.8, 0))
    king_ring_06 = ring(base_radius*0.475, 1.75).translate((0, total_height*0.7, 0))
    king_ring_07 = ring(base_radius*0.8, 5.05).translate((0, base_height + 3.5, 0))

    result = (king_base
        .union(king_neck)
        .union(king_top)
        .union(king_ring_01)
        .union(king_ring_02)
        # .union(queen_ring_03)
        .union(king_ring_04) # closest to the base
        .union(king_ring_05) # Just below queen top piece
        .union(king_ring_06) # third ring from bottom
        .union(king_ring_07) # second ring from bottom
    )

    return result


def queen(base_radius=base_r, base_height=base_h, total_height=standard_h*1.225):

    def queen_top(radius, height):
        # If I can find a skew transformation matrix, try to use that instead.
        # TODO: FIX up multipliers on the radius inside this function
        outer = (cq.Workplane('XY')
            .lineTo(radius*1.125, 0.0)
            .threePointArc((radius*0.95, height*0.5), (radius*1.35, height))
            .lineTo(radius*1.2, height)
            .threePointArc((radius*0.75, height*0.75), (radius*0.65, height*0.5))
            .lineTo(0, height*0.5)
            .close()
            .revolve()
        )

        # TODO: make this a loop
        cyl_rad = 1.75
        cyl_01 = (cq.Workplane('XY')
            .circle(cyl_rad)
            .extrude(3*radius, both=True)
            .translate((0, height, 0))
        )
        cyl_02 = (cq.Workplane('XY')
            .circle(cyl_rad)
            .extrude(3*radius, both=True)
            .rotate((0, 0, 0), (0,1,0), 72)
            .translate((0, height, 0))
        )
        cyl_03 = (cq.Workplane('XY')
            .circle(cyl_rad)
            .extrude(3*radius, both=True)
            .rotate((0, 0, 0), (0,1,0), 144)
            .translate((0, height, 0))
        )
        cyl_04 = (cq.Workplane('XY')
            .circle(cyl_rad)
            .extrude(3*radius, both=True)
            .rotate((0, 0, 0), (0,1,0), 216)
            .translate((0, height, 0))
        )
        cyl_05 = (cq.Workplane('XY')
            .circle(cyl_rad)
            .extrude(3*radius, both=True)
            .rotate((0, 0, 0), (0,1,0), 288)
            .translate((0, height, 0))
        )
        sph = (cq.Workplane('XY')
            .sphere(radius)
            .translate((0, height*0.65, 0))
        )
        # TODO: be more consistent with variable names. EG. sph vs top_sphere
        queen_top_sphere = (cq.Workplane('XY')
            .sphere(cyl_rad)
            .translate((0, height + cyl_rad*0.8, 0))
        )

        result = (outer
            .cut(cyl_01)
            .cut(cyl_02)
            .cut(cyl_03)
            .cut(cyl_04)
            .cut(cyl_05)
            .union(sph)
            .union(queen_top_sphere)
        )

        return result
    
    queen_base = base(base_radius, base_height)

    top_height = total_height*0.225
    queen_top = queen_top(base_radius*0.5, top_height).translate((0, total_height - top_height, 0))

    neck_height = total_height - base_height - top_height
    queen_neck = neck(base_radius*0.90, base_radius*0.4, neck_height).translate((0, base_height, 0))

    queen_ring_01 = ring(base_radius*0.45, total_height*0.04).translate((0,total_height - top_height,0))
    queen_ring_02 = ring(base_radius*0.425, total_height*0.035).translate((0, total_height*0.75, 0))
    queen_ring_03 = ring(base_radius*0.65, total_height*0.065).translate((0, total_height*0.295, 0))
    queen_ring_04 = ring(base_radius*0.95, total_height*0.0525).translate((0, base_height, 0))
    queen_ring_05 = ring(base_radius*0.61, 1.7).translate((0, total_height - top_height + 0.8, 0))
    queen_ring_06 = ring(base_radius*0.475, 1.75).translate((0, total_height*0.7, 0))
    queen_ring_07 = ring(base_radius*0.8, 5.05).translate((0, base_height + 3.5, 0))

    result = (queen_base
        .union(queen_neck)
        .union(queen_top)
        .union(queen_ring_01)
        .union(queen_ring_02)
        # .union(queen_ring_03)
        .union(queen_ring_04) # closest to the base
        .union(queen_ring_05) # Just below queen top piece
        .union(queen_ring_06) # third ring from bottom
        .union(queen_ring_07) # second ring from bottom
    )

    return result



pawn1 = pawn().translate((base_r*-10.5, 0, base_r*-1.5))
pawn2 = pawn().translate((base_r*-7.5, 0, base_r*-1.5))
pawn3 = pawn().translate((base_r*-4.5, 0, base_r*-1.5))
pawn4 = pawn().translate((base_r*-1.5, 0, base_r*-1.5))
pawn5 = pawn().translate((base_r*1.5, 0, base_r*-1.5))
pawn6 = pawn().translate((base_r*4.5, 0, base_r*-1.5))
pawn7 = pawn().translate((base_r*7.5, 0, base_r*-1.5))
pawn8 = pawn().translate((base_r*10.5, 0, base_r*-1.5))
rook1 = rook().translate((base_r*-10.5, 0, base_r*1.5))
knight1 = knight().translate((base_r*-7.5, 0, base_r*1.5))
bishop1 = bishop().translate((base_r*-4.5, 0, base_r*1.5))
queen = queen().translate((base_r*-1.5, 0, base_r*1.5))
king = king().translate((base_r*1.5, 0, base_r*1.5))
bishop2 = bishop().translate((base_r*4.5, 0, base_r*1.5))
knight2 = knight().translate((base_r*7.5, 0, base_r*1.5))
rook2 = rook().translate((base_r*10.5, 0, base_r*1.5))

result = (pawn1
    .union(pawn2)
    .union(pawn3)
    .union(pawn4)
    .union(pawn5)
    .union(pawn6)
    .union(pawn7)
    .union(pawn8)
    .union(rook1)
    .union(bishop1)
    .union(knight1)
    .union(queen)
    .union(king)
    .union(rook2)
    .union(bishop2)
    .union(knight2)
    .rotate((0,0,0), (0,1,0), 180)
)

# show_svg(result)
show_object(result)