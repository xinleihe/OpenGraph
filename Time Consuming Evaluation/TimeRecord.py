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

    def __record_time_interval(self, func, **args):
        start = time.perf_counter()
        func(**args)
        end = time.perf_counter()
        return end-start

    def __generate_graphs(self, test_counts):
        graphs = []
        if self.package_name == 'NetworkX':
            for i in range(test_counts):
                graphs.append(nx.generators.random_graphs.erdos_renyi_graph(
                    n=self.__graph_generator_config['nodes_num'],
                    p=self.__graph_generator_config['erdos_renyi_probability'],
                    directed=self.__graph_generator_config['directed']
                ))
        elif self.package_name == 'SNAP':
            for i in range(test_counts):
                graphs.append(snap.GenRndGnm(
                    (snap.PNGraph if self.__graph_generator_config['directed'] else snap.PUNGraph),
                    self.__graph_generator_config['nodes_num'],
                    self.__graph_generator_config['edges_num'],
                    self.__graph_generator_config['directed']
                ))
        else:
            print("No package named {}".format(self.package_name))

        return graphs

    def set_graph_generator_config(self, directed=False, nodes_num=100, erdos_renyi_probability=0.2):
        self.__graph_generator_config['directed'] = directed
        self.__graph_generator_config['nodes_num'] = nodes_num
        self.__graph_generator_config['edges_num'] = int(
            nodes_num*(nodes_num-1)*erdos_renyi_probability/2)
        self.__graph_generator_config['erdos_renyi_probability'] = erdos_renyi_probability

    def time_record(self, func, test_counts=1000, **args):
        assert test_counts >= 1
        sum = 0
        for i in range(test_counts):
            interval_time = self.__record_time_interval(func=func, **args)
            sum += interval_time
        avg = sum/test_counts
        print("Average running time for \'{}\' in {} times is {} \n".format(
            func.__name__, test_counts, avg))

    def time_record_with_graph(self, func, test_counts=1000, **args):
        assert test_counts >= 1
        graphs = self.__generate_graphs(test_counts=test_counts)
        assert len(graphs) > 0
        sum = 0
        for i in range(test_counts):
            interval_time = self.__record_time_interval(
                func=func, graph=graphs[i], **args)
            sum += interval_time
        avg = sum/test_counts
        print("Average running time for \'{}\' in {} times is {} \n".format(
            func.__name__, test_counts, avg))
