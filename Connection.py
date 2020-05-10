"""
Created by Shinrod at 08/05/2020
"""
from Node import Node
from Params import *
import numpy as np


class Connection:
    """
    Connection between two Node

    As described in http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf (Fig. 2)
    """

    global_innovation_number = 0

    def __init__(self, node_in : Node, node_out : Node, weight = None, innovation_number = None):
        """
        Make a new Connection between two Nodes

        :param node_in: input Node
        :param node_out: output Node
        :param weight: weight of the Connection
        :param innovation_number: historical origin of the connection
        """
        self.node_in = node_in
        self.node_in.outward_connections.append(self)
        self.node_out = node_out
        self.node_out.inward_connections.append(self)

        if weight is None:
            self.randomize_weight()
        else:
            self.weight = weight

        self.enabled = True
        self.innovation_number = innovation_number

    # ----------------------------------------------- MUTATE -----------------------------------------------------------
    def mutate(self):
        """
        Change the weight of this Connection
        """
        if np.random.rand() < MUTATION_NEW_WEIGHT:
            self.randomize_weight()
        else:
            self.change_slightly_weight()


    # ------------------------------------------------ TOOL ------------------------------------------------------------
    def randomize_weight(self):
        """
        Change the weight for a random weight between Params.WEIGHT_LOWER_BOUND and Params.WEIGHT_UPPER_BOUND
        """
        self.weight = (WEIGHT_UPPER_BOUND - WEIGHT_LOWER_BOUND) * np.random.rand() + WEIGHT_LOWER_BOUND

    def change_slightly_weight(self):
        """
        Slightly changes the weight of this Connection.

        It changes according to a normal distribution
        """
        self.weight += np.random.normal(0, SLIGHT_WEIGHT_MUTATION_STD_VAR)

        # Make sure the weight stays between the bounds
        if self.weight > WEIGHT_UPPER_BOUND:
            self.weight = WEIGHT_UPPER_BOUND

        elif self.weight < WEIGHT_LOWER_BOUND:
            self.weight = WEIGHT_LOWER_BOUND


    def clone(self, node_in, node_out):
        """
        Clone this Connection

        Careful, you need to clone the node_in and the node_out first and pass them in the parameters of this method.
        Otherwise there will be some reference issues.

        :param node_in: clone of self.node_in
        :param node_out: clone of self.node_out

        :return: a clone of this Connection
        """
        return Connection(node_in, node_out, self.weight, self.innovation_number)

    def __eq__(self, other):
        """
        Check if the two Connections are linking the same Nodes.

        Called by :
        self == other

        Used by :
        Genome.mutation_add_connection()
        Genome.mutation_add_node()

        :param other: the other Connection

        :return: True if the two are linking the same Nodes, False otherwise
        """
        return self.node_in == other.node_in and self.node_out == other.node_out

# ---------------------------------------------------- TEST ------------------------------------------------------------
if __name__ == '__main__':
    node0 = Node(Node.SENSOR, 0)
    node1 = Node(Node.OUTPUT, 1)
    con0 = Connection(node0, node1)
    con1 = Connection(node0, node1)
    print(con0.weight)
    print(con1.weight)