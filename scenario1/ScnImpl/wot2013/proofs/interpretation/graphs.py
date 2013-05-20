'''
Created on Apr 30, 2013

@author: tulvur
'''

import re
from optparse import OptionParser
from rdflib import Graph, Namespace
import networkx as nx
import matplotlib.pyplot as plt
from wot2013.proofs.extract_info import UsefulInformationExtractor
from wot2013.proofs.interpretation.rest_parser import RESTServicesParser

r_ns = Namespace("http://www.w3.org/2000/10/swap/reason#")

# To be used with "lemma_precedences.txt"
class LemmaPrecedencesGraph(object):
    
    def __init__(self, file_path):
        self.rdf_graph = Graph()
        self.rdf_graph.parse(file_path, format="n3")
        self.filter = None
    
    def add_call_repetition_filter(self, rest_calls_dict):
        self.filter = rest_calls_dict
    
    def _is_rest_call(self, new_child_node):
        return new_child_node in self.filter
    
    def _is_repeated(self, added_children, new_child_node):        
        node_rest_info = self.filter[ new_child_node ]
        for added_child in added_children: # not sure if "in" should work without redefining the hash_code
            if added_child in self.filter:
                added_rest_info = self.filter[ added_child ]
                if added_rest_info == node_rest_info:
                    return True
        return False
    
    def _should_be_filtered(self, added_children, child_node):
        # avoid adding lemmas which are not REST calls
        # avoid adding 2 children lemmas who have the same REST calls
        if self.filter is not None:
            if self._is_rest_call(child_node):
                return self._is_repeated( added_children, child_node )
        return False
    
    def create_nx_graph(self):
        #graph = nx.Graph()
        graph = nx.DiGraph()
        
        unique_parent_nodes = set( list( self.rdf_graph.subjects( r_ns.because, None ) ) )
        for parent_node in unique_parent_nodes:
            added_children = []
            for child_node in self.rdf_graph.objects( parent_node, r_ns.because ):
                
                if not self._should_be_filtered( added_children, child_node ):
                    added_children.append( child_node )
                    
                    graph.add_node( parent_node )
                    graph.add_node( child_node )
                    # lemma1 because lemma2, means that lemma2 -> lemma1
                    graph.add_edge( child_node, parent_node )
        
        # create starting point and ending point and link it with leaves
        graph.add_node( "source" )
        graph.add_node( "target" )
        
        for leave in (n for n,d in graph.out_degree_iter() if d==0):
            if leave is not "source" and leave is not "target":
                graph.add_edge( leave, "target" )
            
        for root in (n for n,d in graph.in_degree_iter() if d==0):
            if root is not "source" and leave is not "target":  
                graph.add_edge( "source", root )
        
        self.graph = graph
    
    def to_gml(self, output_file):
        # from http://networkx.github.io/documentation/latest/examples/drawing/edge_colormap.html
        nx.write_gml(self.graph, output_file)
        #nx.write_edgelist(self.graph, output_file)
    
    def to_image(self, output_file):
        # from http://networkx.github.io/documentation/latest/examples/drawing/edge_colormap.html
        #pos = nx.spectral_layout(self.graph)
        pos = nx.circular_layout(self.graph)
        #pos = nx.spring_layout(self.graph)
        colors = '#6aaed6' #range(len(self.graph.edges()))
        nx.draw( self.graph,
                 pos, node_size=0, alpha=0.4, edge_color=colors, node_color='#A0CBE2', edge_cmap=plt.cm.Blues, width=2) #, node_color='#A0CBE2' , with_labels=False)
        plt.savefig(output_file)

    def get_shortest_path(self):
        return nx.shortest_path(self.graph, source="source", target="target")
    
    def get_all_paths(self):
        return nx.all_simple_paths(self.graph, source="source", target="target")
        

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input", default="../../../files/precedences.txt",
                      help="File to process")
    parser.add_option("-f", "--filter", dest="filter_path", default=None, #"/tmp",
                      help="""Delete repeated REST calls.
                              Avoid REST call repetitions using the information from the provided folder.
                              Note that the folder should contain a 'bindings.txt' and 'services.txt' files.
                              """
                           )
    parser.add_option("-o", "--output", dest="output", default="/tmp",
                      help="Output folder where the image will be written.")
    (options, args) = parser.parse_args()
    
    
    rg = LemmaPrecedencesGraph( options.input )
    
    if options.filter_path is not None:
        rsp = RESTServicesParser( options.filter_path + "/" + UsefulInformationExtractor.get_output_filename("services"),
                              options.filter_path + "/" + UsefulInformationExtractor.get_output_filename("bindings") )
        rg.add_call_repetition_filter( rsp.calls )
    
    rg.create_nx_graph()
    rg.to_image( output_file = options.output + "/lemma_precedences.png" )
    rg.to_gml( output_file = options.output + "/lemma_precedences.gml" )
    
    #rg._get_shortest_path( goal = (URIRef("file:///home/tulvur/Downloads/test/image_ex/myphoto.jpg"), dbpedia_namespace["thumbnail"], None))