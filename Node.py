"""
Created by Shinrod at 08/05/2020
"""
from Params import *
from numpy import e

class Node:
    """
    Nodes as described in http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf (Fig. 2)
    """
    # Constants
    SENSOR = SENSOR
    HIDDEN = HIDDEN
    OUTPUT = OUTPUT

    def __init__(self, kind : int, name : int):
        """
        Make a new Node.

        :param kind: Node.SENSOR, Node.HIDDEN or Node.OUTPUT
        """
        self.kind = kind
        self.name = name

        self.inward_connections = []
        self.outward_connections = []

        self.value = 0
        self.triggered = False

    def think(self):
        """
        Use the node to make computations
        """
        if self.kind != Node.SENSOR:
            input_sum = 0
            for con in self.inward_connections:
                input_sum += con.node_in.value * con.weight
            self.value = Node.sigmoid(input_sum)

        self.triggered = True

    @staticmethod
    def sigmoid(x):
        return 1/(1+e**(-4.9*x))

    # ------------------------------------------------ TOOL ------------------------------------------------------------
    def clone(self):
        """
        Make a copy of that Node

        The 'outward_connections' attribute isn't copied by this.
        It has to be rebuilt when making the copies of the connections.

        Used by :
        Genome.clone()

        :return: a copy of that node
        """
        return self.__class__(self.kind, self.name)


    def __eq__(self, other):
        """
        Check the name equality between two Node

        Called by :
        self == other

        Used by :
        Genome.clone()
        Connection.__eq__()

        :param other: other Node

        :return: True if the name between the two is the same, False otherwise
        """
        return self.name == other.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return str(self.__repr__())