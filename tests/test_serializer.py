from unittest import TestCase
from optonet.model_parser import parse_xml
from optonet.optonet_evolution import initialize_optonet_population
from optonet.serializer import serialize, deserialize

class SerializingTest(TestCase):
    def test_dumping(self):
        polska = parse_xml('../network_instances/polska.xml')
        initial_population = initialize_optonet_population(polska, 3000)
        serialize(initial_population, "./test_pop")
        deserialized_population = deserialize("./test_pop")
        self.assertEqual(initial_population, deserialized_population)

