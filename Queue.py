"""
A custom queue

Created by Shinrod at 06/07/2018
"""

class PriorityQueue:
    """
    Priority queue where the element with the highest priority leaves first
    """

    def __init__(self):
        """
        Make a new Priority Queue
        """
        # self.queue contains the items
        self.queue = []
        self.priority = {}

    def put(self, item, priority):
        """
        Put an item in the queue

        :param item: Item you put in the queue
        :param priority: Priority of the item in the queue (Higher priority is taken first)
        """
        if item in self.queue:
            self.queue.remove(item)
        self.queue.append(item)
        self.priority[str(item)] = priority

    def get(self):
        """
        Return the item with the highest priority
        If two elements have the same priority, the oldest is chosen
        """
        priorityMax = self.priority[str(self.queue[0])]
        index = 0
        for i, item in enumerate(self.queue[1:]):
            if self.priority[str(item)] > priorityMax:
                priorityMax = self.priority[str(item)]
                index = i+1
        return self.queue.pop(index)

    def empty(self):
        """
        Tell if the queue is empty or not
        """
        return len(self.queue) == 0

    def __bool__(self):
        """
        Like python list, returns False if it's empty
        """
        return not self.empty()