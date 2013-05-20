'''
Created on May 20, 2013

@author: tulvur
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
        
    def get_predicates(self):        
        predicates = set()
        for graph in self.graphs:
            for predicate in graph.predicates(None, None):
                # Too general properties to predict anything... :-S
                if not predicate.startswith( str(RDF) ) or predicate.startswith( str(RDFS) ):
                    predicates.add( str(predicate) )
        return predicates