class Board(object):
    """

    >>> Board().rows
    ((' ', ' ', ' '), (' ', ' ', ' '), (' ', ' ', ' '))
    >>> print Board()
     | | 
    -----
     | | 
    -----
     | | 
    >>> Board().columns
    ((' ', ' ', ' '), (' ', ' ', ' '), (' ', ' ', ' '))
    >>> Board().turn
    0
    >>> Board().whose_turn
    'x'
    >>> b = Board().move(2); print b
     | |x
    -----
     | | 
    -----
     | | 
    >>> b.possible()
    [< Board |o.x......| >, < Board |.ox......| >, < Board |..xo.....| >, < Board |..x.o....| >, < Board |..x..o...| >, < Board |..x...o..| >, < Board |..x....o.| >, < Board |..x.....o| >]
    """
    def __init__(self, width=3, height=3):
        self._rows = [[' ' for _ in range(width)] for _ in range(height)]

    rows = property(lambda self: tuple(tuple(row) for row in self._rows))
    columns = property(lambda self: tuple(zip(*self._rows)))
    spots = property(lambda self: tuple(c for row in self._rows for c in row))
    def __str__(self):
        return ('\n'+'-'*(len(self.columns)*2-1) + '\n').join(['|'.join(row) for row in self._rows])
    def __repr__(self): return '< Board |'+''.join(self.spots).replace(' ','.')+'| >'
    @property
    def turn(self):
        return 9 - self.spots.count(' ')
    @property
    def whose_turn(self):
        return 'xo'[self.turn % 2]
    def winner(self):
        for c in 'xo':
            for comb in [(0,3,6), (1,4,7), (2,5,8), (0,1,2), (3,4,5), (6,7,8), (0,4,8), (2,4,6)]:
                if all(self.spots[p] == c for p in comb):
                    return c
        return None
    def move(self, pos):
        assert self.spots[pos] == ' '
        new = Board(len(self.rows), len(self.columns))
        new._rows = list(list(row) for row in self.rows)
        new._rows[pos / 3][pos % 3] = self.whose_turn
        return new
    def possible(self):
        return [self.move(p) for p in range(len(self.spots)) if self.spots[p] == ' ']

def opp(c):
    """
    >>> opp('x'), opp('o')
    ('o', 'x')
    """
    return 'x' if c == 'o' else 'o'

def base_case(board, who):
    w = board.winner()
    if w == who: return 1
    if w == opp(who): return -1
    if board.turn == 9: return 0

def recursive_value(board, who='x'):
    """Returns the value of a board
    >>> b = Board(); b._rows = [['x', 'x', 'x'], ['x', 'x', 'x'], ['x', 'x', 'x']]
    >>> recursive_value(b)
    1
    >>> b = Board(); b._rows = [['o', 'o', 'o'], ['o', 'o', 'o'], ['o', 'o', 'o']]
    >>> recursive_value(b)
    -1
    >>> b = Board(); b._rows = [['x', 'o', ' '], ['x', 'o', ' '], [' ', ' ', ' ']]
    >>> recursive_value(b)
    1
    >>> b._rows[0][2] = 'x'
    >>> recursive_value(b)
    -1
    """
    w = board.winner()
    if w == who: return 1
    if w == opp(who): return -1
    if board.turn == 9: return 0
    if who == board.whose_turn: return max([recursive_value(b, who) for b in board.possible()])
    else: return min([recursive_value(b, who) for b in board.possible()])

def iterative_value(board, who='x'):
    """
    >>> b = Board(); b._rows = [['x', 'x', 'x'], ['x', 'x', 'x'], ['x', 'x', 'x']]
    >>> iterative_value(b)
    1
    >>> b = Board(); b._rows = [['o', 'o', 'o'], ['o', 'o', 'o'], ['o', 'o', 'o']]
    >>> iterative_value(b)
    -1
    >>> b = Board(); b._rows = [['x', 'o', ' '], ['x', 'o', ' '], [' ', ' ', ' ']]
    >>> iterative_value(b)
    1
    >>> b._rows[0][2] = 'x'
    >>> iterative_value(b)
    -1
    """

    layer = 0
    index_at_each_layer = {0: 0}
    layers = {0: [board]}
    def current(): return layers[layer][index_at_each_layer[layer]]
    def set_current(val): layers[layer][index_at_each_layer[layer]] = val

    while True:
        r = base_case(current(), who)
        if r is None:
            parent = current()
            layer += 1
            layers[layer] = parent.possible()
            index_at_each_layer[layer] = 0
        else:
            set_current(r)
            while True:
                if index_at_each_layer[layer] < len(layers[layer]) - 1:
                    index_at_each_layer[layer] += 1
                    break
                else:
                    values = layers[layer]
                    if layer == 0:
                        return layers[layer][0]
                    layer -= 1
                    if who == current().whose_turn:
                        set_current(max(values))
                    else:
                        set_current(min(values))

def ai(board, method=iterative_value):
    """
    Returns best next board

    >>> b = Board(); b._rows = [['x', 'o', ' '], ['x', 'o', ' '], [' ', ' ', ' ']]
    >>> ai(b)
    < Board |xo.xo.x..| >
    """
    return sorted([(method(b, who='x'), b) for b in board.possible()])[-1][1]

if __name__ == '__main__':
    import sys
#i did this here because oh I wanted to write a minimax things that wasn't recursive
# so this is finely tuned
    sys.setrecursionlimit(100)
    import doctest
    doctest.testmod()

    b = Board(); b._rows = [['x', 'o', ' '], ['x', 'o', ' '], [' ', ' ', ' ']]
    print "with board"
    print b
    #iterative_value(b)
    print "ai goes here:"
    print ai(b)
