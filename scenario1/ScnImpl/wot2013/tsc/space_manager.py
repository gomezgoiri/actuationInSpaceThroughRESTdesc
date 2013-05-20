'''
Created on May 20, 2013

@author: tulvur
'''
from abc import ABCMeta, abstractmethod


class SpaceManager(object):
    """
    The responsibilities of this manager are threefold:
      - Configures the nodes of the scenario.
      - It also exposes a WhitePage interface to get clues from the space.
      - Consumes the nodes TSC interface on behalf of the actuation starter.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_node(self, facts, rules):
        pass
    
    @abstractmethod
    def get_clues(self):
        pass
    
    @abstractmethod
    def query_tsc(self, template):
        pass