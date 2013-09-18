'''
 Copyright (C) 2013 onwards University of Deusto
  
 All rights reserved.
 
 This software is licensed as described in the file COPYING, which
 you should have received as part of this distribution.
 
 This software consists of contributions made by many individuals, 
 listed below:
 
 @author: Aitor Gómez Goiri <aitor.gomez@deusto.es>
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
            # TODO optimization: store the used templates to avoid repetition