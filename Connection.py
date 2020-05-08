"""
Created by Shinrod at 08/05/2020
"""
from Node import Node
import numpy as np


class Connection:
    """
    Connection between two Node

    As decribed in http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf (Fig. 2)
    """

    # Todo : Make sure weight and id are well used here
    def __init__(self, input : Node, output : Node, id = None):
        """
        Make a new Connection between two Nodes

        :param input: input Node
        :param output: output Node
        """
        self.input = input
        self.input = output
        # Random weight between -1 and 1
        self.weight = 2 * np.random.rand() - 1
        self.enabled = True
        self.id = id

    def weight_mutation(self):
        # Todo : fill here
        pass


if __name__ == '__main__':
    node0 = Node(Node.SENSOR)
    node1 = Node(Node.OUTPUT)
    con0 = Connection(node0, node1)
    con1 = Connection(node0, node1)
    print(con0.weight)
    print(con1.weight)