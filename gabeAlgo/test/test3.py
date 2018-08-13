import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from test.TestUtil import *
from gabe_versioning import *
from collections import deque

G = Graph()
with open('test/testCommands3', 'r') as trHandle:

    # Test Op 1
    testNext(G, trHandle,1)
    test_marked_vertices_1 = []
    test_active_adjacencies_1 = {'P1':['B1']}
    test_inactive_adjacencies_1 = {}

    if not testGraphValidity(test_marked_vertices_1,test_active_adjacencies_1,test_inactive_adjacencies_1,G):
        print ('Failure at step 1')
        sys.exit()

    # Test Op 2
    testNext(G, trHandle,2)
    test_marked_vertices_2 = []
    test_active_adjacencies_2 = {
                                 'A1':['P1'],
                                 'P1':['B1'],
                                 }
    test_inactive_adjacencies_2 = {}

    if not testGraphValidity(test_marked_vertices_2,test_active_adjacencies_2,test_inactive_adjacencies_2,G):
        print ('Failure at step 2')
        sys.exit()

    # Test Op 3
    testNext(G, trHandle,3)
    test_marked_vertices_3 = []
    test_active_adjacencies_3 = {
                                 'A1':['P1'],
                                 'P1':['B1'],
                                 'Q1':['A1'],
                                 }
    test_inactive_adjacencies_3 = {}

    if not testGraphValidity(test_marked_vertices_3,test_active_adjacencies_3,test_inactive_adjacencies_3,G):
        print ('Failure at step 3')
        sys.exit()

    # Test Op 4
    testNext(G, trHandle,4)
    test_marked_vertices_4 = ['A1', 'P1', 'Q1']
    test_active_adjacencies_4 = {
                                 'A1':['P1'],
                                 'Q1':['A1'],
                                 }
    test_inactive_adjacencies_4 = {
                                   'P1':['B1'],
                                  }

    if not testGraphValidity(test_marked_vertices_4,test_active_adjacencies_4,test_inactive_adjacencies_4,G):
        print ('Failure at step 4')
        sys.exit()

    # Test Op 5
    testNext(G, trHandle,5)
    test_marked_vertices_5 = ['A1', 'P1', 'Q1']
    test_active_adjacencies_5 = {
                                 'A2':['P2'],
                                 'Q1':['A2'],
                                 'Z1':['A2'],
                                }
    test_inactive_adjacencies_5 = {
                                   'A1':['A2', 'P1'],
                                   'P1':['B1', 'P2'],
                                   'Q1':['A1'],
                                  }
    versions                    = {
                                   'A':deque(['A2', 'A1']),
                                   'B':deque(['B1']),
                                   'P':deque(['P2', 'P1']),
                                   'Q':deque(['Q1']),
                                   'Z':deque(['Z1']),
                                  }
    if not testGraphValidity(test_marked_vertices_5,test_active_adjacencies_5,test_inactive_adjacencies_5,G):
        print ('Failure at step 5')
        sys.exit()

    # Test Op 6
#    testNext(G, trHandle,6)
#    test_marked_vertices_6 = ['A1', 'P1']
#    test_active_adjacencies_6 = {'A1':['P2'],
#                                 'E1':['P2'],
#                                 'P2':['B1', 'C1'],
#                                 }
#    test_inactive_adjacencies_6 = {
#                                   'A1':['P1'],
#                                   'P1':['B1', 'C1', 'D1', 'P2'],
#                                  }
#    versions                    = {
#                                   'A':deque(['A1']),
#                                   'B':deque(['B1']),
#                                   'C':deque(['C1']),
#                                   'D':deque(['D1']),
#                                   'E':deque(['E1']),
#                                   'P':deque(['P2', 'P1']),
#                                  }
