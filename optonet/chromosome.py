from abc import ABC, abstractmethod

class Chromosome(ABC):
    """
    Chromosome represents generic chromosome used in evolutionary algorithm
    """


class OptonetGene:
    """
    OptonetGene represents solution to one demand in optical network
    """
    def __init__(self, demand, paths, chosen_path, chosen_card):
        """
        Return initialized instance of OptonetGene
        :param demand: value of the data demand
        :param paths: all paths that can be used to satisfy this demand
        :param chosen_path: path chosen to use for this demand
        :param chosen_card: chosen transponder card to use for this demand
        """
        self.demand = demand
        self.paths = paths
        self.chosen_path = chosen_path
        self.chosen_card = chosen_card


class OptonetChromosome(Chromosome):
    """
    OptonetChromosome represents chromosome encoding solution to problem of finding optimal data flow in optical network
    """
    def __init__(self, genes):
        """
        Each gene includes solution to one demand
        :param genes:
        """
        self.__genes = genes
