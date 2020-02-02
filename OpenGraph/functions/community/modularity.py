from itertools import product

__all__ = [
    "modularity"
]

def modularity(G, communities, weight='weight'):
    # TODO: multigraph and directed detection not included. See networkx.

    if not isinstance(communities, list):
        communities = list(communities)

    m = G.size
    out_degree = dict(G.degree)
    in_degree = out_degree
    norm = 1 / (2 * m)

    def val(u, v):
        try:
            w = G[u][v].get(weight, 1)
        except KeyError:
            w = 0
        # Double count self-loops if the graph is undirected.
        if u == v:
            w *= 2
        return w - in_degree[u] * out_degree[v] * norm

    Q = sum(val(u, v) for c in communities for u, v in product(c, repeat=2))
    return Q * norm


if __name__ == "__main__":
    import sys
    sys.path.append('../../../')
    import OpenGraph as og
    
    g = og.Graph()
    edges1 = [(1, 2), (2, 3), (1, 3), (3, 4), (4, 5), (4, 6), (5, 6)]
    g.add_edges(edges1)

    cmnts = [frozenset([1, 2, 3]), frozenset([4, 5, 6])]
    print(modularity(G=g, communities=cmnts))


