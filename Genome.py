"""
Created by Shinrod at 08/05/2020
"""
from Connection import Connection
from Node import Node
import numpy as np

class Genome:
    """
    A genome is a list of Node and Connection.

    As described in http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf (Fig. 2)
    """

    def __init__(self, inputs : int, outputs : int, random_connection = True):
        """
        Make a new Genome.

        At the beginning, the Genome is MINIMAL : only 1 connection exists

        :param inputs: # of inputs
        :param outputs: # of outputs
        :param random_connection: true : add a random connection between an input and output node; false : no connection
        """
        self.inputs = [Node() for _ in range(inputs)]
        self.outputs = [Node() for _ in range(outputs)]
        self.hidden = []
        self.connections = []
        if random_connection:
            self.connections.append(Connection(np.random.choice(self.inputs, 1), np.random.choice(self.outputs, 1)))
            
    
    def add_connection(self):
        """
        Make a new connection between two nodes that weren't connected before

        :return:
        """
