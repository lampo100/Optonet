from unittest.mock import patch
from unittest import TestCase
from optonet.genetic import EvolutionHandler


class GenomeTest(TestCase):
    @patch('optonet.genetic.BaseSelectionHandler')
    @patch('optonet.genetic.BaseMutationHandler')
    @patch('optonet.genetic.BaseCrossoverHandler')
    def setUp(self, MockCrossover, MockMutator, MockSelector):
        self.test_population = [1, 2, 3, 4]
        self.config = {
            'debug': False,
            'population_size': 4,
        }
        self.MockCrossover = MockCrossover
        self.MockMutator = MockMutator
        self.MockSelector = MockSelector

    def test_evolution_cycle(self):
        self.MockCrossover.return_value.crossover.return_value = self.test_population
        self.MockMutator.return_value.mutate.return_value = self.test_population
        self.MockSelector.return_value.choose_parents.return_value = self.test_population
        crossover_handler_mock = self.MockCrossover()
        mutation_handler_mock = self.MockMutator()
        selection_handler_mock = self.MockSelector()

        evolution_handler = EvolutionHandler(starting_population=self.test_population,
                                             selection_handler=selection_handler_mock,
                                             mutation_handler=mutation_handler_mock,
                                             crossover_handler=crossover_handler_mock,
                                             config=self.config)
        evolution_handler.evolve()

        crossover_handler_mock.crossover.assert_called_once_with(self.test_population)
        mutation_handler_mock.mutate.assert_called_once_with(self.test_population)
        selection_handler_mock.choose_parents.assert_called_once_with(self.test_population)

        self.assertEqual(1, evolution_handler.age)

    def test_raising_exception_on_wrong_population_size(self):
        self.MockCrossover.return_value.crossover.return_value = [1]
        self.MockMutator.return_value.mutate.return_value = [1, 2, 3]
        self.MockSelector.return_value.choose_parents.return_value = [8, 9, 10]
        crossover_handler_mock = self.MockCrossover()
        mutation_handler_mock = self.MockMutator()
        selection_handler_mock = self.MockSelector()

        evolution_handler = EvolutionHandler(starting_population=self.test_population,
                                             selection_handler=selection_handler_mock,
                                             mutation_handler=mutation_handler_mock,
                                             crossover_handler=crossover_handler_mock,
                                             config=self.config)
        self.assertRaises(Exception, evolution_handler.evolve)

        crossover_handler_mock.crossover.assert_called_once_with([8, 9, 10])
        mutation_handler_mock.mutate.assert_called_once_with([1])
        selection_handler_mock.choose_parents.assert_called_once_with(self.test_population)

        self.assertEqual(0, evolution_handler.age)


