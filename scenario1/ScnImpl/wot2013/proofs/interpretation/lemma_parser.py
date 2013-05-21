'''
Created on Apr 30, 2013

@author: tulvur
'''

from optparse import OptionParser
from rdflib import Namespace
from wot2013.proofs.interpretation.bindings_parser import BindingsParser
from wot2013.proofs.interpretation.rest_parser import RESTServicesParser

r_ns = Namespace("http://www.w3.org/2000/10/swap/reason#")
http_ns = Namespace("http://www.w3.org/2011/http#")
log_ns = Namespace("http://www.w3.org/2000/10/swap/log#")


class Lemma(object):
    
    def __init__(self):
        self.rest = None
        self._bindings = set()
        self.evicence_templates = []
    
    def get_binding(self, var_name):
        for binding in self.bindings:
            if binding.variable == var_name:
                return binding.bound
        else: return None
        
    def set_binding(self, var_name, new_value):
        for binding in self.bindings:
            if binding.variable == var_name:
                binding.bound = new_value
                break
    
    @property
    def bindings(self):
        return self._bindings
    
    @bindings.setter
    def bindings(self, bindings): # to ensure that bindings is a list and therefore can be compared with other list
        if isinstance(bindings, (list, tuple)):
            self._bindings = set(bindings)
        elif isinstance(bindings, set):
            self._bindings = bindings
        else:
            raise Exception("It should be a list, tuple or set!")
    
    def equivalent_rest_calls(self, other_lemma):
        ret = self.rest == other_lemma.rest and self.bindings == other_lemma.bindings
        if ret:
            # TODO what if it is not a variable?
            if self.rest is not None: # therefore other_lemma.rest cannot be None either
                ret = self.get_binding( self.rest.var_body ) == other_lemma.get_binding( other_lemma.rest.var_body )
            
            # same bindings
            if ret:
                ret = set( [bind.bound for bind in self.bindings] ) == set( [bind.bound for bind in other_lemma.bindings] )
            
        return ret
    
    def __repr__(self):
        return "l(rest: %s, bindings: %s, evidences: %s)" % (self.rest, self.bindings, self.evicence_templates)
    

class LemmaParser(object):
    """
    This class parses what a lemma contains or may contain:
      * evidence template patterns
      * bindings
      * rest services
    """
    
    def __init__(self, rest_file_path, bindings_path):
        self.lemmas = {}
        
        bp = BindingsParser( bindings_path ) 
        for lemma, bindings in bp.bindings_by_lemma.iteritems():
            self._init_lemma_if_needed(lemma)
            self.lemmas[lemma].bindings = bindings
        
        rp = RESTServicesParser( rest_file_path )
        for lemma, rest in rp.calls.iteritems():
            self._init_lemma_if_needed(lemma)
            self.lemmas[lemma].rest = rest
    
    def _init_lemma_if_needed(self, lemma):
        if lemma not in self.lemmas:
            self.lemmas[lemma] = Lemma()


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--rest_input", dest="input", default="../../../files/services.txt",
                      help="File to process")
    parser.add_option("-b", "--bindings", dest="bindings", default="../../../files/bindings.txt",
                      help="File to process")
    (options, args) = parser.parse_args()
    
    lp = LemmaParser( options.input, options.bindings )
    print lp.lemmas