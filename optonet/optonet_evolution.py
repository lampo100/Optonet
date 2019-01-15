import random
from operator import attrgetter
from typing import List

from optonet.chromosome import OptonetChromosome, OptonetGene
from optonet.consts import TRANSPONDER_CARDS
from .genetic import BaseCrossoverHandler, BaseMutationHandler, BaseSelectionHandler, BaseReplacementHandler


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
        children = []
        for parent1, parent2 in self._list_to_random_pairs(parents):
            chld1, chld2 = self._do_crossover(parent1, parent2)
            children.append(chld1)
            children.append(chld2)
        return children

    def _do_crossover(self, parent1: OptonetChromosome, parent2: OptonetChromosome):
        cutting_point = int(len(parent1.genes) / 2)
        child1_genes = []
        child2_genes = []
        for gene_index in range(len(parent1.genes)):
            if gene_index < cutting_point:
                child1_genes.append(parent1.genes[gene_index])
                child2_genes.append(parent2.genes[gene_index])
            else:
                child1_genes.append(parent2.genes[gene_index])
                child2_genes.append(parent1.genes[gene_index])

        return OptonetChromosome(child1_genes, parent1.penalty_calculator), OptonetChromosome(child2_genes, parent1.penalty_calculator)

    def _list_to_random_pairs(self, lst):
        pairs = []
        while len(lst) >= 2:
            rand1 = lst.pop(random.randrange(0, len(lst)))
            rand2 = lst.pop(random.randrange(0, len(lst)))
            pairs.append((rand1, rand2))

        return pairs

    def __repr__(self):
        return "Simple Crossover"



class OptonetMutation(BaseMutationHandler):

    def __init__(self, mutation_chance=0.1, mutation_card_type_chance=0.5):
        self.__mutation_chance = mutation_chance
        self.__mutation_card_type_chance = mutation_card_type_chance
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
        for index in range(len(population)):
            if random.random() < self.__mutation_chance:
                population[index] = self._do_mutate(population[index])

        return population

    def _do_mutate(self, chromosome):
        mutated_gene_index = random.randrange(0, len(chromosome.genes))
        mutated_gene = chromosome.genes[mutated_gene_index]

        if random.random() < self.__mutation_card_type_chance:
            remaining_transponder_cards = TRANSPONDER_CARDS[:]
            remaining_transponder_cards.remove(mutated_gene.chosen_card)
            new_used_card = random.choice(remaining_transponder_cards)
            chromosome.genes[mutated_gene_index] = OptonetGene(mutated_gene.demand, mutated_gene.chosen_path, new_used_card)
        else:
            remaining_paths = mutated_gene.demand.paths[:]
            remaining_paths.remove(mutated_gene.chosen_path)
            new_used_path = random.choice(remaining_paths)
            chromosome.genes[mutated_gene_index] = OptonetGene(mutated_gene.demand, new_used_path, mutated_gene.chosen_card)

        return chromosome

    def __repr__(self):
        return "Simple Mutation(mutation_chance={}; card_mutation_chance={})".format(self.__mutation_chance, self.__mutation_card_type_chance)


class OptonetFittestFractionSelector(BaseSelectionHandler):

    def __init__(self, best_fraction=0.1):
        self.__best_fraction = best_fraction
    """
    BaseSelectionHandler implementation for the problem of satisfying demand in optical network.
    """
    def choose_parents(self, population: List[OptonetChromosome]):
        """
        Choose fraction of best chromosomes from current population as parents.
        :param population: population to choose parents from.
        :return: possible parents of the next generation
        """
        how_many = int(self.__best_fraction * len(population))
        return sorted(population, key=lambda x: x.fitness, reverse=True)[:how_many]

    def __repr__(self):
        return "Fitness Fraction Selector(best_fraction={})".format(self.__best_fraction)


class OptonetRouletteWheelSelector(BaseSelectionHandler):

    def __init__(self, parents_number):
        self.__parents_number = parents_number

    def choose_parents(self, population: List[OptonetChromosome]):
        fitness_sum = sum(chromosome.fitness for chromosome in population)
        current_fitness_accumulation = 0
        parents = []

        for i in range(self.__parents_number):
            wheel_result = random.uniform(0, fitness_sum)
            for chromosome in population:
                if current_fitness_accumulation + chromosome.fitness >= wheel_result:
                    parents.append(chromosome)
                    current_fitness_accumulation = 0
                    break
                else:
                    current_fitness_accumulation += chromosome.fitness

        return parents

    def __repr__(self):
        return "Roulette Selector"


class OptonetTournamentSelector(BaseSelectionHandler):

    def __init__(self, parents_number, tournament_size, fittest_chromosome_win_chance):
        self.__fittest_chromosome_win_chance = fittest_chromosome_win_chance
        self.__parents_number = parents_number
        self.__tournament_size = tournament_size

    def choose_parents(self, population):
        parents = []
        for i in range(self.__parents_number):
            participants = random.sample(population, self.__tournament_size)
            chromosome_fittest_to_least_fittest = sorted(participants, key=lambda x: x.fitness, reverse=True)
            for index, chromosome in enumerate(chromosome_fittest_to_least_fittest):
                tournament_random_value = random.uniform(0, 1)
                if (self.__fittest_chromosome_win_chance > tournament_random_value) or index == len(population)-1:
                    parents.append(chromosome)
                    break
        return parents

    def __repr__(self):
        return "Tournament Selector(tournament_size={}; win_chance={})".format(self.__tournament_size, self.__fittest_chromosome_win_chance)


class OptonetReplacer(BaseReplacementHandler):

    def replace_generation(self, old_population, offsprings):
        not_replaced_length = len(old_population) - len(offsprings)
        return sorted(old_population, key=lambda x: x.fitness, reverse=True)[:not_replaced_length] + offsprings


def initialize_optonet_population(network, population_size):
    population = []
    for i in range(population_size):
        genes = []
        for demand in network.demands:
            genes.append(OptonetGene(demand, random.choice(demand.paths), random.choice(TRANSPONDER_CARDS)))
        population.append(OptonetChromosome(genes))

    return population
