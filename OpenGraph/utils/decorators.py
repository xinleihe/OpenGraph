__all__ = [
    "only_implemented_for_UnDirected_graph",
    "only_implemented_for_Directed_graph"
]


def only_implemented_for_UnDirected_graph(func, *args, **kwargs):
    print("--------Only Implemented For UnDirected Graph--------")
    return func(*args, **kwargs)

def only_implemented_for_Directed_graph(func, *args, **kwargs):
    print("--------Only Implemented For Directed Graph--------")
    return func(*args, **kwargs)
