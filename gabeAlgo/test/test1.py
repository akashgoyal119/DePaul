import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from test.TestUtil import *
from gabe_versioning import *
from collections import deque

G = Graph()
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
        sys.exit()

    # Test Op 6
    testNext(G, trHandle,6)
    test_marked_vertices_6 = ['A1', 'P1']
    test_active_adjacencies_6 = {'A1':['P2'],
                                 'E1':['P2'],
                                 'P2':['B1', 'C1'],
                                 }
    test_inactive_adjacencies_6 = {
                                   'A1':['P1'],
                                   'P1':['B1', 'C1', 'D1', 'P2'],
                                  }
    versions                    = {
                                   'A':deque(['A1']),
                                   'B':deque(['B1']),
                                   'C':deque(['C1']),
                                   'D':deque(['D1']),
                                   'E':deque(['E1']),
                                   'P':deque(['P2', 'P1']),
                                  }

    if not testGraphValidity(test_marked_vertices_6,test_active_adjacencies_6,test_inactive_adjacencies_6,G, versions=versions):
        print ('Failure at step 6')
        sys.exit()

    # Test Op 7
    testNext(G, trHandle,7)
    test_marked_vertices_7 = ['A1', 'P1']
    test_active_adjacencies_7 = {'A1':['P2'],
                                 'D1':['P2'],
                                 'E1':['P2'],
                                 'P2':['B1', 'C1'],
                                }
    test_inactive_adjacencies_7 = {
                                   'A1':['P1'],
                                   'P1':['B1', 'C1', 'D1', 'P2'],
                                  }
    versions                    = {
                                   'A':deque(['A1']),
                                   'B':deque(['B1']),
                                   'C':deque(['C1']),
                                   'D':deque(['D1']),
                                   'E':deque(['E1']),
                                   'P':deque(['P2', 'P1']),
                                  }

    if not testGraphValidity(test_marked_vertices_7,test_active_adjacencies_7,test_inactive_adjacencies_7,G, versions=versions):
        print ('Failure at step 7')
        sys.exit()

    # Test Op 8
    testNext(G, trHandle,8)
    test_marked_vertices_8 = ['A1', 'P1']
    test_active_adjacencies_8 = {'A2':['P2'],
                                 'D1':['P2'],
                                 'E1':['P2'],
                                 'P2':['B1', 'C1'],
                                 'Z1':['A2'],
                                }
    test_inactive_adjacencies_8 = {
                                   'A1':['A2', 'P1', 'P2'],
                                   'P1':['B1', 'C1', 'D1', 'P2'],
                                  }
    versions                    = {
                                   'A':deque(['A2', 'A1']),
                                   'B':deque(['B1']),
                                   'C':deque(['C1']),
                                   'D':deque(['D1']),
                                   'E':deque(['E1']),
                                   'P':deque(['P2', 'P1']),
                                   'Z':deque(['Z1']),
                                  }

    if not testGraphValidity(test_marked_vertices_8,test_active_adjacencies_8,test_inactive_adjacencies_8,G, versions=versions):
        print ('Failure at step 8')
        sys.exit()

    # Test Op 9
    testNext(G, trHandle,9)
    test_marked_vertices_9 = ['A1', 'A2', 'D1', 'E1', 'P1', 'P2', 'Z1']
    test_active_adjacencies_9 = {'A2':['P2'],
                                 'D1':['P2'],
                                 'E1':['P2'],
                                 'P2':['B1'],
                                 'Z1':['A2'],
                                }
    test_inactive_adjacencies_9 = {
                                   'A1':['A2', 'P1', 'P2'],
                                   'P1':['B1', 'C1', 'D1', 'P2'],
                                   'P2':['C1']
                                  }
    versions                    = {
                                   'A':deque(['A2', 'A1']),
                                   'B':deque(['B1']),
                                   'C':deque(['C1']),
                                   'D':deque(['D1']),
                                   'E':deque(['E1']),
                                   'P':deque(['P2', 'P1']),
                                   'Z':deque(['Z1']),
                                  }

    if not testGraphValidity(test_marked_vertices_9,test_active_adjacencies_9,test_inactive_adjacencies_9,G, versions=versions):
        print ('Failure at step 9')
        sys.exit()

    # Test Op 10
    testNext(G, trHandle,10)
    test_marked_vertices_10 = ['A1', 'A2', 'D1', 'E1', 'P1', 'P2', 'Z1']
    test_active_adjacencies_10 = {'A2':['P3'],
                                  'C1':['P3'],
                                  'D1':['P3'],
                                  'E1':['P3'],
                                  'P3':['B1'],
                                  'Z1':['A2'],
                                 }
    test_inactive_adjacencies_10 = {
                                    'A1':['A2', 'P1', 'P2'],
                                    'A2':['P2'],
                                    'D1':['P2'],
                                    'E1':['P2'],
                                    'P1':['B1', 'C1', 'D1', 'P2'],
                                    'P2':['B1', 'C1', 'P3']
                                   }
    versions                     = {
                                    'A':deque(['A2', 'A1']),
                                    'B':deque(['B1']),
                                    'C':deque(['C1']),
                                    'D':deque(['D1']),
                                    'E':deque(['E1']),
                                    'P':deque(['P3', 'P2', 'P1']),
                                    'Z':deque(['Z1']),
                                   }

    if not testGraphValidity(test_marked_vertices_10,test_active_adjacencies_10,test_inactive_adjacencies_10,G,
                             versions=versions):
        print ('Failure at step 10')
        sys.exit()

    # Test Op 11
    testNext(G, trHandle,11)
    test_marked_vertices_11 = ['A1', 'A2', 'C1', 'D1', 'E1', 'P1', 'P2', 'P3', 'Z1']
    test_active_adjacencies_11 = {'A2':['P3'],
                                  'C1':['P3'],
                                  'D1':['P3'],
                                  'E1':['P3'],
                                  'P3':['B1'],
                                  'Z1':['A2'],
                                 }
    test_inactive_adjacencies_11 = {
                                    'A1':['A2', 'P1', 'P2'],
                                    'A2':['P2'],
                                    'D1':['P2'],
                                    'E1':['P2'],
                                    'P1':['B1', 'C1', 'D1', 'P2'],
                                    'P2':['B1', 'C1', 'P3'],
                                    'P3':['Q1']
                                   }
    versions                     = {
                                    'A':deque(['A2', 'A1']),
                                    'B':deque(['B1']),
                                    'C':deque(['C1']),
                                    'D':deque(['D1']),
                                    'E':deque(['E1']),
                                    'P':deque(['P3', 'P2', 'P1']),
                                    'Q':deque(['Q1']),
                                    'Z':deque(['Z1']),
                                   }

    if not testGraphValidity(test_marked_vertices_11,test_active_adjacencies_11,test_inactive_adjacencies_11,G,
                             versions=versions):
        print ('Failure at step 11')
        sys.exit()

    # Test Op 12
    testNext(G, trHandle,12)
    test_marked_vertices_12 = ['A1', 'A2', 'C1', 'D1', 'E1', 'P1', 'P2', 'P3', 'Z1']
    test_active_adjacencies_12 = {
                                  'C1':['P3'],
                                  'D1':['P3'],
                                  'E1':['P3'],
                                  'P3':['B1'],
                                  'Z1':['A2'],
                                 }
    test_inactive_adjacencies_12 = {
                                    'A1':['A2', 'P1', 'P2'],
                                    'A2':['P2', 'P3'],
                                    'D1':['P2'],
                                    'E1':['P2'],
                                    'P1':['B1', 'C1', 'D1', 'P2'],
                                    'P2':['B1', 'C1', 'P3'],
                                    'P3':['Q1']
                                   }
    versions                     = {
                                    'A':deque(['A2', 'A1']),
                                    'B':deque(['B1']),
                                    'C':deque(['C1']),
                                    'D':deque(['D1']),
                                    'E':deque(['E1']),
                                    'P':deque(['P3', 'P2', 'P1']),
                                    'Q':deque(['Q1']),
                                    'Z':deque(['Z1']),
                                   }

    if not testGraphValidity(test_marked_vertices_12,test_active_adjacencies_12,test_inactive_adjacencies_12,G,
                             versions=versions):
        print ('Failure at step 11')
        sys.exit()
