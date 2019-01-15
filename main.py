from optonet.genetic import EvolutionHandler
from optonet.model_parser import parse_xml
from optonet.optonet_evolution import initialize_optonet_population, OptonetCrossover, OptonetMutation, \
    OptonetFittestFractionSelector, \
    OptonetReplacer, OptonetTournamentSelector, OptonetRouletteWheelSelector
from optonet.stats_counter import StatsLogger
from utils.benchmark import benchmark_evolution

if __name__ == '__main__':
    janos_us = parse_xml('network_instances/janos-us.xml')  # currently demands have awkwardly similar paths i.e. the same starting links and only different at the end, might want to change this later
    polska = parse_xml('network_instances/polska.xml')

    initial_population = initialize_optonet_population(janos_us, 300)
    sc1 = StatsLogger()
    sc2 = StatsLogger()
    sc3 = StatsLogger()
    configs_to_benchmark = [[initial_population, OptonetFittestFractionSelector(), OptonetMutation(), OptonetCrossover(), OptonetReplacer(), sc1, {'debug':False}],
                            [initial_population, OptonetTournamentSelector(40, 50, 0.9), OptonetMutation(), OptonetCrossover(), OptonetReplacer(), sc2, {'debug':False}],
                            [initial_population, OptonetRouletteWheelSelector(40), OptonetMutation(), OptonetCrossover(), OptonetReplacer(), sc3, {'debug':False} ]]

    benchmark_evolution(EvolutionHandler(*configs_to_benchmark[0]), 200, sc1, fitness_plot_name='docs/fraction.png')
    benchmark_evolution(EvolutionHandler(*configs_to_benchmark[1]), 200, sc2, fitness_plot_name='docs/tournament.png')
    benchmark_evolution(EvolutionHandler(*configs_to_benchmark[2]), 200, sc3, fitness_plot_name='docs/roulette.png')
