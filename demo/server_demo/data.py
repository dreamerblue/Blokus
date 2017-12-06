class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

PieceShape = [
    [Point(0, 0)],
    [Point(0, 0), Point(1, 0)],
    [Point(0, 0), Point(0, 1), Point(1, 0)],
    [Point(0, 0), Point(1, 0), Point(2, 0)],
    [Point(0, 0), Point(0, 1), Point(1, 0), Point(1, 1)],
    [Point(0, 0), Point(0, 1), Point(0, 2), Point(1, 1)],
    [Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3)],
    [Point(0, 0), Point(1, 0), Point(2, 0), Point(0, 1)],
    [Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 2)],
    [Point(0, 0), Point(0, 1), Point(1, 0), Point(2, 0), Point(3, 0)],
    [Point(0, 0), Point(0, 1), Point(0, 2), Point(1, 1), Point(2, 1)],
    [Point(0, 0), Point(0, 1), Point(0, 2), Point(1, 0), Point(2, 0)],
    [Point(0, 0), Point(1, 0), Point(1, 1), Point(2, 1), Point(3, 1)],
    [Point(0, 0), Point(0, 1), Point(1, 1), Point(2, 1), Point(2, 2)],
    [Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3), Point(0, 4)],
    [Point(0, 0), Point(0, 1), Point(0, 2), Point(1, 0), Point(1, 1)],
    [Point(0, 0), Point(1, 0), Point(1, 1), Point(2, 1), Point(2, 2)],
    [Point(0, 0), Point(1, 0), Point(2, 0), Point(0, 1), Point(2, 1)],
    [Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 2), Point(2, 1)],
    [Point(1, 0), Point(1, 1), Point(1, 2), Point(0, 1), Point(2, 1)],
    [Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 1), Point(1, 1)]
]

def adhoc_piece_shape_set_generate():
    return [[PieceShape[piece_id] for state in range(8)] for piece_id in range(21)]
