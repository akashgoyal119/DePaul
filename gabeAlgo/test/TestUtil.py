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

def testNext(G, testOpHandle,num):
    tl = TestLine(testOpHandle.readline())
    print('testing op {0} ---> {1}'.format(num,tl.rawLine))
    tl.execute(G)

def testGraphValidity(marked,active_adjacencies,inactive_adjacency,graph, versions={}):
    # check if all marked vertices in the expected graph are in the actual graph
    for vertex in marked:
        if vertex not in graph._marked_vertices:
            print (vertex+' was not in marked vertices when it should have been')
            return False
    # check if all marked vertices in the actual graph are marked in the expected graph
    for vertex in graph._marked_vertices:
        if vertex not in marked:
            print ('failure- actual vertices were not in expected vertices')
            print ('Actual     : {0}'.format(graph._marked_vertices.keys()))
            print ('Expected   : {0}'.format(marked))
            return False

    # check if all edges in the expected adjacencies are in the actual adjacencies
    for adj in active_adjacencies:
        for vertex in active_adjacencies[adj]:
            if vertex not in graph.active_adjacencies[adj]:
                print ('error in edge from {0} to {1}'.format(adj, vertex))
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
                print ('failure from edge {0} to {1}'.format(adj, vertex))
                print (vertex+' was not in deactivated_adjacencies when it should have been')
                return False

    # check if all deactivated edges in the actual graph are in the expected graph
    for adj in graph.deactivated_adjacencies:
        for vertex in graph.deactivated_adjacencies[adj]:
            if vertex not in inactive_adjacency[adj]:
                print ('failure from edge of vertices {0} to {1}'.format(adj, vertex))
                print ('actual deactivated adjacencies not in expected')
                return False

    # check that we have the correct set of versions for each versioned object
    if versions and any([graph.R[v] != versions[v] for v in versions]):
        print('Versions in graph do not match versions in assertion')
        for v in versions:
            print('Expected {0} : {1}'.format(v, versions[v]))
            print('Found    {0} : {1}'.format(v, graph.R[v]))
        return False

    return True
