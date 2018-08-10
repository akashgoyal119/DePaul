from collections import defaultdict, deque
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#from test.TestUtil import *
from gabe_versioning import *


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
            self._reversed_active_adjacencies = self.add_edge(m2,m,self._reversed_active_adjacencies)

            self.deactivate_edge(m,m2,edge_type='forward')
            self.deactivate_edge(m2,m,edge_type='reversed')

            # go through this portion of algo in 2 steps (1- forward adjacency, 2-backward adjacency)
            for y in self.active_adjacencies[m]:
                self.deactivate_edge(m,y,edge_type='forward')
                if y in M:
                    y2 = self.get_latest_version(y)
                    self.active_adjacencies = self.add_edge(m2,y2,self.active_adjacencies)
                else:
                    self.active_adjacencies = self.add_edge(m2,y,self.active_adjacencies)

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
        self._reversed_active_adjacencies = self.add_edge(b2,a2,self._reversed_active_adjacencies)

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

def testNext(G,testOpHandle,num):
    tl = TestLine(testOpHandle.readline())
    print('testing op {0} ---> {1}'.format(num,tl.rawLine))
    tl.execute(G)

#ensure that all items in my list are in the graph's list as well
def testGraphValidity(marked,active_adjacencies,inactive_adjacency,graph,versions={}):
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

    if versions and any([graph.R[v] != versions[v] for v in versions]):
        print('Versions in graph do not match versions in assertion')
        for v in versions:
            print('Expected {0} : {1}'.format(v, versions[v]))
            print('Found    {0} : {1}'.format(v, graph.R[v]))
        return False

    return True


if __name__ == '__main__':

    G = Graph()
    testop = 'test op {0} fails because "{1}"'

    with open('test/testCommands2', 'r') as trHandle:
        # Test Op 1
        testNext(G, trHandle,1)
        test_marked_vertices_1 = []
        test_active_adjacencies_1 = {'A1':['P1']}
        test_inactive_adjacencies_1 = {}

        if not testGraphValidity(test_marked_vertices_1,test_active_adjacencies_1,test_inactive_adjacencies_1,G):
            print ('Failure at step 1')
            sys.exit()

        # Test Op 2
        testNext(G, trHandle,2)
        test_marked_vertices_2 = []
        test_active_adjacencies_2 = {'A1':['P1'],
                                      'P1':['B1'],
                                     }
        test_inactive_adjacencies_2 = {}


        if not testGraphValidity(test_marked_vertices_2,test_active_adjacencies_2,test_inactive_adjacencies_2,G):
            print ('Failure at step 2')
            sys.exit()

        # Test Op 3
        testNext(G, trHandle,3)
        test_marked_vertices_3 = []
        test_active_adjacencies_3 = {'A1':['P1'],
                                     'P1':['B1', 'C1'],
                                    }
        test_inactive_adjacencies_3 = {}

        if not testGraphValidity(test_marked_vertices_3,test_active_adjacencies_3,test_inactive_adjacencies_3,G):
            print ('Failure at step 3')
            sys.exit()

        # Test Op 4
        testNext(G, trHandle,4)
        test_marked_vertices_4 = []
        test_active_adjacencies_4 = {'A1':['P1'],
                                     'P1':['B1', 'C1', 'D1'],
                                    }
        test_inactive_adjacencies_4 = {}

        if not testGraphValidity(test_marked_vertices_4,test_active_adjacencies_4,test_inactive_adjacencies_4,G):
            print ('Failure at step 4')
            sys.exit()

        # Test Op 5
        testNext(G, trHandle,5)
        test_marked_vertices_5 = ['A1', 'P1']
        test_active_adjacencies_5 = {'A1':['P1'],
                                     'P1':['B1', 'C1'],
                                    }
        test_inactive_adjacencies_5 = {'P1':['D1']}

        if not testGraphValidity(test_marked_vertices_5,test_active_adjacencies_5,test_inactive_adjacencies_5,G):
            print ('Failure at step 5')
            print (G._reversed_active_adjacencies['P1'])
            sys.exit()

        # Test Op 6
        testNext(G, trHandle,6)
        test_marked_vertices_6 = ['A1', 'P1']
        test_active_adjacencies_6 = {'A1':['P2'],
                                     'E1':['P2'],
                                     'P2':['B1', 'C1'],
                                    }
        test_inactive_adjacencies_6 = {'P1':['D1']}
        versions                    = {'P':['P2', 'P1'],
                                       'B':['B2', 'B1'],
                                       'C':['C1', 'C2'],
                                       'A':['A1'],
                                       'D':['D1'],
                                       'E':['E1']
                                      }

        if not testGraphValidity(test_marked_vertices_6,test_active_adjacencies_6,test_inactive_adjacencies_6,G,
                                 versions=versions):
            print (G.active_adjacencies['A1'])
            print (G.deactivated_adjacencies['A1'])
            print (G._marked_vertices)
            print ('Failure at step 6')
            sys.exit()

        
