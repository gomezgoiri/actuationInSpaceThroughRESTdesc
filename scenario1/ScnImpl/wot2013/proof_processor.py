'''
Created on Apr 30, 2013

@author: tulvur
'''

import re
from rdflib import Graph, Namespace, URIRef, RDF
from StringIO import StringIO
import networkx as nx
import matplotlib.pyplot as plt


r_namespace = Namespace("http://www.w3.org/2000/10/swap/reason#")


class ResultGraph(object):   
    
    def __init__(self, file_path):
        rdf_str = self._give_URIs_to_lemmas(file_path)
        self.rdf_graph = Graph()
        #self.rdf_graph.parse(file_path, format="n3")
        self.rdf_graph.parse(StringIO(rdf_str), format="n3")
        #print self.rdf_graph.serialize(format="n3")
    
    def _give_URIs_to_lemmas(self, file_path):
        with open (file_path, "r") as myfile:
            #data = myfile.read().replace('_:sk', 'http://anon/') # wrong: "<" and ">" are missing
            data= re.sub('_:lemma(?P<num>\d+)', '<http://lemma/\g<num>>', myfile.read())
            return data
    
    def _substitute_lemma_by_number(self, lemma_uri):
        return str(lemma_uri)[len("http://lemma/"):]
    
    def _extract_elements(self, bnode_list):
        if bnode_list == RDF.nil: # caso base
            return []
        else: # caso recursivo
            l = self._extract_elements( list(self.rdf_graph.triples((bnode_list, RDF.rest, None)))[0] ) # .first() )
            l.append( list(self.rdf_graph.triples((bnode_list, RDF.first, None)))[0] ) # o con [0]
            print l
            return l
        
    def _create_graph(self):
        graph = nx.Graph()
        
        # ?s a r:Inference
        for t in self.rdf_graph.triples((None, RDF.type, r_namespace.Inference)):
            lemma_name = self._substitute_lemma_by_number(t[0])
            graph.add_node( lemma_name )
            for t2 in self.rdf_graph.triples((t[0], r_namespace.evidence, None)):
                elements = self._extract_elements(t2[2])
                for el in elements:
                    evidence_name = self._substitute_lemma_by_number(el)
                    graph.add_node( evidence_name )
                    graph.add_edge( lemma_name, evidence_name )
                
            #graph.add_node( t2 )
            #graph.add_edge( t0, t2 )        
        
        nx.draw(graph)  # networkx draw()
        plt.savefig("path.png")
        
        return graph
        

if __name__ == '__main__':
    #rg = ResultGraph("../files/full_result.n3")
    rg = ResultGraph("/home/tulvur/Downloads/test/image_ex/my_proof.n3")
    #rg._create_graph()
    
    rg._create_graph()