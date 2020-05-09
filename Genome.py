"""
Created by Shinrod at 08/05/2020
"""
from builtins import enumerate

from Connection import Connection
from Node import Node
from Params import node_rank, node_color
import numpy as np

class Genome:
    """
    A genome is a list of Node and Connection.

    As described in http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf (Fig. 2)
    """

    def __init__(self,
                 inputs : int = 1,
                 outputs : int = 1,
                 first_connections = 1,
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
            self.output = [Node(Node.OUTPUT, inputs + i) for i in range(outputs)]
            self.hidden = []
            self.connections = []
            for _ in range(first_connections):
                self.connections.append(Connection(np.random.choice(self.input),
                                                   np.random.choice(self.output)))
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
                    self.connections.append(Connection(node_in,
                                                       node_out,
                                                       old_con.weight,
                                                       old_con.innovation_number))

            
    
    def mutation_add_connection(self):
        """
        Make a new connection between two nodes that weren't connected before

        :return: that new connection, or None if no connection have been found
        """
        first_nodes_list = self.input + self.hidden + self.output
        np.random.shuffle(first_nodes_list)
        # Take the first node amongst the input and hidden nodes
        for first_node in first_nodes_list:
            second_node = self.find_connectable_node(first_node)
            if second_node is not None:
                new_connection = Connection(first_node, second_node)
                self.connections.append(new_connection)
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
            # con.output is forced to be in that list
            # - It is amongst the hidden and output nodes
            # - It has not been removed before because two connections can't have the same input AND output
            non_linked.remove(con.output)
        if non_linked:
            # If it can find a non-linked node, then it's done !
            second_node = np.random.choice(non_linked)
            return second_node
        else:
            return None


    def mutation_add_node(self):
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
        node = Node(Node.HIDDEN)
        self.hidden.append(node)
        self.connections.append(Connection(con.node_in, node, con.weight))
        self.connections.append(Connection(node, con.node_out, con.weight))
        return node


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
            graph.node(str(node.id),
                       rank = node_rank[node.kind],
                       color=node_color[node.kind],
                       shape='circle',
                       width = '0.3')

        # Draw the Connections
        no_connection = True
        for con in self.connections:
            if con.enabled and con.weight != 0:
                if con.weight < 0:
                    color = "0 " + str(0.5 - con.weight / 2) + " 0.7"
                else:
                    color = "0.3333 " + str(0.5 + con.weight / 2) + " 0.7"
                graph.edge(str(con.node_in.id),
                           str(con.node_out.id),
                           str(con.innovation_number),
                           color=color,
                           edgetooltip=str(round(con.weight, 3)),
                           penwidth=str(abs(con.weight * 1.5) + 0.2))

        if no_connection:
            # If there is no connection, make a dummy connection so that the input and output are displayed properly
            graph.edge(str(self.input[int(len(self.input)/2)].id),
                       str(self.output[int(len(self.output)/2)].id),
                       style='invis')

        graph.render(view=True)


# ---------------------------------------------------- TEST ------------------------------------------------------------
if __name__ == '__main__':
    g = Genome(3, 1)
    g.draw()


