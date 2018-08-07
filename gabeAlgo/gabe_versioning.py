from collections import defaultdict, deque
from sys import exit 
import sys

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
        a = a[0]
        if not self.R[a]: self.add_new_version(a)
        return self.R[a][0]

    def add_new_version(self,a):
        a = a[0]
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
        print ('Disconnecting {0} to {1}'.format(a,b))
        self.deactivate_edge(a,b,edge_type='forward')
        self.deactivate_edge(a,b,edge_type='reversed')

        U = self.backward_BFS(a)
        if a not in self._marked_vertices:
            U.append(a)
        for u in U:
            self._marked_vertices[u] = 'marked'

    def connect(self,a,b):
        M = self.forward_BFS(b)
        #print('M after bfs -> {0}'.format(M))
        if b in self._marked_vertices:
            M.append(b)

        for m in M:
            m = m[0]
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
        self.active_adjacencies = self.add_edge(a2,b2,self.active_adjacencies)
        self._reversed_active_adjacencies = self.add_edge(a2,b2,self._reversed_active_adjacencies)

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
    def testNext(testOpHandle,num):
        tl = TestLine(testOpHandle.readline())
        print('testing op {0} ---> {1}'.format(num,tl.rawLine))
        tl.execute(G)

    
    with open('gabe_example', 'r') as trHandle:
        # Test Op 1
        testNext(trHandle,1)
        assert('P1' in G.active_adjacencies['A1']), testop.format(1, 'A does not have active edge to P when it should')
        assert('P1' in G._reversed_active_adjacencies['A1']), testop.format(1,'A does not have reversed active edge to P when it should')
        assert('P1' not in G._marked_vertices), testop.format(1, 'P is marked but should not be marked')
        assert('A1' not in G._marked_vertices), testop.format(1, 'A is marked but should not be marked')
        # Test Op 2
        testNext(trHandle,2)
        assert('P1' not in G.active_adjacencies['A1']), testop.format(2, 'A should no longer have an active edge to P')
        assert('P1' in G.deactivated_adjacencies['A1']), testop.format(2, 'A should have a decativated edge to P')
        assert('A1' in G._marked_vertices), testop.format(2, 'A should be marked')
        assert('P1' not in G._marked_vertices), testop.format(2, 'P should not be marked')
        # Test Op 3
        testNext(trHandle,3)
        assert('B1' in G.active_adjacencies['P1']), testop.format(3, 'P should have an active edge to B')
        assert('P1' not in G._marked_vertices), testop.format(3, 'P is marked but should not be marked')
        assert('B1' not in G._marked_vertices), testop.format(3, 'B is marked but should not be marked')
        # Test Op 4
        testNext(trHandle,4)
        assert('B1' not in G.active_adjacencies['P1']), testop.format(4, 'P should no longer have an active edge to B')
        assert('B1' in G.deactivated_adjacencies['P1']), testop.format(4, 'P should have a decativated edge to B')
        assert('P1' in G._marked_vertices), testop.format(4, 'P should be marked')
        assert('B1' not in G._marked_vertices), testop.format(4, 'B should not be marked')
        # Test Op 5
        testNext(trHandle,5)
        assert('Q1' not in G.active_adjacencies['P1']), testop.format(5, 'P should no longer have an active edge to Q')
        assert('Q1' in G.deactivated_adjacencies['P1']), testop.format(5, 'P should have a deactivated edge to Q')
        assert('A1' in G._marked_vertices), testop.format(5, 'A should be marked')
        assert('P1' in G._marked_vertices), testop.format(5, 'P should be marked')
        assert('B1' not in G._marked_vertices), testop.format(5, 'B should not be marked')
        assert('Q1' not in G._marked_vertices), testop.format(5, 'Q should not be marked')
        # Test Op 6
        testNext(trHandle,6)
        assert('Q1' in G.active_adjacencies['C1']), testop.format(6, 'C does not have active edge to Q when it should')
        assert('Q1' not in G._marked_vertices), testop.format(6, 'Q is marked but should not be marked')
        assert('C1' not in G._marked_vertices), testop.format(6, 'C is marked but should not be marked')
        # Test Op 7
        testNext(trHandle,7)
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
        testNext(trHandle,8)
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
        testNext(trHandle,9)
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


        #ensure that all items in my list are in the graph's list as well
        def testGraphValidity(marked,active_adjacencies,inactive_adjacency,graph):
            # check if all marked vertices in the expected graph are in the actual graph
            for vertex in marked:
                if vertex not in graph._marked_vertices:
                    print (vertex+' was not in marked vertices when it should have been')
                    return False
            # check if all marked vertices in the actual graph are marked in the expected graph
            for vertex in graph._marked_vertices:
                if vertex not in marked:
                    print ('failure- actual vertices were not in expected vertices')
                    return False

            # check if all edges in the expected adjacencies are in the actual adjacencies 
            for adj in active_adjacencies:
                for vertex in active_adjacencies[adj]:
                    
                    if vertex not in graph.active_adjacencies[adj]:
                        print (f'error in edge from {adj} to {vertex}')
                        print (vertex+' was not in active adjacency when it should have')
                        return False

            # check if all edges in the graph's adjacencies are in the expected adjacencies 
            for adj in graph.active_adjacencies:
                for vertex in graph.active_adjacencies[adj]:
                    if vertex not in active_adjacencies[adj]:
                        print ('failure: actual edges were not in expected edges')
                        print (graph.active_adjacencies)
                        print (graph.active_adjacencies[adj],active_adjacencies[adj])
                        return False 

            # FIX THIS TOMORROW 
            # check if all inactive edges in the expected graph are in the actual inactive edge graph
            for adj in inactive_adjacency:
                for vertex in inactive_adjacency[adj]:
                    if vertex not in graph.deactivated_adjacencies[adj]:
                        print (f'failure from edge {adj} to {vertex}')
                        print (vertex+' was not in deactivated_adjacencies when it should have been')
                        return False

            # check if all deactivated edges in the actual graph are in the expected graph
            for adj in graph.deactivated_adjacencies:
                for vertex in graph.deactivated_adjacencies[adj]:
                    if vertex not in inactive_adjacency[adj]:
                        print (f'failure from edge of vertices {adj} to {vertex}')
                        print ('actual deactivated adjacencies not in expected')
                        return False
            return True


        # Test Op 10
        testNext(trHandle,10)
        test_marked_vertices_10 = ['A1','P1','B1','C1']
        test_active_adjacencies_10 = {'P1':['B2']}
        test_inactive_adjacencies_10 = {'A1':['P1'],
                                     'P1':['B1','Q1'],
                                     'B1':['B2','Q1'],
                                     'Q1':[],
                                     'C1':['Q1'],
                                     'B2':[]
                                     }

        if not testGraphValidity(test_marked_vertices_10,test_active_adjacencies_10,test_inactive_adjacencies_10,G):
            print ('Failure at step 10')
            sys.exit()

        # Test Op 11
        testNext(trHandle,11)
        test_marked_vertices_11 = test_marked_vertices_10.copy()
        test_active_adjacencies_11 = {}
        test_inactive_adjacencies_11 = {'A1':['P1'],
                                     'P1':['B1','Q1','B2'],
                                     'B1':['B2','Q1'],
                                     'Q1':[],
                                     'C1':['Q1'],
                                     'B2':[]
                                     }
        if not testGraphValidity(test_marked_vertices_11,test_active_adjacencies_11,test_inactive_adjacencies_11,G):
            print ('Failure at step 11')
            sys.exit()

        # Test Op 12 - P spawn R
        testNext(trHandle,12)
        test_marked_vertices_12 = test_marked_vertices_11.copy()
        test_active_adjacencies_12 = {}
        test_inactive_adjacencies_12 = {'A1':['P1'],
                                     'P1':['B1','Q1','B2','R1'],
                                     'B1':['B2','Q1'],
                                     'Q1':[],
                                     'C1':['Q1'],
                                     'B2':[],
                                     'R1':[]
                                     }
        if not testGraphValidity(test_marked_vertices_12,test_active_adjacencies_12,test_inactive_adjacencies_12,G):
            print ('Failure at step 12')
            sys.exit()

        # Test Op 13- R open E (read)
        testNext(trHandle,13)
        test_marked_vertices_13 = test_marked_vertices_12.copy()
        test_active_adjacencies_13 = {'E1':['R1']}
        test_inactive_adjacencies_13 = test_inactive_adjacencies_12.copy()
        if not testGraphValidity(test_marked_vertices_13,test_active_adjacencies_13,test_inactive_adjacencies_13,G):
            print ('Failure at step 13')
            sys.exit()

        # Test Op 14- R close E (read)
        testNext(trHandle,14)
        test_marked_vertices_14 = ['A1','E1','P1','B1','C1']
        test_active_adjacencies_14 = {}
        test_inactive_adjacencies_14 = test_inactive_adjacencies_13.copy()
        test_inactive_adjacencies_14['E1'] = ['R1']
        if not testGraphValidity(test_marked_vertices_14,test_active_adjacencies_14,test_inactive_adjacencies_14,G):
            print ('Failure at step 14')
            sys.exit()

        # Test Op 15- R open B (read)
        testNext(trHandle,15)
        test_marked_vertices_15 = test_marked_vertices_14.copy()
        test_active_adjacencies_15 = {'B2':['R1']}
        test_inactive_adjacencies_15 = test_inactive_adjacencies_14.copy()
        if not testGraphValidity(test_marked_vertices_15,test_active_adjacencies_15,test_inactive_adjacencies_15,G):
            print ('Failure at step 15')
            sys.exit()

        # Test Op 16- R close B (read)
        testNext(trHandle,16)
        test_marked_vertices_16 = ['A1','E1','P1','B2','B1','C1']
        test_active_adjacencies_16 = {}
        test_inactive_adjacencies_16 = test_inactive_adjacencies_15.copy()
        test_inactive_adjacencies_16['B2'] = ['R1']
        if not testGraphValidity(test_marked_vertices_16,test_active_adjacencies_16,test_inactive_adjacencies_16,G):
            print ('Failure at step 16')
            sys.exit()

        # Test Op 17 - Q open D for write
        testNext(trHandle,17)
        test_marked_vertices_17 = test_marked_vertices_16.copy()
        test_active_adjacencies_17 = {'Q1':['D1']}
        test_inactive_adjacencies_17 = test_inactive_adjacencies_16.copy()
        if not testGraphValidity(test_marked_vertices_17,test_active_adjacencies_17,test_inactive_adjacencies_17,G):
            print ('Failure at step 17')
            sys.exit()

        testNext(trHandle,18)
        test_marked_vertices_18 = ['A1','E1','P1','B2','B1','C1','Q1']
        test_active_adjacencies_18 = {}
        test_inactive_adjacencies_18 = test_inactive_adjacencies_16.copy()
        test_inactive_adjacencies_18['Q1'] = ['D1']
        if not testGraphValidity(test_marked_vertices_18,test_active_adjacencies_18,test_inactive_adjacencies_18,G):
            print ('Failure at step 18')
            sys.exit()

        testNext(trHandle,19)
        test_marked_vertices_19 = test_marked_vertices_18.copy()
        test_active_adjacencies_19 = {'R1':['F1']}
        test_inactive_adjacencies_19 = test_inactive_adjacencies_18.copy()
        if not testGraphValidity(test_marked_vertices_19,test_active_adjacencies_19,test_inactive_adjacencies_19,G):
            print ('Failure at step 19')
            sys.exit()

        testNext(trHandle,20)
        test_marked_vertices_20 = ['A1','E1','P1','B2','B1','C1','Q1','R1']
        test_active_adjacencies_20 = {}
        test_inactive_adjacencies_20 = test_inactive_adjacencies_19.copy()
        test_inactive_adjacencies_20['R1'] = ['F1']
        if not testGraphValidity(test_marked_vertices_20,test_active_adjacencies_20,test_inactive_adjacencies_20,G):
            print ('Failure at step 20')
            sys.exit()
