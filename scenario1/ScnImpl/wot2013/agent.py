'''
Created on Apr 30, 2013

@author: tulvur
'''

from StringIO import StringIO
from rdflib import Graph, Namespace

class Agent(object):
    
    http_namespace = Namespace("http://www.w3.org/2011/http#")
    dul_namespace = Namespace("http://www.loa.istc.cnr.it/ontologies/DUL.owl#")
    dbpedia_namespace = Namespace("http://dbpedia.org/ontology/")
    
    def __init__(self, file_path):
        n3_ordered = self._order_triples_alphabetically(file_path)
        self.g = Graph()
        #self.g.parse(file_path, format="n3")
        self.g.parse(StringIO(n3_ordered), format="n3")
        print self.g.serialize(format="n3")
    
    def _order_triples_alphabetically(self, file_path):        
        with open (file_path, "r") as myfile:
            ret = ""
            to_order = []
            for line in myfile.read().splitlines(): # .sort()
                if line.startswith("@prefix"):
                    ret = "%s\n%s" % (ret, line)
                elif line.startswith("#"):
                    pass # ignore
                else:
                    to_order.append(line)
            
            for line in sorted(to_order):
                ret = "%s\n%s" % (ret, line)
            return ret
    
    def get_requests_in_order(self):
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
    Agent("../files/query_output_order2.n3")