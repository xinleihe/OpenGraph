import sys
sys.path.append('../../../')
import OpenGraph as og

__all__ = [
    'effective_size',
    'efficiency',
    'constraint'
]


def mutual_weight(G, u, v, weight=None):
    try:
        a_uv = G[u][v].get(weight, 1)
    except KeyError:
        a_uv = 0
    try:
        a_vu = G[v][u].get(weight, 1)
    except KeyError:
        a_vu = 0
    return a_uv + a_vu


def normalized_mutual_weight(G, u, v, norm=sum, weight=None):
    scale = norm(mutual_weight(G, u, w, weight)
                 for w in G.all_neighbors(u))
    return 0 if scale == 0 else mutual_weight(G, u, v, weight) / scale


def effective_size(G, nodes=None, weight=None):
    def redundancy(G, u, v, weight=None):
        nmw = normalized_mutual_weight
        r = sum(nmw(G, u, w, weight=weight) * nmw(G, v, w, norm=max, weight=weight)
                for w in set(G.all_neighbors(u)))
        return 1 - r
    effective_size = {}
    if nodes is None:
        nodes = G
    # Use Borgatti's simplified formula for unweighted and undirected graphs
    if not G.is_directed() and weight is None:
        for v in nodes:
            # Effective size is not defined for isolated nodes
            if len(G[v]) == 0:
                effective_size[v] = float('nan')
                continue
            E = G.ego_subgraph(v)
            effective_size[v] = len(E) - (2 * E.size()) / len(E)
    else:
        for v in nodes:
            # Effective size is not defined for isolated nodes
            if len(G[v]) == 0:
                effective_size[v] = float('nan')
                continue
            effective_size[v] = sum(redundancy(G, v, u, weight)
                                    for u in set(G.all_neighbors(v)))
    return effective_size


def efficiency(G, nodes=None, weight=None):
    e_size = effective_size(G=G, nodes=nodes, weight=weight)
    degree = G.degree(weihgt=weight)
    efficiency = {n: v / degree[n] for n, v in e_size.items()}


def constraint(G, nodes=None, weight=None):
    if nodes is None:
        nodes = G.nodes
    constraint = {}
    for v in nodes:
        # Constraint is not defined for isolated nodes
        neighbors_of_v = set(G.all_neighbors(v))
        if len(neighbors_of_v) == 0:
            constraint[v] = float('nan')
            continue
        constraint[v] = sum(local_constraint(G, v, n, weight)
                            for n in neighbors_of_v)
    return constraint


def local_constraint(G, u, v, weight=None):
    nmw = normalized_mutual_weight
    direct = nmw(G, u, v, weight=weight)
    indirect = sum(nmw(G, u, w, weight=weight) * nmw(G, w, v, weight=weight)
                   for w in set(G.all_neighbors(u)))
    return (direct + indirect) ** 2
