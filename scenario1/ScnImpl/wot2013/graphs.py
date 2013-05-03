'''
Created on Apr 30, 2013

@author: tulvur
'''

import re
from rdflib import Graph, Namespace, URIRef
from StringIO import StringIO
import networkx as nx
import matplotlib.pyplot as plt

class ResultGraph(object):   
    
    def __init__(self, file_path):
        rdf_str = self._delete_blank_nodes(file_path)
        self.rdf_graph = Graph()
        #self.rdf_graph.parse(file_path, format="n3")
        self.rdf_graph.parse(StringIO(rdf_str), format="n3")
        #print self.rdf_graph.serialize(format="n3")
    
    def _delete_blank_nodes(self, file_path):
        with open (file_path, "r") as myfile:
            #data = myfile.read().replace('_:sk', 'http://anon/') # wrong: "<" and ">" are missing
            data= re.sub('_:sk(?P<num>\d+)', '<http://anon/\g<num>>', myfile.read())
            return data
        
    def _create_graph(self):
        graph = nx.Graph()
        for t in self.rdf_graph.triples((None, None, None)):
            t0 = str(t[0])
            t2 = str(t[2])
            graph.add_node( t0 )
            graph.add_node( t2 )
            graph.add_edge( t0, t2 )
        nx.draw(graph)  # networkx draw()
        plt.savefig("path.png")
        
        return graph
    
    def _get_targets(self, goal_template):
        # <myphoto.jpg> dbpedia-owl:thumbnail ?thumbnail.
        return list( self.rdf_graph.triples(goal_template) )
         
    def _get_shortest_path(self, goal):
        print self._get_targets(goal)
        g = self._create_graph()
        print(nx.shortest_path(g, source="http://anon/0", target="http://anon/3"))
        
    def _get_requests(self):
        t = self.g.triples((None, Agent.http_namespace["requestURI"], None ) )
        for trip in t:
            print trip
            
    def get_goal(self):
        # <myphoto.jpg> dbpedia-owl:thumbnail
        # ?outputvalue  dul:hasDataValue  :t19 .
        #t = self.g.triples((None, Agent.dul_namespace["hasDataValue"], None ) )
        return self.g.triples((None, Agent.dbpedia_namespace["thumbnail"], None ) )
            
    def get_path_to_goal(self):
        # <myphoto.jpg> dbpedia-owl:thumbnail
        # ?outputvalue  dul:hasDataValue  :t19 .
        #t = self.g.triples((None, Agent.dul_namespace["hasDataValue"], None ) )
        t = self.g.triples((None, Agent.dbpedia_namespace["thumbnail"], None ) )
        for trip in t:
            print trip
        

if __name__ == '__main__':    
    http_namespace = Namespace("http://www.w3.org/2011/http#")
    dul_namespace = Namespace("http://www.loa.istc.cnr.it/ontologies/DUL.owl#")
    dbpedia_namespace = Namespace("http://dbpedia.org/ontology/")
    
    rg = ResultGraph("../files/query_output_order2.n3")
    #rg._create_graph()
    
    rg._get_shortest_path( goal = (URIRef("file:///home/tulvur/Downloads/test/image_ex/myphoto.jpg"), dbpedia_namespace["thumbnail"], None))