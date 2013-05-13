'''
Created on Apr 30, 2013

@author: tulvur
'''

from optparse import OptionParser
from rdflib import Graph, Namespace, URIRef

r_ns = Namespace("http://www.w3.org/2000/10/swap/reason#")
http_ns = Namespace("http://www.w3.org/2011/http#")
log_ns = Namespace("http://www.w3.org/2000/10/swap/log#")

class RESTCall(object):
    
    def __init__(self, method, request_uri, var_body):
        self.method = method
        self.request_uri = request_uri
        self.var_body = var_body
        self.bindings = []
    
    def add_binding(self, var, bound):
        self.bindings = (var, bound)
    
    def __repr__(self):
        return "(m: %s, ru: %s, body: %s, bindings: %s)" % (self.method, self.request_uri, self.var_body, self.bindings)

# To be used with "services.txt"
class RESTServicesParser(object):   
    
    def __init__(self, rest_file_path, bindings_path):        
        self.calls = {}
        self._process_rest_services( rest_file_path )
        self._process_bindings( bindings_path )
            
    def _process_rest_services(self, rest_file_path):
        rdf_graph = Graph()
        rdf_graph.parse(rest_file_path, format="n3")
        
        for t in rdf_graph.triples((None, http_ns.request, None)):
                rc = self._process_lemmas_rest(t[2])
                self.calls[t[0]] = rc
    
    def _process_lemmas_rest(self, lemma_rest):
        for t in lemma_rest.triples((None, log_ns.implies, None)):
            ru = None
            for t2 in t[2].triples((None, http_ns.requestURI, None)):
                ru = t2[2]
                break
            m = None
            for t2 in t[2].triples((None, http_ns.methodName, None)):
                m = t2[2]
                break
            b = None
            for t2 in t[2].triples((None, http_ns.body, None)):
                b = t2[2]
                break
            return RESTCall(m, ru, b)
    
    def _process_bindings(self, bindings_file_path):
        rdf_graph = Graph()
        rdf_graph.parse(bindings_file_path, format="n3")
        
        for lemma, rest_call in self.calls.iteritems():
            var, bound = None, None
            for t in rdf_graph.triples((lemma, r_ns.var, None)):
                var = t[2]
                bound = rdf_graph.triples((lemma, r_ns.bound, None)).next()[2]
                    
            if var is None or bound is None:
                print "Warning: no 'var' or 'bound' for the binding of lemma %s"%(lemma)
            else:
                rest_call.add_binding(var, bound)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--rest_input", dest="input", default="../../../files/services.txt",
                      help="File to process")
    parser.add_option("-b", "--bindings", dest="bindings", default="../../../files/bindings.txt",
                      help="File to process")
    (options, args) = parser.parse_args()
    
    rsp = RESTServicesParser( options.input, options.bindings )
    print rsp.calls