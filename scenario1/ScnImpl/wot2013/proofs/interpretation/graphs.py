'''
Created on Apr 30, 2013

@author: tulvur
'''

import re
from optparse import OptionParser
from rdflib import Graph, Namespace
import networkx as nx
import matplotlib.pyplot as plt

r_ns = Namespace("http://www.w3.org/2000/10/swap/reason#")

# To be used with "lemma_precedences.txt"
class LemmaPrecedencesGraph(object):   
    
    def __init__(self, file_path):
        self.rdf_graph = Graph()
        self.rdf_graph.parse(file_path, format="n3")
        #rdf_str = self._delete_blank_nodes(file_path)
        #self.rdf_graph.parse(StringIO(rdf_str), format="n3")
        #print self.rdf_graph.serialize(format="n3")
    
    def _delete_blank_nodes(self, file_path):
        with open (file_path, "r") as myfile:
            #data = myfile.read().replace('_:sk', 'http://anon/') # wrong: "<" and ">" are missing
            data= re.sub('_:sk(?P<num>\d+)', '<http://anon/\g<num>>', myfile.read())
            return data
    
    def print_graph(self, output_file):
        nx.draw( self.create_graph() )  # networkx draw()
        plt.savefig(output_file)
    
    def create_graph(self):
        graph = nx.Graph()
        for t in self.rdf_graph.triples((None, r_ns.because, None)):
            t0 = str(t[0])
            t2 = str(t[2])
            graph.add_node( t0 )
            graph.add_node( t2 )
            graph.add_edge( t0, t2 )        
        return graph
             
    def _get_shortest_path(self, goal):
        print self._get_targets(goal)
        g = self._create_graph()
        print(nx.shortest_path(g, source="http://anon/0", target="http://anon/3"))
        

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input", default="../../../files/precedences.txt",
                      help="File to process")
    parser.add_option("-o", "--output", dest="output", default="/tmp",
                      help="Output folder where the image will be written.")
    (options, args) = parser.parse_args()
    
    rg = LemmaPrecedencesGraph( options.input )
    rg.print_graph( output_file = options.output + "/lemma_precedences.png" )
    
    #rg._get_shortest_path( goal = (URIRef("file:///home/tulvur/Downloads/test/image_ex/myphoto.jpg"), dbpedia_namespace["thumbnail"], None))