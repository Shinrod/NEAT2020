"""
Created by Shinrod at 08/05/2020
"""
from Params import SENSOR, HIDDEN, OUTPUT

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

        self.outward_connections = []


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

        :param other: other Node

        :return: True if the name between the two is the same, False otherwise
        """
        return self.name == other.name