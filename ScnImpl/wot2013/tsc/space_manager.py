'''
 Copyright (C) 2013 onwards University of Deusto
  
 All rights reserved.
 
 This software is licensed as described in the file COPYING, which
 you should have received as part of this distribution.
 
 This software consists of contributions made by many individuals, 
 listed below:
 
 @author: Aitor Gómez Goiri <aitor.gomez@deusto.es>
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