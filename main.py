from optonet.genetic import EvolutionHandler
from optonet.model_parser import parse_xml
from optonet.optonet_evolution import initialize_optonet_population, OptonetCrossover, OptonetMutation, \
    OptonetFittestFractionSelector, \
    OptonetReplacer, OptonetTournamentSelector, OptonetRouletteWheelSelector
from optonet.stats_counter import StatsLogger
from plotter.plotter import visualize_evolution
import time

if __name__ == '__main__':
    janos_us = parse_xml('network_instances/janos-us.xml')  # currently demands have awkwardly similar paths i.e. the same starting links and only different at the end, might want to change this later
    polska = parse_xml('network_instances/polska.xml')

    initial_population = initialize_optonet_population(janos_us, 300)
    selection_handler = OptonetTournamentSelector(40, 50, 0.9)
    mutation_handler = OptonetMutation()
    crossover_handler = OptonetCrossover()
    replacement_handler = OptonetReplacer()
    config = {'debug': True}

    default_selection_stats = StatsLogger()
    evolution = EvolutionHandler(initial_population, selection_handler, mutation_handler, crossover_handler, replacement_handler, default_selection_stats, config)
    start = time.time()
    for i in range(30):
        evolution.evolve()
        if evolution.stop_condition_satisfied():
            break
    end = time.time()
    print('time: {}'.format(end - start))
    visualize_evolution(default_selection_stats.stats)

    # print(50 * '-')
    # tournament_selection_handler = OptonetTournamentSelector(40, 50, 0.9)
    # tournament_selection_stats = StatsLogger()
    # evolution2 = EvolutionHandler(initial_population, tournament_selection_handler, mutation_handler, crossover_handler, replacement_handler, tournament_selection_stats, config)
    # for i in range(200):
    #     evolution2.evolve()
    # print(50 * '-')
    # roulette_selection_handler = OptonetRouletteWheelSelector(40)
    # roulette_selection_stats = StatsLogger()
    # evolution3 = EvolutionHandler(initial_population, roulette_selection_handler, mutation_handler, crossover_handler,
    #                               replacement_handler, roulette_selection_stats, config)
    # for i in range(200):
    #     evolution3.evolve()
    #
    best_stats = evolution.get_best_chromosome().stats()
    print(best_stats)
