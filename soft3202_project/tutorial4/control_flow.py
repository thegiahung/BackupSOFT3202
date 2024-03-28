from graphviz import Digraph

def calculate_value(x):
    if x < 5:  # Node 1
        y = x * 2  # Node 2
    else:
        y = x + 2  # Node 3
    return y  # Node 4

cfg = {
    'while True': ['if x > 3', 'if x < 3'],
    'if x > 3': ["break out loop"],
    'if x < 3': ['print i'],
    'print i': ['i =+ 1']
}

def visualize_cfg(cfg):
    dot = Digraph()
    for node, edges in cfg.items():
        dot.node(node, node)
        for edge in edges:
            dot.edge(node, edge)
    return dot

# 'cfg' is the Control Flow Graph we defined earlier
dot = visualize_cfg(cfg)
dot.render('cfg', view=True)