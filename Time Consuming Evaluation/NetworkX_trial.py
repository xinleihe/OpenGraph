import networkx as nx
from networkx.algorithms import approximation
from TimeRecord import TimeRecord


def generate_graph_erdos_renyi(n=100, p=0.2, directed=None):
    g = nx.generators.random_graphs.erdos_renyi_graph(
        n=n, p=p, directed=directed)


def generate_complete_graph(n=100, create_using=None):
    g = nx.generators.classic.complete_graph(n=n, create_using=create_using)


def generate_directed_gn_graph(n=100, kernel=None):
    g = nx.generators.directed.gn_graph(n=n, kernel=kernel)


def get_subgraph(graph, nodes=[(i+1) for i in range(20)]):
    sg = graph.subgraph(nodes)


def get_connected_components_number(graph: nx.Graph):
    connected_components_number = nx.algorithms.components.number_connected_components(
        G=graph)


def get_strongly_connected_components_number(graph: nx.DiGraph):
    strongly_connected_components_number = nx.algorithms.components.number_strongly_connected_components(
        G=graph)


def get_weakly_connected_components_number(graph: nx.DiGraph):
    weakly_connected_components_number = nx.algorithms.components.number_weakly_connected_components(
        G=graph)


def get_all_cliques(graph: nx.Graph):
    cliques = nx.algorithms.clique.enumerate_all_cliques(G=graph)


def get_min_edge_dominating_set(graph: nx.Graph):
    meds = nx.algorithms.approximation.dominating_set.min_edge_dominating_set(
        G=graph)


def get_closeness_centrality(graph):
    cc = nx.algorithms.centrality.closeness_centrality(G=graph)


def get_betweenness_centrality(graph):
    bc = nx.algorithms.centrality.betweenness_centrality(G=graph)


def get_communities_girvan_newman(graph):
    communities = nx.algorithms.community.centrality.girvan_newman(G=graph)


def get_clustering_coefficient(graph):
    cc = nx.algorithms.cluster.average_clustering(G=graph)


def get_k_core(graph, K=5):
    kc = nx.algorithms.core.k_core(G=graph, k=K)


if __name__ == "__main__":
    recorder = TimeRecord(package_name='NetworkX')

    recorder.get_time_of_func(func=generate_graph_erdos_renyi, n=100, p=0.2)
    recorder.get_time_of_func(func=generate_complete_graph, n=100)
    recorder.get_time_of_func(func=generate_directed_gn_graph, n=100)

    recorder.set_graph_generator_config(directed=False, nodes_num=100, erdos_renyi_probability=0.2)
    recorder.get_time_of_func(func=get_subgraph, need_generate_graph=True)

    recorder.set_graph_generator_config(directed=False, nodes_num=100, erdos_renyi_probability=0.05)
    recorder.get_time_of_func(func=get_connected_components_number, need_generate_graph=True)

    recorder.set_graph_generator_config(directed=True, nodes_num=100, erdos_renyi_probability=0.05)
    recorder.get_time_of_func(func=get_strongly_connected_components_number, need_generate_graph=True)
    recorder.get_time_of_func(func=get_weakly_connected_components_number, need_generate_graph=True)

    recorder.set_graph_generator_config(directed=False, nodes_num=100, erdos_renyi_probability=0.2)
    recorder.get_time_of_func(func=get_all_cliques, test_times=10, need_generate_graph=True)
    recorder.get_time_of_func(func=get_min_edge_dominating_set, need_generate_graph=True)
    recorder.get_time_of_func(func=get_closeness_centrality, test_times=100, need_generate_graph=True)
    recorder.get_time_of_func(func=get_betweenness_centrality, test_times=100, need_generate_graph=True)
    recorder.get_time_of_func(func=get_communities_girvan_newman, test_times=100, need_generate_graph=True)
    recorder.get_time_of_func(func=get_clustering_coefficient, need_generate_graph=True)
    recorder.get_time_of_func(func=get_k_core, need_generate_graph=True, K=5)
