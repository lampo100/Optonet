import statistics


class StatsLogger:
    def __init__(self):
        self.stats = {}

    def log_stats(self, generation, population):
        mean_fitness = statistics.mean((x.fitness for x in population))
        fitness_scores = [x.fitness for x in population]
        max_fitness = max(fitness_scores)
        min_fitness = min(fitness_scores)
        std = statistics.stdev((x.fitness for x in population))

        self.stats[generation] = {'mean': mean_fitness, 'max': max_fitness, 'min': min_fitness, 'std': std}

