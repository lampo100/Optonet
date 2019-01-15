import xml.etree.ElementTree
import networkx as nx
import random

from optonet.network_model import Network, Link, Node, Demand

FIND_ADMISSIBLE_PATHS_NUMBER = 3


def parse_xml(xml_path: str) -> Network:
    xml_root = xml.etree.ElementTree.parse(xml_path).getroot()
    xml_network_structure = xml_root.find('networkStructure')

    # ------------------------- NODES -------------------------

    xml_nodes = xml_network_structure.find('nodes')
    nodes = []
    id_to_node = dict()

    for xml_node in xml_nodes.findall('node'):
        id = xml_node.attrib['id']
        node = Node(id)
        nodes.append(node)
        id_to_node[id] = node

    # ------------------------- LINKS -------------------------

    xml_links = xml_network_structure.find('links')
    links = []
    id_to_link = dict()
    already_created_links = set()

    for xml_link in xml_links.findall('link'):
        id = xml_link.attrib['id']
        source = xml_link.find('source').text
        target = xml_link.find('target').text
        # prevent duplicates
        if {source, target} in already_created_links:
            continue
        else:
            already_created_links.add(frozenset([source, target]))
        link = Link(id, source, target)
        links.append(link)
        id_to_link[id] = link

    # ------------------------- DEMANDS -------------------------

    xml_demands = xml_root.find('demands')
    demands = []
    already_created_demands = set()

    for xml_demand in xml_demands.findall('demand'):
        id = xml_demand.attrib['id']
        source = xml_demand.find('source').text
        target = xml_demand.find('target').text

        # prevent duplicates
        if {source, target} in already_created_demands:
            continue
        else:
            already_created_demands.add(frozenset([source, target]))

        value = xml_demand.find('demandValue').text
        xml_admissible_paths = xml_demand.find('admissiblePaths')
        paths = []
        if xml_admissible_paths is not None:
            for xml_path in xml_admissible_paths.findall('admissiblePath'):
                path = [id_to_link[link_id.text] for link_id in xml_path.findall('linkId')]
                paths.append(path)
        else:
            paths = _find_paths(links, source, target, FIND_ADMISSIBLE_PATHS_NUMBER)

        demands.append(Demand(id, source, target, paths, value))

    return Network(nodes, links, demands)


def _find_paths(links, source, target, paths_no):
    edges = [(link.first_node, link.second_node) for link in links]
    graph = nx.Graph(edges)
    all_paths = random.choices([x for x in nx.all_simple_paths(graph, source=source, target=target)], k=paths_no)
    paths_of_links = [[]] * paths_no
    for index, path in enumerate(all_paths):
        i = 0
        while i != len(path) - 1:
            for link in links:
                if (link.first_node == path[i] and link.second_node == path[i+1]) or (link.first_node == path[i+1] and link.second_node == path[i]):
                    paths_of_links[index].append(link)
            i += 1

    return paths_of_links
