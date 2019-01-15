import networkx as nx
import numpy as np
import holoviews as hv
from holoviews import opts
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from optonet.network_model import Network

hv.extension('bokeh')

defaults = dict(width=900, height=900, padding=0.1)
hv.opts.defaults(
    opts.EdgePaths(**defaults), opts.Graph(**defaults), opts.Nodes(**defaults))

def visualize_solution(network: Network, solution: dict):
    # source = [link.first_node for link in network.links]
    # dest = [link.second_node for link in network.links]
    # links = [(link.first_node, link.second_node) for link in network.links]
    #
    # features = {source: [demand[1] for demand in demands] for source, demands in solution[0].items()}
    # simple_graph = hv.Graph((links))
    # x, y = simple_graph.nodes.array([0, 1]).T
    #
    # ids = [node.id for node in network.nodes]
    # nodes = hv.Nodes((x, y, ids, *features.keys()), vdims=['Type', 'Type2'])
    # simple_graph = hv.Graph(((links, nodes)))
    # simple_graph.opts(node_size=30, arrowhead_length=0.03)

    N = 8
    node_indices = np.arange(N, dtype=np.int32)
    source = np.zeros(N, dtype=np.int32)
    target = node_indices

    simple_graph = hv.Graph(((source, target),))

    def bezier(start, end, control, steps=np.linspace(0, 1, 100)):
        return (1 - steps) ** 2 * start + 2 * (1 - steps) * steps * control + steps ** 2 * end

    x, y = simple_graph.nodes.array([0, 1]).T

    paths = []
    for node_index in node_indices:
        ex, ey = x[node_index], y[node_index]
        paths.append(np.column_stack([bezier(x[0], ex, 0), bezier(y[0], ey, 0)]))

    bezier_graph = hv.Graph(((source, target), (x, y, node_indices), paths))

    node_labels = ['Output'] + ['Input'] * (N - 1)
    np.random.seed(7)
    edge_labels = np.random.rand(8)

    nodes = hv.Nodes((x, y, node_indices, node_labels), vdims=['Type', 'Type2'])
    graph = hv.Graph(((source, target, edge_labels), nodes, paths), vdims='Weight')

    (graph + graph.opts(inspection_policy='edges', clone=True)).opts(
        opts.Graph(node_color='Type', edge_color='Weight', cmap='Set1',
                   edge_cmap='viridis', edge_line_width=hv.dim('Weight') * 10))
    hv.save(graph, 'out.html')

def visualize_evolution(statistics, filepath):
    colors = (
        ('blue', 'mean'),
        ('red', 'min'),
        ('green', 'max')
    )
    plt.xlabel('generation')
    plt.ylabel('fitness score')
    for x, y in colors:
        plt.plot(range(len(statistics)), [gen[y] for gen in statistics.values()], x)
    plt.legend(handles=[mlines.Line2D([], [], color=x, label=y) for x, y in colors])
    plt.xlim(-1, len(statistics))
    plt.savefig(filepath)
    plt.clf()
