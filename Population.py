"""
Population gathering multiple genomes

Created by Shinrod at 09/05/2020
"""
from Genome import Genome


class Population:
    """
    Population gathering multiple genomes
    """

    def __init__(self,
                 demography : int = None,
                 inputs : int = None,
                 outputs : int = None,
                 first_connections : int = 1,
                 __other = None):
        """
        Make a Population.

        To make a new Population use :
        pop = Population(demography, inputs, outputs)

        or, if you want the NNs to start with n connections, use :
        pop  = Population(demography, inputs, outputs, n)


        The __other argument is used to clone a Population and should not be used with the other arguments.

        :param demography: # of people in the population
        :param inputs: # of inputs in the neural network
        :param outputs: # of outputs in the neural network
        :param first_connections: # of connections the NN is starting with (must be between 0 and inputs included)

        :param __other: Use that parameter alone to clone a Population
        """
        if __other is None:
            # Create a brand new population
            self.demography = demography
            self.people = [Genome(inputs, outputs, first_connections) for _ in range(demography)]
        else:
            # Clone that population
            self.demography = __other.demography
            self.people = [genome.clone() for genome in __other.people]


    def clone(self):
        """
        Make a deepcopy of that Population
        """
        return self.__class__(__other=self)