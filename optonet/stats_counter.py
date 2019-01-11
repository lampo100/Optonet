
class StatsCounter:

    def __init__(self):
        self.generation_stats = []

    def count_stats(self, generation, population):
        # avg fitness
        avg_fitness = sum((chromosome.fitness for chromosome in population)) / len(population)
        valid_chromosomes = [chromosome for chromosome in population if chromosome.penalty == 0]
        if len(valid_chromosomes) == 0:
            best_cost = 0
        else:
            best_cost = 1 / max(chromosome.fitness for chromosome in valid_chromosomes)
        valid_percent = len(valid_chromosomes) / len(population)

        self.generation_stats.append(Stats(avg_fitness, 0, best_cost, valid_percent))


class Stats:

    def __init__(self, average_fitness, average_link_usage, best_valid_solution_cost, valid_solution_chromosome_percent):
        self.average_fitness = average_fitness
        self.average_link_usage = average_link_usage
        self.best_valid_solution_cost = best_valid_solution_cost
        self.valid_solution_chromosomes_percent = valid_solution_chromosome_percent
