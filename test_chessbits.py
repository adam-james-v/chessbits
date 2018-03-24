import cadquery as cq
import unittest
import chessbits as cb

class ChessbitsTest(unittest.TestCase):
    """Tests for chessbits.py"""

    def test_ring(self):
        """Does the ring function generate correct geometry?"""
        a = len(cb.ring(20.0, 2.0).edges().vals())
        self.assertEquals(a, 7)

    def test_base(self):
        """Does the base function generate correct geometry?"""
        a = len(cb.base(30.0, 10.0).edges().vals())
        self.assertEquals(a, 13)

    def test_neck(self):
        """Does the neck function generate correct geometry?"""
        a = len(cb.neck(20.0, 10.0, 30.0).edges().vals())
        self.assertEquals(a, 37)

    def test_top(self):
        """Does the top function generate correct geometry?"""
        d = 10.0
        pawn = len(cq.Workplane('XY').union(cb.top(d, 'pawn')).edges().vals())
        rook = len(cq.Workplane('XY').union(cb.top(d, 'rook')).edges().vals())
        knight = len(cq.Workplane('XY').union(cb.top(d, 'knight')).edges().vals())
        bishop = len(cq.Workplane('XY').union(cb.top(d, 'bishop')).edges().vals())
        king = len(cq.Workplane('XY').union(cb.top(d, 'king')).edges().vals())
        queen = len(cq.Workplane('XY').union(cb.top(d, 'queen')).edges().vals())
        self.assertEquals(pawn, 13)
        self.assertEquals(rook, 82)
        self.assertEquals(knight, 154)
        self.assertEquals(bishop, 24)
        self.assertEquals(king, 44)
        self.assertEquals(queen, 70)

    def test_add_rings(self):
        """Does the add rings function add correct geometry?"""
        ringlist = [
            {'diameter': 30.0, 'thickness': 5.0, 'pos': 0.0},
            {'diameter': 30.0, 'thickness': 5.0, 'pos': 20.0},
            {'diameter': 30.0, 'thickness': 5.0, 'pos': 40.0},
        ]
        a = len(cb.add_rings(ringlist).edges().vals())
        self.assertEquals(a, 21)

    def test_build_piece(self):
        """Does the build_piece function work?"""
        a = len(cb.build_piece(cb.specs('pawn')).edges().vals())
        self.assertEquals(a, 59)

if __name__ == '__main__':
    unittest.main()
