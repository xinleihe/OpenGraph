## Classes

### Graph

Undirected graph class

`./classes/graph.py`

- {property} **adj**

  returns the adjacent matrix of each node ( dict )

- {property} **nodes**

  returns all the nodes ( list )

- {property} **edges**

  returns all the edges ( list(tuple) )

- **degree**

  returns degree(weighted or not) of each node ( dict )

- **size**

  returns sum of weight in graph, or the number of edges 

- **neighbors**

  returns the neighbors of node x.

  ```python
  G.neighbors(node=1)
  ```

+ **add_node**

  ```python
  G.add_node(node_for_adding = 1, node_attr = {"attr1": 1, "attr2": 2})
  ```

+ **add_nodes**

  ```python
  G.add_nodes(nodes_for_adding = [1,2,3], 
              nodes_attr = [
                  {"attr1": 1, "attr2": 2},
                  {"attr1": 2, "attr2": 4},
                  {"attr1": 3, "attr2": 6},
              ])
  ```

+ **add_edge**

  ```python
  G.add_edge(u_of_edge = 1, v_of_edge = 2)
  ```

+ **add_weighted_edge**

  ```python
  G.add_weighted_edge(u_of_edge = 1, v_of_edge = 2, weight = 2)
  ```

+ **add_edges**

  ```python
  G.add_edge(edges_for_adding = [(1,2), (2,3)],
            edges_attr = [
                {"weight": 1, "flow": 2},
                {"weight": 2, "flow": 2}
            ])
  ```

+ **remove_node**

  ```python
  G.remove_node(node_to_remove = 1)
  ```

+ **remove_nodes**

  ```python
  G.remove_nodes(nodes_to_remove = [1, 2, 3])
  ```

+ **remove_edge**

  ```python
  G.remove_edge(u = 1, v = 2)
  ```

+ **remove_edges**

  ```python
  G.remove_edges(edges_to_remove = [(1,2), (2,3)])
  ```

+ **has_node**

  returns whether node x exists in the graph or not

  ```python
  G.has_node(node=1) 
  ```

+ **has_edge**

  returns whether edge (u, v) exists in the graph or not ( boolean )

  ```python
  G.has_edge(u=1, v=2)
  ```

+ **number_of_nodes**

  returns number of nodes in the graph ( int )

+ **number_of_edges**

  returns number of edges in the graph ( int )

+ **is_directed**

  returns whether this is a directed graph or not ( boolean )

+ **copy**

  returns deep copy of the graph ( OpenGraph.Graph )

  ```python
  G_duplicate = G.copy()
  ```

+ **nodes_subgraph**

  returns subgraph of nodes [...] (OpenGraph.Graph)

  ```python
  G_subgraph = G.nodes_subgraph(from_nodes = [1,2,3])
  ```

+ **to_index_node_graph**

  returns

  1. deepcopy of graph, with each node switched to its index.
  2. index of node 
  3. node of index

  ```python
  G_index, index_of_node, node_of_index = G.to_index_node_graph()
  ```

### DiGraph

Directed graph class

`./classes/directed_graph.py`

Many properties and functions are same as Class Graph, except:

+ **neighbors**

  returns the **successors** of node x
  
+ **out_degree**

  returns out degree(weighted or not) of each node ( dict )

+ **in_degree**

  returns out degree(weighted or not) of each node ( dict )

## Functions

### Components

`./functions/components/connected.py`

+ **is_connected**

  return whether the graph is connected or not

  ```python
  is_connected(G = G)
  ```

+ **number_connected_components**

  return the number of connected components

  ```python
  number_connected_components(G = G)
  ```

+ **connected_components**

  return all components ordered by number of nodes included

  ```python
  connected_components(G = G)
  ```

+ **connected_component_of_node**

  return connected component including node x

  ```python
  connected_component_of_node(G = G, node = 1)
  ```

`./functions/components/biconnected.py`

+ **is_biconnected**

  return whether the graph is biconnected or not

  ```python
  is_biconnected(G = G)
  ```

+ **biconnected_components**

  return all biconnected components

  ```python
  biconnected_components(G = G)
  ```

+ **generator_biconnected_components_nodes**

  return a generator of the nodes of each biconnected components

  ```python
  generator_biconnected_components_nodes(G = G)
  ```

+ **generator_biconnected_components_edges**

  return a generator of the edges of each biconnected components

  ```python
  generator_biconnected_components_edges(G = G)
  ```

+ **generator_articulation_points**

  return a generator of articulation points

  ```python
  generator_articulation_points(G = G)
  ```



### Community

`./functions/community/modularity_max_detection.py`

+ **greedy_modularity_communities**

  yields sets of nodes, one for each community, via method Clauset-Newman-Moore greedy modularity maximization

  ```python
  # Init graph
  g = og.classes.Graph()
  g.add_edges(edges_for_adding = [(1, 2), (2, 3), (1, 3), (3, 4), (4, 5), (4, 6), (5, 6)])
  
  print(greedy_modularity_communities(G = g, weight = None))
  ```

+ **modularity**

  returns modularity of a nodes community

  *TODO: multigraph and directed detection not included. Check networkx.*

  ```python
  # Init graph
  g = og.classes.Graph()
  g.add_edges(edges_for_adding = [(1, 2), (2, 3), (1, 3), (3, 4), (4, 5), (4, 6), (5, 6)])
  
  # Nodes communities
  cmnts = [frozenset([1, 2, 3]), frozenset([4, 5, 6])]
  
  print(modularity(G = g, communities = cmnts))
  ```

  

### Structural Holes

`./functions/structural_holes/HIS.py`

+ **get_structural_holes_HIS**

  returns the Importance score **I** and structural hole score **H** via method **HIS**(https://www.aminer.cn/structural-hole)

  ```python
  # Init graph
  g = og.classes.Graph()
  edges1 = [(1, 2), (2, 3), (1, 3), (3, 4), (4, 5), (4, 6), (5, 6)]
  edges2 = [(3, 7), (4, 7), (10, 7), (11, 7)]
  edges3 = [(8, 9), (8, 10), (9, 10), (10, 11), (11, 12), (11, 13), (12, 13)]
  g.add_edges(edges1)
  g.add_edges(edges2)
  g.add_edges(edges3)
  
  # Nodes communities
  cmnts = [frozenset([1, 2, 3]), frozenset([4, 5, 6]), frozenset([3, 4, 7, 10, 11]),
           frozenset([8, 9, 10]), frozenset([11, 12, 13])]
  
  # Get structural holes via HIS method
  S, I, H = get_structural_holes_HIS(G = g, C = cmnts, epsilon=0.01)
  ```

`./functions/structural_holes/MaxD.py`

+ **get_structural_holes_MaxD**

  returns top-k structural holes spanners of the graph, via method **MaxD**(https://www.aminer.cn/structural-hole)

  ```python
  # Init graph
  g = og.classes.Graph()
  edges1 = [(1, 2), (2, 3), (1, 3), (3, 4), (4, 5), (4, 6), (5, 6)]
  edges2 = [(3, 7), (4, 7), (10, 7), (11, 7)]
  edges3 = [(8, 9), (8, 10), (9, 10), (10, 11), (11, 12), (11, 13), (12, 13)]
  g.add_edges(edges1)
  g.add_edges(edges2)
  g.add_edges(edges3)
  
  # Nodes communities
  cmnts = [frozenset([1, 2, 3]), frozenset([4, 5, 6]), frozenset([3, 4, 7, 10, 11]),
           frozenset([8, 9, 10]), frozenset([11, 12, 13])]
  
  k = 5 # top-k spanners
  
  k_top = get_structural_holes_MaxD(G = g, k_size = k, C = cmnts)
  ```

`./functions/structural_holes/AP_Greedy.py`

+ **common_greedy**

  returns top-k nodes as structural hole spanners, Algorithm 1 of https://dl.acm.org/profile/81484650642

  ```python
  # Init graph
  g = og.classes.Graph()
  g.add_edges(edges_for_adding = [(2,4), (3,4), (4,5), (2,5), (6,7), (3,6)])
  
  # top-k spanners
  k = 5
  
  k_top = common_greedy(G = g, k = k, c = 1.0)
  ```

+ **AP_greedy**

  returns top k nodes as structural hole spanners, Algorithm 2 of https://dl.acm.org/profile/81484650642

  ```python
  # Init graph
  g = og.classes.Graph()
  g.add_edges(edges_for_adding = [(2,4), (3,4), (4,5), (2,5), (6,7), (3,6)])
  
  # top-k spanners
  k = 5 
  
  k_top = AP_greedy(G = g, k = k, c = 1.0)
  ```



### Graph Embedding

`./functions/graph_embedding/deepwalk.py`

+ **deepwalk**

  returns

  1. The embedding vector of each node via DeepWalk: https://arxiv.org/abs/1403.6652
  2. The most similar nodes of each node and its similarity

  ```python
  # Init graph
  g = og.classes.Graph()
  g.add_edges(edges_for_adding = [(2,4), (3,4), (4,5), (2,5), (6,'a'), (3,6)])
  
  # Skip_gram parameters
  skip_gram_params = dict(window=10, min_count=1, batch_words=4)
  
  # DeepWalk results
  embedding_vector, most_similar_nodes_of_node = deepwalk(
      G=g,
      dimensions=64, walk_length=30,
      num_walks=2000, **skip_gram_params
  )
  ```

`./functions/graph_embedding/line.py`

+ **Class: LINE**

  Graph embedding model **LINE** of https://arxiv.org/pdf/1503.03578.pdf

  ```python
  # Init graph
  with open('./Wiki_edgelist.txt', 'r') as fp:
      data = fp.readlines()
  G = og.Graph()
  for edge in data:
      edge = edge.split()
      try:
          G.add_edge(int(edge[0]), int(edge[1]))
      except:
          pass
  
  # Model LINE
  model = LINE(G, embedding_size=128, order='second')
  model.train(batch_size=1024, epochs=50, verbose=2)
  embeddings = model.get_embeddings()
  ```

`./functions/graph_embedding/sdne.py`

+ **Class: SDNE**

  Graph embedding model **SDNE** of https://www.kdd.org/kdd2016/papers/files/rfp0191-wangAemb.pdf

  ```python
  # Init graph
  with open('./Wiki_edgelist.txt', 'r') as fp:
      data = fp.readlines()
  G = og.Graph()
  for edge in data:
      edge = edge.split()
      try:
          G.add_edge(int(edge[0]), int(edge[1]))
      except:
          pass
      
  # Model SDNE
  model = SDNE(G, hidden_size=[256, 128],)
  model.train(batch_size=3000, epochs=40, verbose=2)
  embeddings = model.get_embeddings()
  ```

`./functions/graph_embedding/node2vec.py`

+ **node2vec**

  returns

  1. The embedding vector of each node via node2vec: https://arxiv.org/abs/1607.00653
  2. The most similar nodes of each node and its similarity

  ```python
  # Init graph
  g = og.classes.Graph()
  g.add_edges(edges_for_adding = [(2,4), (3,4), (4,5), (2,5), (6,'a'), (3,6)])
  
  # Skip_gram parameters
  skip_gram_params = dict(window=10, min_count=1, batch_words=4)
  
  # Node2vec results
  embedding_vector, most_similar_nodes_of_node = node2vec(
      G=g,
      dimensions=64, walk_length=30,
      num_walks=2000, **skip_gram_params
  )
  ```



### Drawing

`./functions/drawing/positioning.py`

+ **random_position**

  returns random positions for each node in graph G. 

  ```python
  # generated positions of graph G
  pos = random_position(G)
  ```

+ **circular_position**

  returns nodes' positions on a circle, the dimension is 2.

  ```python
  # generated positions of graph G
  pos = circular_position(G)
  ```

+ **shell_position**

  returns nodes' positions in concentric circles, the dimension is 2.

  ```python
  # generated positions of graph G
  pos = shell_position(G)
  ```

+ **rescale_position**

  returns scaled positions array of a given positions list

  ```python
  # previous positions list
  pos = [(1,2), (2,1), (3,4), (4,5)]
  
  # rescaled positions
  pos = rescale_position(pos = pos, scale = 1)
  ```

  

  

  