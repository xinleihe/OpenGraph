import sys
sys.path.append('../../../')
import OpenGraph as og

import random
import math
from OpenGraph.utils.decorators import only_implemented_for_UnDirected_graph
from OpenGraph.functions.components.connected import connected_components

__all__ = [
    "common_greedy"
]


@only_implemented_for_UnDirected_graph
def common_greedy(G, k, c=1.0):
    """
    Returns top k nodes as structural hole spanners,
    Algorithm 1 of https://dl.acm.org/profile/81484650642

    Parameters
    ----------
    G : graph
        An undirected graph.
    k : int
        top - k structural hole spanners
    c : float
        To define zeta: zeta = c * (n*n*n), and zeta is the large
        value assigned as the shortest distance of two unreachable
        vertices.
        Default is 1.
    """
    v_sns = []
    G_i = G.copy()
    N = len(G)
    for i in range(k):
        sorted_nodes = sort_nodes_by_degree(G_i)
        C_max = 0 

        for j in range(N-i):
            G_i_j = G_i.copy()
            G_i_j.remove_node(sorted_nodes[j])
            upper_bound = procedure1(G_i_j, c)
            if upper_bound < C_max:
                pass
            else:
                sum_all_shortest_paths = procedure2(G_i_j, c)
                if sum_all_shortest_paths >= C_max:
                    v_i = sorted_nodes[j]
                    C_max = sum_all_shortest_paths
                else:
                    pass
            del G_i_j
        
        v_sns.append(v_i)
        G_i.remove_node(v_i)
    return v_sns


def sort_nodes_by_degree(G):
    sorted_nodes = []
    for node, degree in sorted(G.degree.items(), key=lambda x: x[1], reverse=True):
        sorted_nodes.append(node)
    return sorted_nodes


def procedure1(G, c=1.0):
    """
    Procedure 1 of https://dl.acm.org/profile/81484650642

    Parameters
    -----------
    G : graph
    c : float
        To define zeta: zeta = c * (n*n*n)
        Default is 1.
    """
    components = connected_components(G)
    upper_bound = 0
    for component in components:
        component_subgraph = G.nodes_subgraph(from_nodes=list(component))
        spanning_tree = _get_spanning_tree_of_component(component_subgraph)


        random_root = list(spanning_tree.nodes)[random.randint(0, len(spanning_tree)-1)]
        num_subtree_nodes = _get_num_subtree_nodes(spanning_tree, random_root)

        N_tree = num_subtree_nodes[random_root]
        for node, num in num_subtree_nodes.items():
            upper_bound += 2 * num * (N_tree - num)
        
        del component_subgraph, spanning_tree

    N_G = len(G)
    zeta = c * math.pow(N_G, 3)
    for component in components:
        N_c = len(component)
        upper_bound += N_c * (N_G - N_c) * zeta

    return upper_bound


def _get_spanning_tree_of_component(G):
    spanning_tree = og.Graph()
    seen = set()
    def _plain_dfs(u):
        for v, edge_data in G.adj[u].items():
            if v not in seen:
                seen.add(v)
                spanning_tree.add_edge(u, v)
                _plain_dfs(v)

    random_node = list(G.nodes)[0]
    seen.add(random_node)
    spanning_tree.add_node(random_node)

    _plain_dfs(random_node)
    
    return spanning_tree


def _get_num_subtree_nodes(G, root):
    num_subtree_nodes = dict()
    seen = set()
    def _plain_dfs(u):
        num_nodes = 1
        for v, edge_data in G.adj[u].items():
            if v not in seen:
                seen.add(v)
                num_nodes += _plain_dfs(v)

        num_subtree_nodes[u] = num_nodes
        return num_nodes

    seen.add(root)
    _plain_dfs(root)

    return num_subtree_nodes


def procedure2(G, c=1.0):
    """
    Procedure 2 of https://dl.acm.org/profile/81484650642

    Parameters
    -----------
    G : graph
    c : float
        To define zeta: zeta = c * (n*n*n)
        Default is 1.
    """
    components = connected_components(G)
    C = 0
    N_G = len(G)
    zeta = c * math.pow(N_G, 3)
    for component in components:
        component_subgraph = G.nodes_subgraph(from_nodes=list(component))
        C_l = _get_sum_all_shortest_paths_of_component(component_subgraph)
        N_c = len(component)
        C += (C_l + N_c * (N_G - N_c) * zeta)

        del component_subgraph

    return C


def _get_sum_all_shortest_paths_of_component(G):
    # TODO: Using randomized algorithm in http://de.arxiv.org/pdf/1503.08528
    #       instead of bfs method.
    def _plain_bfs(G, source):
        seen = set([source])
        nextlevel = {source}
        level = 1
        sum_paths_of_G = 0

        while nextlevel:
            thislevel = nextlevel
            nextlevel = set()
            for u in thislevel:
                for v in G.adj[u]:
                    if v not in seen:
                        seen.add(v)
                        nextlevel.add(v)
                        sum_paths_of_G += level
            level += 1
        return sum_paths_of_G

    sum_paths = 0
    for node in G.nodes:
        sum_paths += _plain_bfs(G, node)

    return sum_paths

if __name__ == "__main__":
    g = og.Graph()
    g.add_edge(2,4)
    g.add_edge(3,4)
    g.add_edge(4,5)
    g.add_edge(2,5)
    g.add_edge(6,7)
    g.add_edge(3,6)

    print(common_greedy(g, k=5))