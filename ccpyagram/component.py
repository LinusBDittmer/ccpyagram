"""

This file deals with the drawing of individual components

"""

class Component:

    def __init__(self, indices):
        self.root = None # Root coordinate from which drawing starts
        self.size = None # Width of 4-index comps, ignored otherwise
        self.indices = indices

    def draw(self, **kwargs):
        pass

    def is_connected(self, other):
        return bool(set(self.indices) & set(other.indices))

class Fock(Component):

    def __init__(self, indices):
        super().__init__(indices)

    def draw(self, **kwargs):
        xoffset = kwargs.get('xoffset', 0.0)
        size = kwargs.get('size', self.size)
        s = r"\draw " + f"({root[0]+xoffset}, {root[1]}) -- ({root[0]+xoffset+size}, {root[1]});\n"
        s += r"\draw " + f"({root[0]+xoffset+size}, {root[1]}) node[cross,rotate=45] {};\n"
        return s

class ERI(Component):

    def __init__(self, indices):
        super().__init__(indices)

    def draw(self, **kwargs):
        xoffset = kwargs.get('xoffset', 0.0)
        size = kwargs.get('size', self.size)
        x0 = root[0]+xoffset
        x1 = x0+size
        return r"\draw[dashed] " + f"({x0}, {root[1]}) -- ({x1}, {root[1]});\n"

class Amplitude(Component):

    def __init__(self, indices):
        super().__init__(indices)

    def draw(self, **kwargs):
        xoffset = kwargs.get('xoffset', 0.0)
        size = kwargs.get('size', self.size)
        x0 = root[0]+xoffset
        x1 = x0+size
        return r"\draw " + f"({x0}, {root[1]}) -- ({x1}, {root[1]});\n"


