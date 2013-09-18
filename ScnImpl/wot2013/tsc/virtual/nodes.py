'''
 Copyright (C) 2013 onwards University of Deusto
  
 All rights reserved.
 
 This software is licensed as described in the file COPYING, which
 you should have received as part of this distribution.
 
 This software consists of contributions made by many individuals, 
 listed below:
 
 @author: Aitor Gómez Goiri <aitor.gomez@deusto.es>
'''

from rdflib import Graph, RDF, RDFS

class VirtualNode(object):
    
    def __init__(self):
        self.graphs = []
        self.rule_files = []
    
    def add_graph(self, graph_file):
        g = Graph()
        g.parse( graph_file , format="n3" )
        self.graphs.append( g )
    
    def add_rule(self, rule_file):
        self.rule_files.append( rule_file )

    @property
    def predicates(self):      
        predicates = set()
        for graph in self.graphs:
            for predicate in graph.predicates(None, None):
                # Too general properties to predict anything... :-S
                if not predicate.startswith( str(RDF) ) or predicate.startswith( str(RDFS) ):
                    predicates.add( str(predicate) )
        return predicates