## Classes

### Graph

Undirected graph class

`./classes/graph.py`

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

+ {property} **adj**

  return the adjacent matrix of each node ( dict )

+ {property} **nodes**

  return all the nodes ( list )

+ {property} **edges**

  return all the edges ( list(tuple) )

+ {property} **degree**

  return degree of each node ( dict )

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

### Structural Holes

`./functions/structural_holes/HIS.py`

+ **get_structural_holes_HIS**

  return the Importance score **I** and structural hole score **H** via method **HIS**(https://www.aminer.cn/structural-hole)

  ```python
  # Init graph
  g = og.classes.Graph()
  edges1 = [(1, 2), (2, 3), (1, 3), (3, 4), (4, 5), (4, 6), (5, 6)]
  edges2 = [(3, 7), (4, 7), (10, 7), (11, 7)]
  edges3 = [(8, 9), (8, 10), (9, 10), (10, 11), (11, 12), (11, 13), (12, 13)]
  g.add_edges(edges1)
  g.add_edges(edges2)
  g.add_edges(edges3)
  
  cmnts = [frozenset([1, 2, 3]), frozenset([4, 5, 6]), frozenset([3, 4, 7, 10, 11]),
           frozenset([8, 9, 10]), frozenset([11, 12, 13])]
  
  # Get structural holes via HIS method
  S, I, H = get_structural_holes_HIS(G = g, C = cmnts, epsilon=0.01)
  ```

  

  