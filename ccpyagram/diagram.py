"""

This class represents the internal structure of a diagram

"""

from ccpyagram import Fock, ERI, Amplitude, Component

GLOBAL_ROOT = (0., 0.)
GRIDSIZE = (1., 1.)
INIT_WIDTH = 1.

def longest_path(graph, n):
    def dfs(current_node, current_length):
        nonlocal max_length
        # Base case: if current_node == n, update max_length
        if current_node == n:
            max_length = max(max_length, current_length)
            return
        
        # Recursive case: visit each neighbor
        visited.add(current_node)
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                dfs(neighbor, current_length + 1)
        
        # Backtrack: remove current_node from visited
        visited.remove(current_node)
    
    max_length = 0
    visited = set()
    dfs(0, 0)
    return max_length

def gen_depth_array(components, connections):
    # The user has to specify the components in the order
    # they appear up -> down. This allows for the construction
    # of a trivial depth array, which can then be shortened by
    # checking if any component on depth n has connections to components on depth n-1

    depth = list(range(len(components)))
    changes = True # Whether changes happen during an iteration
    while changes:
        changes = False
        for comp_index, comp in enumerate(components):
            current_depth = depth[comp_index]
            # Skip base layer, no simplification possible
            if current_depth == 0: continue
            # Indices of all components directly above the current component
            layer_above = [i for i in range(components) if depth[i] == current_depth-1]
            if len(layer_above) == 0: # Missing layer -> reduce depth
                depth[comp_index] -= 1
                changes = True
            # Check if all components above are disconnected from this component
            disconnected = [not comp.is_connected(components[i]) for i in layer_above]
            if all(disconnected):
                depth[comp_index] -= 1
                changes = True
    return depth

def gen_connections(components):
    conn_list = []
    for i, comp1 in enumerate(components):
        conns = []
        for j, comp2 in enumerate(components):
            if i == j: continue
            if comp1.is_connected(comp2):
                conns.append(j)
        conn_list.append(tuple(conns))
    return tuple(conn_list)

class Diagram:

    def __init__(self, *components):
        if components is not None:
            self.components = list(components)
            self.validate_components()
        else:
            self.components = list()

    def add_component(self, comptype, *indices):
        if comptype not in ('f', 'V', 't1'):
            raise NotImplementedError(f'Only f, V, t1 implemented, not {comptype}.')
        if comptype == 'f' and len(indices) != 2:
            raise ValueError(f'Incorrect number of indices for Fock matrix. ' 
                             +'Required 2, received {len(indices)}')
        elif comptype in ('V', 't1') and len(indices) != 4:
            raise ValueError(f'Incorrect number of indices for ERI/t1. ' 
                             +'Required 4, received {len(indices)}')

        if comptype == 'f':
            f = Fock(tuple(indices))
            self.components.append(f)
        elif comptype == 'V':
            v = ERI(tuple(indices))
            self.components.append(v)
        else:
            t = Amplitude(tuple(indices))
            self.components.append(t)
   
    def align_components(self):
        root_comp = self.components[0]
        # Grounding the root, i. e. the first added component
        root_comp.root = GLOBAL_ROOT
        root_ocmp.size = INIT_WIDTH
        
        connections = gen_connections(self.components)
        depth_array = gen_depth_array(self.components, connections)
        
        # Initialising y coordinates 
        for i, component in enumerate(self.components):
            y = GLOBAL_ROOT[1] + GRIDSIZE * depth_array[i]
            component.root = [0., y]

        # Determining the x coordinates:
        # We first determine the max number of components per area.
        # On that layer, each component has a spacing of GRIDSIZE
        max_depth = max(depth_array)
        depth_num = [len([d for d in depth_array if d == depth]) for depth in range(max_depth+1)]
        max_comps = max(depth_num)
        # 2n-1 results from the fact that we count both components and spaces
        spacing_factor = [round(float(2*max_comps-1) / (2*dn-1), 2) for dn in depth_num]
       
        counters = [0] * (max(depth_array)+1)
        for i, component in enumerate(self.components):
            depth = depth_array[i]
            offset = round(counters[depth] * 2 * spacing_factor[depth], 2)
            component.size = GRIDSIZE * spacing_factor[depth]
            component.root[0] = GLOBAL_ROOT[0] + GRIDSIZE * offset

    def draw_connections(self):
        pass

    def draw(self):
        self.align_components()

        drawstr = ""
        for component in self.components:
            drawstr += component.draw()

        self.draw_connections()
