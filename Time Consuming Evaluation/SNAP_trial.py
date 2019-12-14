import snap
from TimeRecord import TimeRecord


def generate_graph_erdos_renyi(n=100, p=0.2, directed=False):
    edges = int(n*(n-1)*p/2)
    if directed:
        g = snap.GenRndGnm(snap.PNGraph, n, edges, True)
    else:
        g = snap.GenRndGnm(snap.PUNGraph, n, edges, False)


def generate_complete_graph(n=100, directed=False):
    if directed:
        g = snap.GenFull(snap.PNGraph, n)
    else:
        g = snap.GenFull(snap.PUNGraph, n)


front_20_nodes = snap.TIntV()
for i in range(20):
    front_20_nodes.Add(i)


def get_subgraph(graph, nodes=front_20_nodes):
    sg = snap.ConvertSubGraph(snap.PUNGraph, graph, front_20_nodes)


def get_connected_components_number(graph: snap.PUNGraph):
    components = snap.TCnComV()
    snap.GetWccs(graph, components)


def get_strongly_connected_components_number(graph: snap.PNGraph):
    components = snap.TCnComV()
    snap.GetSccs(graph, components)


def get_weakly_connected_components_number(graph: snap.PNGraph):
    components = snap.TCnComV()
    snap.GetWccs(graph, components)


def get_closeness_centrality(graph):
    for ni in graph.Nodes():
        snap.GetClosenessCentr(graph, ni.GetId())


def get_betweenness_centrality(graph):
    nodes = snap.TIntFltH()
    edges = snap.TIntPrFltH()
    snap.GetBetweennessCentr(graph, nodes, edges, 1.0)


def get_communities_girvan_newman(graph: snap.PUNGraph):
    CmtyV = snap.TCnComV()
    modularity = snap.CommunityGirvanNewman(graph, CmtyV)


def get_communities_CNM(graph: snap.PUNGraph):
    CmtyV = snap.TCnComV()
    modularity = snap.CommunityCNM(graph, CmtyV)


def get_clustering_coefficient(graph):
    GraphClustCoeff = snap.GetClustCf(graph, -1)


def get_k_core(graph, K=5):
    KCore = snap.GetKCore(graph, K)


if __name__ == "__main__":
    recorder = TimeRecord(package_name="SNAP")
    
    recorder.get_time_of_func(func=generate_graph_erdos_renyi, n=100, p=0.2, directed=False)
    recorder.get_time_of_func(func=generate_complete_graph, n=100, directed=False)

    recorder.set_graph_generator_config(directed=False, nodes_num=100, erdos_renyi_probability=0.2)
    recorder.get_time_of_func(func=get_subgraph, need_generate_graph=True)

    recorder.set_graph_generator_config(directed=False, nodes_num=100, erdos_renyi_probability=0.05)
    recorder.get_time_of_func(func=get_connected_components_number, need_generate_graph=True)
    
    recorder.set_graph_generator_config(directed=True, nodes_num=100, erdos_renyi_probability=0.05)
    recorder.get_time_of_func(func=get_strongly_connected_components_number, need_generate_graph=True)
    recorder.get_time_of_func(func=get_weakly_connected_components_number, need_generate_graph=True)
    
    recorder.set_graph_generator_config(directed=False, nodes_num=100, erdos_renyi_probability=0.2)
    recorder.get_time_of_func(func=get_closeness_centrality, need_generate_graph=True)
    recorder.get_time_of_func(func=get_betweenness_centrality, need_generate_graph=True)
    recorder.get_time_of_func(func=get_communities_girvan_newman, test_times=10, need_generate_graph=True)
    recorder.get_time_of_func(func=get_communities_CNM, need_generate_graph=True)
    recorder.get_time_of_func(func=get_clustering_coefficient, need_generate_graph=True)
    recorder.get_time_of_func(func=get_k_core, need_generate_graph=True)
