"""
Todo : Identify recurrent connections
Currently recurrent connections are defined by the calling order in the 'think' method

Created by Shinrod at 08/05/2020
"""
from Connection import Connection
from Node import Node
from Params import *
import numpy as np
from Queue import PriorityQueue



class Genome:
    """
    A genome is a list of Node and Connection.

    As described in http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf (Fig. 2)
    """

    def __init__(self,
                 inputs : int = 1,
                 outputs : int = 1,
                 first_connections = 1,
                 innovation_history = None,
                 __other = None):
        """
        Make a new Genome.

        You should always use a Population to initiate the genomes and not the genome constructor.
        If you still want to make a single genome, without using a Population use :
        genome = Genome(inputs, outputs)

        or, if you want the NNs to start with n connections, use :
        genome = Genome(inputs, outputs, first_connections)


        The __other argument is used to clone a Genome and should not be used with the other arguments.

        :param inputs: # of inputs
        :param outputs: # of outputs
        :param first_connections: # of connections the NN is starting with (must be between 0 and inputs included)

        :param __other: Use that parameter alone to clone a Genome
        """
        if __other is None:
            # Make a new Genome
            self.input = [Node(Node.SENSOR, i) for i in range(inputs)]
            self.bias = Node(Node.SENSOR, inputs)
            self.output = [Node(Node.OUTPUT, inputs + 1 + i) for i in range(outputs)]
            self.hidden = []
            self.standard_connections = []
            self.bias_connections = []

            # Link the bias to the outputs
            for i, output in enumerate(self.output):
                self.bias_connections.append(Connection(self.bias, output, innovation_number=None))

            # Add the # of connections we want the genome to start with
            if innovation_history is None:
                innovation_history = []
            for _ in range(first_connections):
                self.mutation_add_connection(innovation_history, first_node_pool=self.input)
        else:
            # Clone __other
            self.input = [node.clone() for node in __other.input]
            self.hidden = [node.clone() for node in __other.hidden]
            self.output = [node.clone() for node in __other.output]

            # Make the connections
            old_nodes = __other.input + __other.hidden + __other.output
            nodes = self.input + self.hidden + self.output
            self.connections = []

            # Go through all the nodes, find the old connection and make a new one using the new nodes
            for i, old_node_in in enumerate(old_nodes):
                node_in = nodes[i]
                for old_con in old_node_in.outward_connections:
                    node_out = nodes[nodes.index(old_con.node_out)]
                    self.connections.append(old_con.clone(node_in, node_out))


    # ----------------------------------------------- THINK ------------------------------------------------------------
    def think(self, inputs):
        """
        Use the neural network

        :param inputs: inputs given to the network

        :return: the result of the neural network evaluation
        """
        # 1st step : inputs & bias
        queue = PriorityQueue()
        for i, node in enumerate(self.input):
            node.value = inputs[i]
            queue.put(node, 0)
        self.bias.value = 1
        queue.put(self.bias, 0)

        # 2nd step : launch the evaluation !
        while queue:
            node = queue.get()
            print(node)
            node.think()
            for con in node.outward_connections:
                target = con.node_out
                if not target.triggered:
                    queue.put(target, -1)

        return [node.value for node in self.output]



    # ----------------------------------------------- MUTATE -----------------------------------------------------------
    def mutate(self, innovation_history):
        """
        Mutate.

        There are two mutations :
        - Connection mutation, which adds a new Connection
        - Structural mutation, which adds a new Node

        :return: None
        """
        if np.random.rand() < MUTATION_CHANGE_ALL_WEIGHT:
            for con in self.connections:
                con.mutate()

        if np.random.rand() < MUTATION_CHANCE_ADD_CONNECTION:
            self.mutation_add_connection(innovation_history)

        if np.random.rand() < MUTATION_CHANCE_ADD_NODE:
            self.mutation_add_node(innovation_history)


    def mutation_add_connection(self, innovation_history, first_node_pool = None):
        """
        Make a new connection between two nodes that weren't connected before

        :return: that new connection, or None if no connection have been found
        """
        if first_node_pool is None:
            first_nodes_list = self.input + self.hidden + self.output
        else:
            first_nodes_list = first_node_pool
        np.random.shuffle(first_nodes_list)
        # Take the first node amongst the input and hidden nodes
        for first_node in first_nodes_list:
            second_node = self.find_connectable_node(first_node)
            if second_node is not None:
                new_connection = Connection(first_node, second_node)
                self.standard_connections.append(new_connection)
                # Check what innovation number it should have
                try:
                    index = innovation_history.index(new_connection)
                except ValueError:
                    # It's a new connection never made before
                    new_connection.innovation_number = Connection.global_innovation_number
                    Connection.global_innovation_number += 1
                    innovation_history.append(new_connection)
                else:
                    # It's a connection that has been made before
                    new_connection.innovation_number = innovation_history[index]
                return new_connection
        # If it didn't find any two unconnected nodes
        return None


    def find_connectable_node(self, first_node):
        """
        Find a node (2) that can be connected to the first_node (1) with a connection (1) -> (2)

        :param first_node: beginning of the connection

        :return: a node (2) that can be connected to first_node (1) with a connection (1) -> (2)
        """
        # Take the second node amongst the hidden and output nodes that are not linked to the first one
        non_linked = self.hidden + self.output
        for con in first_node.outward_connections:
            # con.node_out is forced to be in that list
            # - It is amongst the hidden and output nodes
            # - It has not been removed before because two connections can't have the same input AND output
            non_linked.remove(con.node_out)
        if non_linked:
            # If it can find a non-linked node, then it's done !
            second_node = np.random.choice(non_linked)
            return second_node
        else:
            return None


    def mutation_add_node(self, innovation_history):
        """
        Create a new Node from a Connection

        It does those steps :
        - Take a connection which has a input Node (i) and output Node (o) and a weight of (w)
        - Disable it
        - Make a new Node (n)
        - Make a new Connection (i) -> (n) with a weight of 1
        - Make a new Connection (n) -> (i) with a weight of (w)

        :return: that new Node
        """
        con : Connection = np.random.choice(self.connections)
        con.enabled = False
        node = Node(Node.HIDDEN, con.innovation_number)
        self.hidden.append(node)
        self.standard_connections.append(Connection(con.node_in, node, con.weight))
        self.standard_connections.append(Connection(node, con.node_out, con.weight))
        return node

    # ------------------------------------------------ TOOL ------------------------------------------------------------
    def clone(self):
        """
        Make a deepcopy of this Genome

        :return: a deepcopy of this Genome
        """
        return self.__class__(__other=self)


    # ------------------------------------------------ DRAW ------------------------------------------------------------
    def draw(self):
        """
        Draw the genome using graphviz

        :return: None
        """
        import graphviz as gv
        graph = gv.Digraph("Genome", format='svg')
        # Make the graph go from left to right
        graph.attr(rankdir='LR')

        # Draw the Nodes
        for node in self.input + self.hidden + self.output:
            graph.node(str(node),
                       rank = node_rank[node.kind],
                       color=node_color[node.kind],
                       shape='circle',
                       width = '0.3')

        # Draw the Connections
        no_connection = True
        for con in self.standard_connections:
            if con.enabled and con.weight != 0:
                if con.weight < 0:
                    color = "0 " + str(0.5 - con.weight / 2) + " 0.7"
                else:
                    color = "0.3333 " + str(0.5 + con.weight / 2) + " 0.7"
                graph.edge(str(con.node_in),
                           str(con.node_out),
                           str(con.innovation_number),
                           color=color,
                           edgetooltip=str(round(con.weight, 3)),
                           penwidth=str(abs(con.weight * 1.5) + 0.2))

        if no_connection:
            # If there is no connection, make a dummy connection so that the input and output are displayed properly
            graph.edge(str(self.input[int(len(self.input)/2)]),
                       str(self.output[int(len(self.output)/2)]),
                       style='invis')

        graph.render(view=True)


# ---------------------------------------------------- TEST ------------------------------------------------------------
if __name__ == '__main__':
    g = Genome(3, 1, first_connections=3)
    print(g.think([0.1,0.1,0.1]))
    g.draw()


