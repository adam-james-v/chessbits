# Specify output formats. At least one must = True
STL = True   # [True, False]
WEB = False  # [True, False]
STEP = False # [True, False]

# Set Standard Dimensions
std_d = 40.0    # Diameter of the base [5.0 to 100.0] (mm)
std_h = 48.0    # Height of the neck [10.0 to 200.0 ] (mm) NOTE: this is the height of the bishop.
std_top = 22.0  # Diameter of the top part [5.0 to 100] (mm)

# Specifications for each piece
# Valid pieces: pawn, rook, knight, bishop, queen, king.
# All other variables will be ignored.

# If you only want to generate some pieces, exclude definitions for the ones you dont' need.
# See sample specifications below: Note the exception of the knight, which has no neck portion

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
