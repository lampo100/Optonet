from abc import ABC, abstractmethod
from collections import Counter

from optonet.penalty import DefaultPenaltyCalculator


class Chromosome(ABC):
    """
    Chromosome represents generic chromosome used in evolutionary algorithm
    """


class OptonetGene:
    """
    OptonetGene represents solution to one demand in optical network
    """
    def __init__(self, demand, chosen_path, chosen_cards):
        """
        Return initialized instance of OptonetGene
        :param demand: value of the data demand
        :param paths: all paths that can be used to satisfy this demand
        :param chosen_path: path chosen to use for this demand
        :param chosen_cards: chosen transponder cards to use for this demand
        """
        self.demand = demand
        self.chosen_path = chosen_path
        self.chosen_cards = chosen_cards


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
        cost_at_node = dict()

        for gene in self.genes:
            source = gene.demand.first_node
            target = gene.demand.second_node
            cost_at_node[source] = cost_at_node.get(source, 0) + sum((card.cost for card in gene.chosen_cards))
            cost_at_node[target] = cost_at_node.get(target, 0) + sum((card.cost for card in gene.chosen_cards))

        cost = sum(cost_at_node.values())

        return 1 / (cost + self.penalty)

    @property
    def penalty(self):
        used_wavelengths_count = dict()
        for gene in self.genes:
            for link in gene.chosen_path:
                used_wavelengths_count[link] = used_wavelengths_count.get(link, 0) \
                                               + len(gene.chosen_cards)
        return self.penalty_calculator.calc_penalty(used_wavelengths_count)

    def stats(self):
        cost_at_node = dict()
        link_to_lambdas_used = dict()
        cards_at_node = dict()

        for gene in self.genes:
            source = gene.demand.first_node
            target = gene.demand.second_node
            cards_at_node.setdefault(source, Counter([str(card.cost) for card in gene.chosen_cards])).update([str(card.cost) for card in gene.chosen_cards])
            cards_at_node.setdefault(target, Counter([str(card.cost) for card in gene.chosen_cards])).update([str(card.cost) for card in gene.chosen_cards])
            cost_at_node[source] = cost_at_node.get(source, 0) + sum((card.cost for card in gene.chosen_cards))
            cost_at_node[target] = cost_at_node.get(target, 0) + sum((card.cost for card in gene.chosen_cards))
            for link in gene.chosen_path:
                link_to_lambdas_used[link] = link_to_lambdas_used.get(link, 0) \
                                             + len(gene.chosen_cards)

        cost = sum(cost_at_node.values())
        penalty = self.penalty_calculator.calc_penalty(link_to_lambdas_used)

        return """cost : {} penalty: {}\nCost of transponder cards: {}\nCards costs at nodes: {}\nWavelengths used at connections: {}""".format\
                (
                cost,
                penalty,
                cost_at_node,
                cards_at_node,
                link_to_lambdas_used
                )

    def stats2(self):
        cost_at_node = {}
        link_to_lambdas_used = {}
        demands = {}

        for gene in self.genes:
            source = gene.demand.first_node
            target = gene.demand.second_node

            demands.setdefault(source, []).append([target, gene.demand.value])
            cost_at_node[source] = cost_at_node.get(source, 0) + gene.chosen_card.cost
            cost_at_node[target] = cost_at_node.get(target, 0) + gene.chosen_card.cost

            for link in gene.chosen_path:
                link_to_lambdas_used.setdefault(link, []).append([
                    source,
                    target,
                    gene.chosen_card.necessary_lambdas(gene.demand.value)
                ])

        return (demands, cost_at_node, link_to_lambdas_used)