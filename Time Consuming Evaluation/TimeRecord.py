import networkx as nx
import snap
import time


class TimeRecord:
    package_name = None
    __graph_generator_config = {
        "directed": None,
        "nodes_num": None,
        "edges_num": None,
        "erdos_renyi_probability": None,
    }

    def __init__(self, package_name):
        self.package_name = package_name
        self.set_graph_generator_config()

    def set_graph_generator_config(self, directed=False, nodes_num=100, erdos_renyi_probability=0.2):
        self.__graph_generator_config['directed'] = directed
        self.__graph_generator_config['nodes_num'] = nodes_num
        self.__graph_generator_config['edges_num'] = int(
            nodes_num*(nodes_num-1)*erdos_renyi_probability/2)
        self.__graph_generator_config['erdos_renyi_probability'] = erdos_renyi_probability

    def get_time_of_func(self, func, need_generate_graph=False, test_times=1000, **args):
        assert test_times >= 1
        sum = 0
        if need_generate_graph:
            graphs = self.__generate_graphs(test_times=test_times)
            assert len(graphs) >= 1
            for i in range(test_times):
                interval_time = self.__record_time_interval(
                    func=func, graph=graphs[i], **args)
                sum += interval_time
        else:
            for i in range(test_times):
                interval_time = self.__record_time_interval(func=func, **args)
                sum += interval_time

        avg = sum/test_times
        print("Average running time for \'{}\' in {} times is {} \n".format(
            func.__name__, test_times, avg))
    
    def __generate_graphs(self, test_times):
        if self.package_name == 'NetworkX':
            graphs = self.__generate_NetworkX_graphs(graphs_num=test_times)
        elif self.package_name == 'SNAP':
            graphs = self.__generate_SNAP_graphs(graphs_num=test_times)
        else:
            graphs = []
            print("No package named {}".format(self.package_name))

        return graphs

    def __generate_NetworkX_graphs(self, graphs_num):
        graphs = []
        for i in range(graphs_num):
            graphs.append(nx.generators.random_graphs.erdos_renyi_graph(
                n=self.__graph_generator_config['nodes_num'],
                p=self.__graph_generator_config['erdos_renyi_probability'],
                directed=self.__graph_generator_config['directed']
            ))
        return graphs

    def __generate_SNAP_graphs(self, graphs_num):
        graphs = []
        for i in range(graphs_num):
            graphs.append(snap.GenRndGnm(
                (snap.PNGraph if self.__graph_generator_config['directed'] else snap.PUNGraph),
                self.__graph_generator_config['nodes_num'],
                self.__graph_generator_config['edges_num'],
                self.__graph_generator_config['directed']
            ))
        return graphs

    def __record_time_interval(self, func, **args):
        start = time.perf_counter()
        func(**args)
        end = time.perf_counter()
        return end-start
