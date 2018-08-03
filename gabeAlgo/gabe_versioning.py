from collections import defaultdict, deque
from sys import exit 

class Graph:
    def __init__(self):
        '''
        Adjacency has the key as vertex X, and the values as the list of outgoing vertices (i.e. x --> y).
        Reversed adjacencies also has key as vertex X, and the values as the list of incoming vertices (i.e. y --> x)
        '''
        self.active_adjacencies = defaultdict(list)
        self.deactivated_adjacencies = defaultdict(list)
        self._reversed_active_adjacencies = defaultdict(list)
        self._reversed_deactivated_adjacencies = defaultdict(list)
        self._marked_vertices = {}
        self.R = defaultdict(deque)

    def get_latest_version(self,a):
        if not self.R[a]: self.add_new_version(a)
        return self.R[a][0]

    def add_new_version(self,a):
        print('Adding {0} to {1}'.format(a, self.R[a]))
        self.R[a].appendleft(a + str(len(self.R[a]) + 1))

    def open_read(self,p, f):
        self.connect(self.get_latest_version(f), self.get_latest_version(p))

    def close_read(self,p, f):
        self.disconnect(self.get_latest_version(f), self.get_latest_version(p))

    def open_write(self,p, f):
        self.connect(self.get_latest_version(p), self.get_latest_version(f))

    def close_write(self,p, f):
        self.disconnect(self.get_latest_version(p), self.get_latest_version(f))

    def open_read_write(self,p, f):
        self.connect(self.get_latest_version(f), self.get_latest_version(p))
        self.connect(self.get_latest_version(p), self.get_latest_version(f))

    def close_read_write(self,p, f):
        self.disconnect(self.get_latest_version(f), self.get_latest_version(p))
        self.disconnect(self.get_latest_version(p), self.get_latest_version(f))

    def spawn(self,p, c):
        self.connect(self.get_latest_version(p), self.get_latest_version(c))
        self.disconnect(self.get_latest_version(p), self.get_latest_version(c))

    # from node u to node v, D is the dictionary
    @staticmethod
    def add_edge(u,v,D):
        if not D.get(u):
            D[u] = [v]
        else:
            D[u].append(v)
        return D

    def deactivate_edge(self,u,v,edge_type='forward'):
        if edge_type == 'forward':
            self.active_adjacencies[u] = [node for node in self.active_adjacencies[u] if node!=v]
            self.deactivated_adjacencies = self.add_edge(u,v,self.deactivated_adjacencies)
        elif edge_type == 'reversed':
            self._reversed_active_adjacencies[u] = [node for node in self._reversed_active_adjacencies[u] if node!=v]
            self._reversed_deactivated_adjacencies = self.add_edge(u,v,self._reversed_deactivated_adjacencies)
        else:
            raise Exception ("edge_type option: '{0}' not available. Please choose either forward or reversed".format(edge_type))

    # The Q is used to traverse the graph, and the marking indicates whether a file has been read or written to
    # before, and NOT whether this node has already been traversed in the given function. This distinction
    # is important to note
    def forward_BFS(self,s):
        q = []
        q.append(s)
        previously_marked_vertices = []
        while q:
            s = q.pop(0)
            for adjacent_vertex in self.active_adjacencies[s]:
                if adjacent_vertex not in q:
                    q.append(adjacent_vertex)
                    if adjacent_vertex in self._marked_vertices:
                        previously_marked_vertices.append(adjacent_vertex)

        return previously_marked_vertices

    def backward_BFS(self,s):
        q = []
        q.append(s)
        unmarked_vertices = []
        while q:
            s = q.pop(0)
            for adjacent_vertex in self._reversed_active_adjacencies[s]:
                if adjacent_vertex not in q:
                    q.append(adjacent_vertex)
                    if adjacent_vertex not in self._marked_vertices:
                        unmarked_vertices.append(adjacent_vertex)
        return unmarked_vertices

    def disconnect(self,a,b):
        self.deactivate_edge(a,b,edge_type='forward')
        self.deactivate_edge(a,b,edge_type='reversed')

        U = self.backward_BFS(a)
        if a not in self._marked_vertices:
            U.append(a)
        for u in U:
            self._marked_vertices[u] = 'marked'

    def connect(self,a,b):
        print('Connecting {0} to {1}'.format(a, b))
        M = self.forward_BFS(b)
        print('M after bfs -> {0}'.format(M))
        if b in self._marked_vertices:
            print(self._marked_vertices)
            M.append(b)

        for m in M:
            self.add_new_version(m)

        for m in M:
            m2 = self.get_latest_version(m)
            self.active_adjacencies = self.add_edge(m,m2,self.active_adjacencies)
            self._reversed_active_adjacencies = self.add_edge(m,m2,self._reversed_active_adjacencies)

            self.deactivate_edge(m,m2,edge_type='forward')
            self.deactivate_edge(m,m2,edge_type='reversed')

            # go through this portion of algo in 2 steps (1- forward adjacency, 2-backward adjacency)
            for y in self.active_adjacencies[m]:
                self.deactivate_edge(m,y,edge_type='forward')
                if y in M:
                    y2 = self.get_latest_version(y)
                    self.active_adjacencies = self.add_edge(m2,y2)
                else:
                    self.active_adjacencies = self.add_edge(m2,y)

            for x in self._reversed_active_adjacencies[m]:
                self.deactivate_edge(m,x,edge_type='reversed')
                if x in M:
                    x2 = self.get_latest_version(x)
                    self._reversed_active_adjacencies = self.add_edge(m2,x2,self._reversed_active_adjacencies)
                else:
                    self._reversed_active_adjacencies = self.add_edge(m2,x,self._reversed_active_adjacencies)

        a2 = a
        if a in M:
            a2 = self.get_latest_version(a)

        b2 = b
        if b in M:
            b2 = self.get_latest_version(b)
        self.active_adjacencies = self.add_edge(a,b,self.active_adjacencies)
        self._reversed_active_adjacencies = self.add_edge(a,b,self._reversed_active_adjacencies)

if __name__ == '__main__':
    #pass
    # WRITE OUT EXAMPLE CASE
    class TestLine(object):
        def __init__(self, rawLine):
            self.rawLine = rawLine.strip()
            tokens       = self.rawLine.split()
            self.subject = tokens[0]
            self.verb    = tokens[1]
            self.object  = tokens[2]
            self.modi    = tokens[3] if len(tokens) > 3 else ''

        def execute(self, G):
            cases = {
                    'openread':G.open_read,
                    'closeread': G.close_read,
                    'openwrite':G.open_write,
                    'closewrite':G.close_write,
                    'openreadwrite':G.open_read_write,
                    'closereadwrite':G.close_read_write,
                    'spawn':G.spawn,
                    }

            cases[self.verb + self.modi](self.subject, self.object)
#self.active_adjacencies = {}
#self.deactivated_adjacencies = {}
#self._reversed_active_adjacencies = {}
#self._reversed_deactivated_adjacencies = {}
#self._marked_vertices = {}
    G      = Graph()
    testop = 'test op {0} fails because "{1}"'
    def testNext(testOpHandle):
        tl = TestLine(testOpHandle.readline())
        print('testing op ---> {0}'.format(tl.rawLine))
        tl.execute(G)

    with open('gabes20', 'r') as trHandle:
        # Test Op 1
        testNext(trHandle)
        assert('P1' in G.active_adjacencies['A1']), testop.format(1, 'A does not have active edge to P when it should')
        assert('P1' not in G._marked_vertices), testop.format(1, 'P is marked but should not be marked')
        assert('A1' not in G._marked_vertices), testop.format(1, 'A is marked but should not be marked')
        # Test Op 2
        testNext(trHandle)
        assert('P1' not in G.active_adjacencies['A1']), testop.format(2, 'A should no longer have an active edge to P')
        assert('P1' in G.deactivated_adjacencies['A1']), testop.format(2, 'A should have a decativated edge to P')
        assert('A1' in G._marked_vertices), testop.format(2, 'A should be marked')
        assert('P1' not in G._marked_vertices), testop.format(2, 'P should not be marked')
        # Test Op 3
        testNext(trHandle)
        assert('B1' in G.active_adjacencies['P1']), testop.format(3, 'P should have an active edge to B')
        assert('P1' not in G._marked_vertices), testop.format(3, 'P is marked but should not be marked')
        assert('B1' not in G._marked_vertices), testop.format(3, 'B is marked but should not be marked')
        # Test Op 4
        testNext(trHandle)
        assert('B1' not in G.active_adjacencies['P1']), testop.format(4, 'P should no longer have an active edge to B')
        assert('B1' in G.deactivated_adjacencies['P1']), testop.format(4, 'P should have a decativated edge to B')
        assert('P1' in G._marked_vertices), testop.format(4, 'P should be marked')
        assert('B1' not in G._marked_vertices), testop.format(4, 'B should not be marked')
        # Test Op 5
        testNext(trHandle)
        assert('Q1' not in G.active_adjacencies['P1']), testop.format(5, 'P should no longer have an active edge to Q')
        assert('Q1' in G.deactivated_adjacencies['P1']), testop.format(5, 'P should have a deactivated edge to Q')
        assert('A1' in G._marked_vertices), testop.format(5, 'A should be marked')
        assert('P1' in G._marked_vertices), testop.format(5, 'P should be marked')
        assert('B1' not in G._marked_vertices), testop.format(5, 'B should not be marked')
        assert('Q1' not in G._marked_vertices), testop.format(5, 'Q should not be marked')
        # Test Op 6
        testNext(trHandle)
        assert('Q1' in G.active_adjacencies['C1']), testop.format(6, 'C does not have active edge to Q when it should')
        assert('Q1' not in G._marked_vertices), testop.format(6, 'Q is marked but should not be marked')
        assert('C1' not in G._marked_vertices), testop.format(6, 'C is marked but should not be marked')
        # Test Op 7
        testNext(trHandle)
        assert('Q1' not in G.active_adjacencies['C1']), testop.format(7, 'C should no longer have an active edge to Q')
        assert('Q1' not in G.active_adjacencies['P1']), testop.format(7, 'C should not have an active edge to Q')
        assert('Q1' in G.deactivated_adjacencies['C1']), testop.format(7, 'C should have a decativated edge to Q')
        assert('Q1' in G.deactivated_adjacencies['P1']), testop.format(7, 'P should have a decativated edge to Q')
        assert('C1' in G._marked_vertices), testop.format(7, 'C should be marked')
        assert('A1' in G._marked_vertices), testop.format(7, 'A should be marked')
        assert('P1' in G._marked_vertices), testop.format(7, 'P should be marked')
        assert('B1' not in G._marked_vertices), testop.format(7, 'B should not be marked')
        assert('Q1' not in G._marked_vertices), testop.format(7, 'Q should not be marked')
        # Test Op 8
        testNext(trHandle)
        assert('Q1' in G.active_adjacencies['B1']), testop.format(8, 'B should have an active adjacency to Q')
        assert('Q1' not in G.active_adjacencies['C1']), testop.format(8, 'C should no longer have an active edge to Q')
        assert('Q1' not in G.active_adjacencies['P1']), testop.format(8, 'C should not have an active edge to Q')
        assert('Q1' in G.deactivated_adjacencies['C1']), testop.format(8, 'C should have a decativated edge to Q')
        assert('Q1' in G.deactivated_adjacencies['P1']), testop.format(8, 'P should have a decativated edge to Q')
        assert('C1' in G._marked_vertices), testop.format(8, 'C should be marked')
        assert('A1' in G._marked_vertices), testop.format(8, 'A should be marked')
        assert('P1' in G._marked_vertices), testop.format(8, 'P should be marked')
        assert('B1' not in G._marked_vertices), testop.format(8, 'B should not be marked')
        assert('Q1' not in G._marked_vertices), testop.format(8, 'Q should not be marked')
        # Test Op 9
        testNext(trHandle)
        assert('Q1' not in G.active_adjacencies['B1']), testop.format(9, 'B should not have an active adjacency to Q')
        assert('Q1' in G.deactivated_adjacencies['B1']), testop.format(9, 'B should not have an active adjacency to Q')
        assert('Q1' not in G.active_adjacencies['C1']), testop.format(9, 'C should no longer have an active edge to Q')
        assert('Q1' not in G.active_adjacencies['P1']), testop.format(9, 'C should not have an active edge to Q')
        assert('Q1' in G.deactivated_adjacencies['C1']), testop.format(9, 'C should have a decativated edge to Q')
        assert('Q1' in G.deactivated_adjacencies['P1']), testop.format(9, 'P should have a decativated edge to Q')
        assert('C1' in G._marked_vertices), testop.format(9, 'C should be marked')
        assert('A1' in G._marked_vertices), testop.format(9, 'A should be marked')
        assert('P1' in G._marked_vertices), testop.format(9, 'P should be marked')
        assert('B1' in G._marked_vertices), testop.format(9, 'B should be marked')
        assert('Q1' not in G._marked_vertices), testop.format(9, 'Q should not be marked')
        # Test Op 10
        testNext(trHandle)
        print(G.R)
        bVer = G.get_latest_version('B')
        assert(bVer == 'B2'), testop.format(10, 'B2 should be the latest version not {0}'.format(bVer))
