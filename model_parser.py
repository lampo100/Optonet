import xml.etree.ElementTree
from pprint import pprint

from network_model import Network, Link, Node, Demand

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
    node_to_neighbours = dict()
    node_to_is_visited = dict()

    for link in links:
        node_to_neighbours.setdefault(link.first_node, []).append((link.second_node, link))
        node_to_neighbours.setdefault(link.second_node, []).append((link.first_node, link))

    paths = []

    _find_paths_dfs(paths, node_to_neighbours, node_to_is_visited, paths_no, source, target, [])

    return paths


def _find_paths_dfs(found_paths, node_to_neighbours, node_to_is_visited, paths_no, current_node, target, path_so_far):
    if current_node == target:
        found_paths.append(path_so_far)
    else:
        node_to_is_visited[current_node] = True
        for neighbour in node_to_neighbours[current_node]:
            if not node_to_is_visited.get(neighbour[0], False):
                _find_paths_dfs(found_paths, node_to_neighbours, node_to_is_visited, paths_no, neighbour[0], target, path_so_far + [neighbour[1]])
                node_to_is_visited[neighbour[0]] = False
                if (len(found_paths)) == paths_no:
                    return
