'''
Created on Apr 30, 2013

@author: tulvur
'''

from optparse import OptionParser
from rdflib import Graph, Namespace

r_ns = Namespace("http://www.w3.org/2000/10/swap/reason#")
http_ns = Namespace("http://www.w3.org/2011/http#")
log_ns = Namespace("http://www.w3.org/2000/10/swap/log#")

class RESTCall(object):
    
    def __init__(self, method, request_uri, var_body):
        self.method = method
        self.request_uri = request_uri
        self.var_body = self.get_var_name(var_body) # its name can be different and still be the same variable
    
    def get_var_name(self, binding_name):
        """if 'binding_name' is "http://localhost/var#x0" or ?x0, simply take x0"""
        prefs = ("http://localhost/var#", "?")
        for pref in prefs:
            if binding_name.startswith(pref):
                return binding_name[len(pref):]
        return binding_name
    
    def __repr__(self):
        return "r(m: %s, ru: %s, body: %s)" % (self.method, self.request_uri, self.var_body)
    
    def __eq__(self, other):
        return (self.method == other.method) & (self.request_uri == other.request_uri)


# To be used with "services.txt"
class RESTServicesParser(object):   
    
    def __init__(self, rest_file_path):        
        self.calls = {}
        self._process_rest_services( rest_file_path )
            
    def _process_rest_services(self, rest_file_path):
        rdf_graph = Graph()
        rdf_graph.parse(rest_file_path, format="n3")
        
        for t in rdf_graph.triples((None, http_ns.request, None)):
            rc = self._process_lemmas_rest(t[2])
            self.calls[ str(t[0]) ] = rc
    
    def _process_lemmas_rest(self, lemma_rest):
        for conclusion in lemma_rest.objects(None, log_ns.implies):
            request_subject = None
            ru = None
            for t in conclusion.triples((None, http_ns.requestURI, None)):
                request_subject = t[0]
                ru = t[2]
                break
            m = None
            for method_name in conclusion.objects(request_subject, http_ns.methodName):
                m = method_name
                break
            b = None
            for body in conclusion.objects(request_subject, http_ns.body):
                b = body
                break
            return RESTCall(m, ru, b)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--rest_input", dest="input", default="../../../files/services.txt",
                      help="File to process")
    (options, args) = parser.parse_args()
    
    rsp = RESTServicesParser( options.input )
    print rsp.calls