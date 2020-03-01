import OpenGraph as og
import numpy as np


from OpenGraph.tests import(
    assert_graphs_equal,
    assert_edges_equal,
    assert_nodes_equal
)

def test_HAM():
    g = og.classes.Graph()
    edges0 = [(1, 32), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 11), (1, 12), (1, 13),
              (1, 14), (1, 18), (1, 20), (1, 22), (2, 3), (2, 4), (2, 8), (2, 14), (2, 18), (2, 20), (2, 22), (2, 31),
              (3, 4), (3, 33), (3, 8), (3, 9), (3, 10), (3, 14), (3, 28), (3, 29), (4, 8), (4, 13), (4, 14), (5, 11),
              (5, 7), (6, 7), (6, 11), (6, 17), (7, 17), (9, 31), (9, 34), (9, 33), (10, 34), (14, 34), (15, 33),
              (15, 34), (16, 33), (16, 34), (19, 33), (19, 34), (20, 34), (21, 33), (21, 34), (23, 33), (23, 34),
              (24, 33), (24, 26), (24, 28), (24, 34), (24, 30), (25, 32), (25, 26), (25, 28), (26, 32), (27, 34),
              (27, 30), (28, 34), (29, 32), (29, 34), (30, 33), (30, 34), (31, 34), (31, 33), (32, 33), (32, 34),
              (33, 34), ]

    g.add_edges(edges0)
    ground_truth_labels = [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [1], [1],
                           [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1]]

    # print(ground_truth_labels)
    k = 3  # top-k spanners
    c = len(np.unique(ground_truth_labels))
    k_top, communities = og.functions.structural_holes.get_structural_holes_HAM(g, k, c, ground_truth_labels)
    list_k_top = list(k_top)
    list1 = [3, 20, 9]
    assert_nodes_equal(list_k_top, list1)


def test_MaxD():
    g = og.classes.Graph()
    edges1 = [(1, 2), (2, 3), (1, 3), (3, 4), (4, 5), (4, 6), (5, 6)]
    edges2 = [(3, 7), (4, 7), (10, 7), (11, 7)]
    edges3 = [(8, 9), (8, 10), (9, 10), (10, 11), (11, 12), (11, 13), (12, 13)]
    g.add_edges(edges1)
    g.add_edges(edges2)
    g.add_edges(edges3)

    cmnts = [frozenset([1, 2, 3]), frozenset([4, 5, 6]), frozenset([3, 4, 7, 10, 11]),
             frozenset([8, 9, 10]), frozenset([11, 12, 13])]
    # for edge in g.edges:
    #     print(edge[0],edge[1])

    k = 5  # top-k spanners

    k_top = og.functions.structural_holes.get_structural_holes_MaxD(g, k, cmnts)
    # print(k_top)
    list_k_top = list(k_top)
    list1 = [11, 10, 7, 4, 3]
    assert_nodes_equal(list_k_top, list1)


def test_AP_Greedy():
    g = og.Graph()
    g.add_edge(2, 4)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(2, 5)
    g.add_edge(6, 7)
    g.add_edge(3, 6)

    k_top = og.functions.structural_holes.AP_Greedy(g, k=2)
    list_k_top = list(k_top)
    list1 = [3, 5]
    assert_nodes_equal(list_k_top, list1)


def test_HIS():
    g = og.classes.Graph()
    edges1 = [(1, 2), (2, 3), (1, 3), (3, 4), (4, 5), (4, 6), (5, 6)]
    edges2 = [(3, 7), (4, 7), (10, 7), (11, 7)]
    edges3 = [(8, 9), (8, 10), (9, 10), (10, 11), (11, 12), (11, 13), (12, 13)]
    g.add_edges(edges1)
    g.add_edges(edges2)
    g.add_edges(edges3)

    cmnts = [frozenset([1, 2, 3]), frozenset([4, 5, 6]), frozenset([3, 4, 7, 10, 11]),
             frozenset([8, 9, 10]), frozenset([11, 12, 13])]
    S, I, H = og.functions.structural_holes.get_structural_holes_HIS(g, cmnts, epsilon=0.01)

    mx = 0
    pos = 0
    list_k_top = []
    for node in H:
        print("{}: {}".format(node, H[node][len(S) - 1]))
        if H[node][len(S) - 1] > mx:
            mx =  H[node][len(S) - 1]
            pos = node
        list_k_top.append((node,H[node][len(S) - 1]))
    list_k_top = sorted(list_k_top, key=lambda x: x[1], reverse=True)
    list_k_top = [i[0] for i in list_k_top[0:5]]
    list1 = [7, 3, 4, 10, 11]
    assert_nodes_equal(list_k_top, list1)


def test_modularity_max_detection():

    g = og.Graph()
    edges1 = [(1, 2), (2, 3), (1, 3), (3, 4), (4, 5), (4, 6), (5, 6)]
    g.add_edges(edges1)

    list1 = [1, 2, 3]
    cmmty1 = []
    for j in og.functions.community.greedy_modularity_communities(g)[0]:
        cmmty1.append(j)
    assert_nodes_equal(cmmty1, list1)


def test_pagerank():
    g = og.DiGraph()
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(2, 5)
    g.add_node(6)
    list_k_top = og.functions.not_sorted.pagerank(g, alpha=0.85)
    list1 = []
    for key, item in list_k_top.items():
        list1.append((key, item))
    list_k_top = sorted(list1, key=lambda x: x[1], reverse=True)
    list_k_top = [i[0] for i in list_k_top[0:3]]
    list1 = [5, 4, 3]
    assert_nodes_equal(list_k_top, list1)


