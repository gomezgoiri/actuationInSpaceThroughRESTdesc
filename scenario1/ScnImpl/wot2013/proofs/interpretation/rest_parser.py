'''
Created on Apr 30, 2013

@author: tulvur
'''

from optparse import OptionParser
from rdflib import Graph, Namespace, URIRef

http_ns = Namespace("http://www.w3.org/2011/http#")
log_ns = Namespace("http://www.w3.org/2000/10/swap/log#")

class RESTCall(object):
    
    def __init__(self, method, request_uri, var_body):
        self.method = method
        self.request_uri = request_uri
        self.var_body = var_body

# To be used with "services.txt"
class RESTServicesParser(object):   
    
    def __init__(self, file_path):
        self.rdf_graph = Graph()
        self.rdf_graph.parse(file_path, format="n3")
        #rdf_str = self._delete_blank_nodes(file_path)
        #self.rdf_graph.parse(StringIO(rdf_str), format="n3")
        #print self.rdf_graph.serialize(format="n3")
        
        self.calls = {}
        for t in self.rdf_graph.triples((None, http_ns.request, None)):
            rc = self.process_lemma(t[2])
            self.calls[t[0]] = rc 
    
    def process_lemma(self, lemma_rest):
        ru = None
        for t2 in lemma_rest.triples((None, http_ns.requestURI, None)):
            ru = t2[2]
            break
        m = None
        for t2 in lemma_rest.triples((None, http_ns.methodName, None)):
            m = t2[2]
            break
        b = None
        for t2 in lemma_rest.triples((None, http_ns.body, None)):
            b = t2[2]
            break
        return RESTCall(m, ru, b)
    
    def process_bindings(self, lemma_uri):
        pass # TODO
        

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input", default="../../../files/services.txt",
                      help="File to process")
    (options, args) = parser.parse_args()
    
    rg = RESTServicesParser( options.input )
    #rg.print_graph()
    
    #rg._get_shortest_path( goal = (URIRef("file:///home/tulvur/Downloads/test/image_ex/myphoto.jpg"), dbpedia_namespace["thumbnail"], None))