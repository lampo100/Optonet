from optonet.genetic import EvolutionHandler
from optonet.model_parser import parse_xml
from optonet.optonet_evolution import initialize_optonet_population, OptonetCrossover, OptonetMutation, OptonetSelector, \
    OptonetReplacer
from plotter.plotter import visualize_network


if __name__ == '__main__':
    janos_us = parse_xml('network_instances/janos-us.xml')  # currently demands have awkwardly similar paths i.e. the same starting links and only different at the end, might want to change this later
    polska = parse_xml('network_instances/polska.xml')

    initial_population = initialize_optonet_population(polska, 1000)
    selection_handler = OptonetSelector()
    mutation_handler = OptonetMutation()
    crossover_handler = OptonetCrossover()
    replacement_handler = OptonetReplacer()
    config = {'debug': True}
    evolution = EvolutionHandler(starting_population=initial_population,
                                 selection_handler=selection_handler,
                                 mutation_handler=mutation_handler,
                                 crossover_handler=crossover_handler,
                                 replacement_handler=replacement_handler,
                                 config=config,
                                 logger=None
                                 )
    for i in range(100):
        evolution.evolve()
        if evolution.stop_condition_satisfied():
            break

    best_stats = evolution.get_best_chromosome().stats()
    print(best_stats)
