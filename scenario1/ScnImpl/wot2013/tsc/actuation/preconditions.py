'''
Created on May 28, 2013

@author: tulvur
'''

from os import removedirs
from tempfile import mkdtemp


class LemmaPreconditionsChecker(object):
    
    def __init__(self, output_folder, reasoner, evicence_templates, space_cache):
        self.output_folder = mkdtemp( dir = output_folder )
        self.reasoner = reasoner
        self.evicence_templates = evicence_templates
        self.space_cache = space_cache
    
    def clear_data(self):
        removedirs( self.output_folder )
    
    def cache_data(self):
        """Discards paths which cannot be followed because we do not have input data"""        
        for template in self.evicence_templates:
                self.space_cache.add_query( template.get_template() )
        self.space_cache.launch_requests()
        
        self._cached_file = self.output_folder + "cached.n3"
        self.space_cache.cache.serialize( self._cached_file, format="n3")
    
    
    def _create_fake_query_rule(self, path):
        tpls_to_str = ""
        for t in self.evicence_templates:
            tpls_to_str += t.n3()
        
        fq = """
{
    %s
} => {
    %s
} .
        """ % (tpls_to_str, tpls_to_str)
        
        with open(path, 'w') as fil:
            fil.write(fq)
    
    def _obtain_proofs(self):
        plan_path = self.output_folder + "/plan.n3" # not to confuse with ../plan.n3 ;-)
        query_path = self.output_folder + "/query.n3"
        self._create_fake_query_rule( query_path )
        self.reasoner.query_proofs( [self._cached_file] , query_path, plan_path )
    
    def get_real_bindings(self):
        self._obtain_proofs()