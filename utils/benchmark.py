import time
from plotter.plotter import visualize_evolution


def benchmark_evolution(evolution_handler, gen_iters, stats_counter, stats_filename, fitness_plot_name, stop_when_solution_found=True):
        """
        Benchmark evolution and
        :param evolution_handler: evolution handler to benchmark
        :param gen_iters: number of evolution generations
        :param fitness_plot_name: name of the file to save the plot to
        :param stop_when_solution_found: should the evolution stop when the solution is found
        """
        print('Start benchmarking {}'.format(evolution_handler))
        start = time.time()
        for i in range(gen_iters):
            evolution_handler.evolve()
            if stop_when_solution_found and evolution_handler.stop_condition_satisfied():
                break
        stop = time.time()
        print("Stop benchmark")

        with open(stats_filename, 'w') as stats_file:
            stats_file.write("Time: {}\n".format(stop - start))
            stats_file.write("Stats: \n{}\n".format(evolution_handler.get_best_chromosome().stats()))

        visualize_evolution(stats_counter.stats, fitness_plot_name)
