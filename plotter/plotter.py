import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from optonet.network_model import Network


def visualize_network(network: Network):
    graph = nx.Graph()
    for node in network.nodes:
        graph.add_node(node.id)
    for link in network.links:
        graph.add_edge(link.first_node, link.second_node, capacity=link.capacity)
    plt.subplot(121)
    nx.draw(graph, with_labels=True, node_size=1500, font_size=5, node_color='skyblue')
    plt.show()


def visualize_evolution(statistics):
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
    plt.show()
