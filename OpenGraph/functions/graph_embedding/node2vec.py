import sys
sys.path.append('../../../')
import OpenGraph as og

from node2vec import Node2Vec

__all__ = [
    "node2vec"
]


def node2vec(G, dimensions=128, walk_length=80, num_walks=10, p=1.0, q=1.0, weight_key="weight", workers=1,
             **skip_gram_params):
    """
    Returns 
        1. The embedding vector of each node via node2vec 
        2. The most similar nodes of each node and its similarity
    Packaged functions implemented by https://towardsdatascience.com/node2vec-embeddings-for-graph-data-32a866340fef
    Using Word2Vec model of package gensim.

    Parameters
    ----------
    G : graph

    dimensions : int
        Embedding dimensions (default: 128)

    walk_length : int
        Number of nodes in each walk (default: 80)

    num_walks : int
        Number of walks per node (default: 10)

    p : float
        The return hyper parameter (default: 1.0)

    q : float
        The inout parameter (default: 1.0)

    weight_key : string
        On weighted graphs, this is the key for the weight attribute (default: 'weight')

    workers : int
        Number of workers for parallel execution (default: 1)

    skip_gram_params : dict
        Parameteres for gensim.models.Word2Vec - do not supply 'size' it is taken from the Node2Vec 'dimensions' parameter
    """
    G_index, index_of_node, node_of_index = G.to_index_node_graph()

    node2vec = Node2Vec(graph=G_index, dimensions=dimensions,
                        walk_length=walk_length, num_walks=num_walks, workers=workers)

    # Embed nodes
    model = node2vec.fit(**skip_gram_params)

    embedding_vector = dict()
    most_similar_nodes_of_node = dict()


    def change_string_to_node_from_gensim_return_value(value_including_str):
        # As the return value of gensim model.wv.most_similar includes string index in G_index, 
        # the string index should be changed to the original node element in G.
        result = []
        for (node_index, value) in value_including_str:
            node_index = int(node_index)
            node = node_of_index[node_index]
            result.append((node, value))
        return result

    for node in G.nodes:
        # Output node names are always strings in gensim
        embedding_vector[node] = model.wv[str(index_of_node[node])]

        most_similar_nodes = model.wv.most_similar(str(index_of_node[node]))
        most_similar_nodes_of_node[node] = change_string_to_node_from_gensim_return_value(most_similar_nodes)

    del G_index
    return embedding_vector, most_similar_nodes_of_node


if __name__ == "__main__":
    graph = og.Graph()
    graph.add_edge(2, 4)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(2, 5)
    graph.add_edge(6, 7)
    graph.add_edge(3, 6)

    skip_gram_params = dict(window=10, min_count=1, batch_words=4)

    embedding_vector, most_similar_nodes_of_node = node2vec(
        G=graph,
        dimensions=64, walk_length=30,
        num_walks=200, workers=4, **skip_gram_params
    )

    print(embedding_vector)
    print(most_similar_nodes_of_node)
