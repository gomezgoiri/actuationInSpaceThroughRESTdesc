'''
Created on May 20, 2013

@author: tulvur
'''

from rdflib import Graph, RDF, RDFS
from wot2013.tsc.space_manager import SpaceManager
from wot2013.tsc.virtual.nodes import VirtualNode


class VirtualSpaceManager(SpaceManager):
    
    def __init__(self):
        self.nodes = {}
        self.clues = None
        self.calls_to_middleware = 0
    
    def create_node(self, facts, rules):
        vn = VirtualNode()
        for fact_file in facts:
            vn.add_graph( fact_file )
            
        for rule_file in rules:
            vn.add_rule( rule_file )
        
        self.nodes[ "node_%d" % len(self.nodes) ] = vn
    
    
    def create_clues(self):
        ret = {}
        # Simplified: not following IJWGS' format
        ret["predicates"] = {}
        ret["rule_files"] = {}
        
        for name, node in self.nodes.iteritems():
            ret["predicates"][name] = node.predicates
            ret["rule_files"][name] = node.rule_files
            
        return ret
        
    
    def get_clues(self):
        if self.clues is None:
            # Assuming they do not change
            self.clues = self.create_clues()
        return self.clues
    
    
    def query_tsc(self, template):
        self.calls_to_middleware += 1
        ret = Graph()
        looking_for = str(template[1])
        for name, predicates in self.get_clues()["predicates"].iteritems():
            query_this_node = False
            
            if looking_for.startswith( str(RDF) ) or looking_for.startswith( str(RDFS) ):
                # any node can have this kind of predicates
                #(actually, they were filtered for the clue generation)
                query_this_node = True
            else:
                for pred in predicates:
                    if pred == looking_for:
                        query_this_node = True
                        break
            
            if query_this_node:
                for graph in self.nodes[name].graphs:
                    for triple in graph.triples(template):
                        ret.add( triple )
        return ret