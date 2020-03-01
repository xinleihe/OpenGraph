import OpenGraph as og
from OpenGraph.tests import(
    assert_graphs_equal,
    assert_edges_equal,
    assert_nodes_equal
)

def test_passing():
    assert (1, 2, 3) == (1, 2, 3)


# thanks to numpy for this GenericTest class (numpy/testing/test_utils.py)


class _GenericTest:
    @classmethod
    def _test_equal(cls, a, b):
        cls._assert_func(a, b)

    @classmethod
    def _test_not_equal(cls, a, b):
        try:
            cls._assert_func(a, b)
            passed = True
        except AssertionError:
            pass
        else:
            raise AssertionError("a and b are found equal but are not")


# def test_equal1():
#     G = og.classes.Graph()
#     G.add_nodes([1, 2, 3])
#     H = og.classes.Graph()
#     H.add_nodes([1, 2, 3])
#     #assert G == H

class TestNodesEqual(_GenericTest):
    _assert_func = assert_nodes_equal

    def test_nodes_equal(self):
        a = [1, 2, 5, 4]
        b = [4, 5, 1, 2]
        self._test_equal(a, b)

    def test_nodes_not_equal(self):
        a = [1, 2, 5, 4]
        b = [4, 5, 1, 3]
        self._test_not_equal(a, b)

    def test_nodes_with_data_equal(self):
        G = og.Graph()
        G.add_nodes([1, 2, 3])
        H = og.Graph()
        H.add_nodes([1, 2, 3])
        self._test_equal(G.nodes, H.nodes)

    def test_edges_with_data_not_equal(self):
        G = og.Graph()
        G.add_nodes([1, 2, 3])
        H = og.Graph()
        H.add_nodes([1, 4, 3])
        self._test_not_equal(G.nodes, H.nodes)

class TestEdgesEqual(_GenericTest):
    _assert_func = assert_edges_equal

    def test_edges_equal(self):
        a = [(1, 2), (5, 4)]
        b = [(4, 5), (1, 2)]
        self._test_equal(a, b)

    def test_edges_not_equal(self):
        a = [(1, 2), (5, 4)]
        b = [(4, 5), (1, 3)]
        self._test_not_equal(a, b)

    def test_duplicate_edges(self):
        a = [(1, 2), (5, 4), (1, 2)]
        b = [(4, 5), (1, 2)]
        self._test_not_equal(a, b)

    def test_duplicate_edges_with_data(self):
        a = [(1, 2, {'weight': 10}), (5, 4), (1, 2, {'weight': 1})]
        b = [(4, 5), (1, 2), (1, 2, {'weight': 1})]
        self._test_not_equal(a, b)

    def test_order_of_edges_with_data(self):
        a = [(1, 2, {'weight': 10}), (1, 2, {'weight': 1})]
        b = [(1, 2, {'weight': 1}), (1, 2, {'weight': 10})]
        self._test_equal(a, b)

    def test_order_of_multiedges(self):
        wt1 = {'weight': 1}
        wt2 = {'weight': 2}
        a = [(1, 2, wt1), (1, 2, wt1), (1, 2, wt2)]
        b = [(1, 2, wt1), (1, 2, wt2), (1, 2, wt2)]
        self._test_not_equal(a, b)

    def test_order_of_edges_with_keys(self):
        a = [(1, 2, 0, {'weight': 10}), (1, 2, 1, {'weight': 1}), (1, 2, 2)]
        b = [(1, 2, 1, {'weight': 1}), (1, 2, 2), (1, 2, 0, {'weight': 10})]
        self._test_equal(a, b)
        a = [(1, 2, 1, {'weight': 10}), (1, 2, 0, {'weight': 1}), (1, 2, 2)]
        b = [(1, 2, 1, {'weight': 1}), (1, 2, 2), (1, 2, 0, {'weight': 10})]
        self._test_not_equal(a, b)

class TestGraphsEqual(_GenericTest):
    _assert_func = assert_graphs_equal


    def test_graphs_euqal(self):
        G = og.Graph()
        H = og.Graph()
        edges1 = [(1, 2), (2, 3), (1, 3), (3, 4), (4, 5), (4, 6), (5, 6)]
        edges2 = [(3, 7), (4, 7), (10, 7), (11, 7)]
        edges3 = [(8, 9), (8, 10), (9, 10), (10, 11), (11, 12), (11, 13), (12, 13)]
        G.add_edges(edges1)
        G.add_edges(edges2)
        G.add_edges(edges3)
        H.add_edges(edges1)
        H.add_edges(edges2)
        H.add_edges(edges3)
        self._test_equal(G, H)

    def test_graphs_not_equal(self):
        G = og.Graph()
        H = og.Graph()
        edges1 = [(1, 2), (2, 3), (1, 3), (3, 4), (4, 5), (4, 6), (5, 6)]
        edges2 = [(3, 7), (4, 7), (10, 7), (11, 7)]
        edges3 = [(8, 9), (8, 10), (9, 10), (10, 11), (11, 12), (11, 13), (12, 13)]
        G.add_edges(edges1)
        G.add_edges(edges2)
        G.add_edges(edges3)
        H.add_edges(edges1)
        H.add_edges(edges2)
        self._test_not_equal(G, H)