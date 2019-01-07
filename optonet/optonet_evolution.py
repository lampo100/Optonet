from .genetic import BaseCrossoverHandler, BaseMutationHandler, BaseSelectionHandler


class OptonetCrossover(BaseCrossoverHandler):
    """
    BaseCrossoverHandler implementation for the problem of satisfying demand in optical network.
    """
    def crossover(self, parents):
        """
        Do crossover on parent generation. This implementation simply takes two random parents and then for each demand
        selects random solution from either of the parents.
        :param parents: population of parents to choose from
        :return: population of children
        """


class OptonetMutation(BaseMutationHandler):
    """
    BaseMutationHandler implementation for the problem of satisfying demand in optical network.
    """
    def mutate(self, population):
        """
        Mutate given population. This implementation of mutation takes a chromosome and decides to mutate each
        gene with some probability. If the gene is to be mutated, then its chosen path is chosen randomly from all
        the paths and the card is also randomized.
        :param population: population to mutate
        :return: mutated population
        """


class OptonetSelector(BaseSelectionHandler):
    """
    BaseSelectionHandler implementation for the problem of satisfying demand in optical network.
    """
    def choose_parents(self, population):
        """
        Choose parents from given population. This implementation chooses best 10% of chromosomes as a possible parents.
        :param population: population to choose parents from.
        :return: possible parents of the next generation
        """

