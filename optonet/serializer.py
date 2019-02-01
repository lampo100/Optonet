import pickle

def serialize(population, output_file):
    """
    Serialize given population to file
    :param population:
    :param output_file:
    :return:
    """
    with open(output_file, 'wb') as file:
        pickle.dump(population, file)



def deserialize(input_file):
    """
    Deserialize a population from given file
    :param input_file:
    :return: population
    """
    with open(input_file, 'rb') as file:
        return pickle.load(file)