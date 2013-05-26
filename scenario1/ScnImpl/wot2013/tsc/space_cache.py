'''
Created on May 21, 2013

@author: tulvur
'''
from rdflib import Graph


class SpaceCache(object):
    
    def __init__(self, space_manager):
        self.space_manager = space_manager
        self.queries = set()
        self.cache = Graph()
    
    def add_query(self, new_query):
        self.queries.add( new_query )
    
    def add_queries(self, new_queries):
        self.queries.union( new_queries )
    
    # this should be done in background as they arrive
    # but to simplify...
    def launch_requests(self):
        for query in self.queries:
            self.cache += self.space_manager.query_tsc(query)