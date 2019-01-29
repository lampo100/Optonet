from optonet.genetic import EvolutionHandler
from optonet.model_parser import parse_xml
from optonet.optonet_evolution import initialize_optonet_population, OptonetCrossover, OptonetMutation, \
    OptonetFittestFractionSelector, \
    OptonetReplacer, OptonetTournamentSelector, OptonetRouletteWheelSelector
from optonet.stats_counter import StatsLogger
from utils.benchmark import benchmark_evolution
from optonet.serializer import serialize

if __name__ == '__main__':
    #janos_us = parse_xml('network_instances/janos-us.xml')  # currently demands have awkwardly similar paths i.e. the same starting links and only different at the end, might want to change this later
    polska = parse_xml('network_instances/polska.xml')

    initial_population = initialize_optonet_population(polska, 3000)
    sc1 = StatsLogger()
    sc2 = StatsLogger()
    sc3 = StatsLogger()
    configs_to_benchmark = [[initial_population, OptonetFittestFractionSelector(), OptonetMutation(), OptonetCrossover(), OptonetReplacer(), sc1, {'debug':True}],
                            [initial_population, OptonetTournamentSelector(40, 50, 0.9), OptonetMutation(), OptonetCrossover(), OptonetReplacer(), sc2, {'debug':True}],
                            [initial_population, OptonetRouletteWheelSelector(40), OptonetMutation(), OptonetCrossover(), OptonetReplacer(), sc3, {'debug':True} ]]

    #benchmark_evolution(EvolutionHandler(*configs_to_benchmark[0]), 150, sc1, stats_filename='docs/all_256/stats_fraction.txt', fitness_plot_name='docs/all_256/fraction.png')
    benchmark_evolution(EvolutionHandler(*configs_to_benchmark[1]), 1000, sc2, stats_filename='docs/pol_3_lib_32/stats_tournament.txt', fitness_plot_name='docs/pol_3_lib_32/tournament.png')
    #benchmark_evolution(EvolutionHandler(*configs_to_benchmark[2]), 300, sc3, stats_filename='docs/all_256/stats_roulette.txt', fitness_plot_name='docs/all_256/roulette.png')
