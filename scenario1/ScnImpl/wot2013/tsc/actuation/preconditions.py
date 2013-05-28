'''
Created on May 28, 2013

@author: tulvur
'''

from os import removedirs
from tempfile import mkdtemp
from rdflib import Graph, Namespace
from wot2013.proofs.interpretation.variable import Variable


blah_ns = Namespace("http://blah.is/absurd#")

class LemmaPreconditionsChecker(object):
    
    def __init__(self, output_folder, reasoner, evidence_templates, space_cache):
        self.output_folder = mkdtemp( dir = output_folder )
        self.reasoner = reasoner
        self.evidence_templates = evidence_templates
        self.variables = self._extract_variables( evidence_templates )
        self.space_cache = space_cache
    
    def clear_data(self):
        removedirs( self.output_folder )
        
    def _extract_variables(self, tpls):
        variables = set()
        for tpl in tpls:
            variables = variables.union( tpl.get_variables() )
        return variables
        
    
    def cache_data(self):
        """Discards paths which cannot be followed because we do not have input data"""        
        for template in self.evidence_templates:
                self.space_cache.add_query( template.get_template() )
        self.space_cache.launch_requests()
        
        self._cached_file = self.output_folder + "/cached.n3"
        self.space_cache.cache.serialize( self._cached_file, format="n3")
    
    def _create_consequence(self):
        ret = ""
        for var in self.variables:
            ret += "<%s> <%s> %s . \n" % ( var.fake_urize(), blah_ns.bound_to, var )
        return ret
    
    def _create_fake_query_rule(self, path):
        tpls_to_str = ""
        for t in self.evidence_templates:
            tpls_to_str += t.n3()
        
        fq = """
@prefix blah: <%s>.
{
    %s
} => {
    %s
} .
        """ % ( blah_ns, tpls_to_str, self._create_consequence() )
        
        with open(path, 'w') as fil:
            fil.write(fq)
    
    def _obtain_proofs(self):
        self._result_path = self.output_folder + "/results.n3" # not to confuse with ../plan.n3 ;-)
        query_path = self.output_folder + "/query.n3"
        self._create_fake_query_rule( query_path )
        self.reasoner.query( [self._cached_file] , query_path, self._result_path )
    
    # error prone: what if multiple results unrelated with each other?
    def _get_bindings(self):
        ret = {}
        
        g = Graph()
        g.parse( self._result_path, format="n3" )
        for var, _, bound_to in g.triples( (None, blah_ns.bound_to, None) ):
            v = Variable( var )
            if v not in ret:
                ret[v] = []
            ret[v].append( bound_to )
        
        return ret
    
    def get_real_bindings(self):
        self._obtain_proofs()
        return self._get_bindings()