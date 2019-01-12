from abc import ABC, abstractmethod

from optonet.penalty import DefaultPenaltyCalculator


class Chromosome(ABC):
    """
    Chromosome represents generic chromosome used in evolutionary algorithm
    """


class OptonetGene:
    """
    OptonetGene represents solution to one demand in optical network
    """
    def __init__(self, demand, chosen_path, chosen_card):
        """
        Return initialized instance of OptonetGene
        :param demand: value of the data demand
        :param paths: all paths that can be used to satisfy this demand
        :param chosen_path: path chosen to use for this demand
        :param chosen_card: chosen transponder card to use for this demand
        """
        self.demand = demand
        self.chosen_path = chosen_path
        self.chosen_card = chosen_card


class OptonetChromosome(Chromosome):
    """
    OptonetChromosome represents chromosome encoding solution to problem of finding optimal data flow in optical network
    """
    def __init__(self, genes, penalty_calculator=DefaultPenaltyCalculator()):
        """
        Each gene includes solution to one demand
        :param genes:
        """
        self.genes = genes
        self.penalty_calculator = penalty_calculator
        self.fitness = self.calc_fitness()

    def calc_fitness(self):
        node_to_cost = dict()
        link_to_lambdas_used = dict()

        for gene in self.genes:
            source = gene.demand.first_node
            target = gene.demand.second_node
            node_to_cost[source] = node_to_cost.get(source, 0) + gene.chosen_card.cost
            node_to_cost[target] = node_to_cost.get(target, 0) + gene.chosen_card.cost

            for link in gene.chosen_path:
                link_to_lambdas_used[link] = link_to_lambdas_used.get(link, 0)\
                                             + gene.chosen_card.necessary_lambdas(gene.demand.value)

        cost = sum(node_to_cost.values())

        return 1 / (cost + self.penalty)

    @property
    def penalty(self):
        used_wavelengths_count = dict()
        for gene in self.genes:
            for link in gene.chosen_path:
                used_wavelengths_count[link] = used_wavelengths_count.get(link, 0) \
                                               + gene.chosen_card.necessary_lambdas(gene.demand.value)
        return self.penalty_calculator.calc_penalty(used_wavelengths_count)


    @property
    def penalty(self):
        used_wavelengths_count = dict()
        for gene in self.genes:
            for link in gene.chosen_path:
                used_wavelengths_count[link] = used_wavelengths_count.get(link, 0) \
                                               + gene.chosen_card.necessary_lambdas(gene.demand.value)
        return self.penalty_calculator.calc_penalty(used_wavelengths_count)


    def stats(self):
        node_to_cost = dict()
        link_to_lambdas_used = dict()

        for gene in self.genes:
            source = gene.demand.first_node
            target = gene.demand.second_node
            node_to_cost[source] = node_to_cost.get(source, 0) + gene.chosen_card.cost
            node_to_cost[target] = node_to_cost.get(target, 0) + gene.chosen_card.cost

            for link in gene.chosen_path:
                link_to_lambdas_used[link] = link_to_lambdas_used.get(link, 0) \
                                             + gene.chosen_card.necessary_lambdas(gene.demand.value)

        cost = sum(node_to_cost.values())
        penalty = self.penalty_calculator.calc_penalty(link_to_lambdas_used)

        return """cost : {}
                penalty: {}
                Cost of transponder cards: {}
                Wavelengths used at connections: {}""".format\
                (
                cost,
                penalty,
                node_to_cost,
                link_to_lambdas_used
                )
