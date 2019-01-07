from optonet.model_parser import parse_xml

if __name__ == '__main__':
    janos_us = parse_xml('network_instances/janos-us.xml')  # currently demands have awkwardly similar paths i.e. the same starting links and only different at the end, might want to change this later
    polska = parse_xml('network_instances/polska.xml')
