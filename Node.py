"""
Created by Shinrod at 08/05/2020
"""

class Node:
    """
    Nodes as described in http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf (Fig. 2)
    """
    # Node types
    SENSOR = 0
    HIDDEN = 1
    OUTPUT = 2

    def __init__(self, type : int):
        """
        Make a new Node.

        :param type: SENSOR, HIDDEN or OUTPUT
        """
        self.type = type
        self.id = None

