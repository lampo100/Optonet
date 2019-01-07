class Chromosome:
    '''
    DemandSolution holds information about possible solution to some given data demand
    '''
    def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness
        self.Age = 0
