"""
Created by Shinrod at 08/05/2020
"""
from Node import Node
from Params import WEIGHT_LOWER_BOUND, WEIGHT_UPPER_BOUND
import numpy as np


class Connection:
    """
    Connection between two Node

    As decribed in http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf (Fig. 2)
    """

    # Todo : Make sure weight and innovation_number are well used here
    def __init__(self, node_in : Node, node_out : Node, weight = None, innovation_number = None):
        """
        Make a new Connection between two Nodes

        :param node_in: input Node
        :param node_out: output Node
        """
        self.node_in = node_in
        self.node_in.outward_connections.append(self)
        self.node_out = node_out

        if weight is None:
            self.randomize_weight()
        else:
            self.weight = weight

        self.enabled = True
        self.innovation_number = innovation_number

    def weight_mutation(self):
        # Todo : fill here
        pass

    def randomize_weight(self):
        """
        Change the weight for a random weight between Params.WEIGHT_LOWER_BOUND and Params.WEIGHT_UPPER_BOUND

        :return: None
        """
        self.weight = (WEIGHT_UPPER_BOUND - WEIGHT_LOWER_BOUND) * np.random.rand() + WEIGHT_LOWER_BOUND


if __name__ == '__main__':
    node0 = Node(Node.SENSOR, 0)
    node1 = Node(Node.OUTPUT, 1)
    con0 = Connection(node0, node1)
    con1 = Connection(node0, node1)
    print(con0.weight)
    print(con1.weight)