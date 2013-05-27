'''
Created on May 20, 2013

@author: tulvur
'''
import re
from os import remove
from tempfile import mkdtemp
from os.path import basename, splitext
from rdflib import Graph, Namespace, Literal, RDF, RDFS
from rdflib.namespace import XSD

from wot2013.proofs.interpretation.variable import fake_ns
from wot2013.proofs.extract_info import UsefulInformationExtractor
from wot2013.proofs.interpretation.graphs import LemmaPrecedencesGraph
from wot2013.proofs.interpretation.lemma_parser import LemmaParser



log_ns = Namespace("http://www.w3.org/2000/10/swap/log#")
op_ns = Namespace("http://www.w3.org/2000/10/swap/math#")


class ActuationStarterNode(object):
    
    def __init__(self, query_goal_path, output_folder, reasoner):
        self.query_goal_path = query_goal_path
        self.output_folder = mkdtemp(dir=output_folder)
        self.reasoner = reasoner
    
    def add_clues(self, clues):
        self.rule_paths = self._extract_rules(clues["rule_files"])
        self.predicates = self._extract_predicates(clues["predicates"])
        
    def _extract_rules(self, rules_by_node):
        rules = []
        for _, ruls in rules_by_node.iteritems():
            rules += ruls
        return rules

    def _extract_predicates(self, predicates_by_node):
        predicates = set()
        for _, predicats in predicates_by_node.iteritems():
            predicates = predicates.union(predicats)
        return predicates
    
    def _get_temporary_file_path(self, original_file_path):
        # now you can call it directly with basename
        filename_with_extension = basename(original_file_path)
        filename_without_extension = splitext(filename_with_extension)[0]
        return self.output_folder + "/" + filename_without_extension + "_activator.n3"
    
    def _create_fake_rules(self):
        temporary_files = []
        for rule_path in self.rule_paths:
            g = Graph()
            g.parse( rule_path, format="n3" )
            for premise in g.subjects(log_ns.implies, None):
                # premise should be another "graph"
                all_in_clues = True
                for predicate in premise.predicates(None, None):
                    str_pred = str(predicate)
                    if str_pred.startswith( str(RDF) ) or str_pred.startswith( str(RDFS) ) or str_pred.startswith( str(op_ns) ):
                        pass # all_in_clues is still True
                    else:
                        if str_pred not in self.predicates:
                            all_in_clues = False
                            break # I got it, so do not check more predicates
            
                if all_in_clues:
                    temporary_file_path = self._get_temporary_file_path( rule_path )
                    self._create_fake_rule( premise, temporary_file_path )
                    temporary_files.append( temporary_file_path )
        return temporary_files
    
    def _create_fake_rule(self, premise, temporary_file_path):
        new_g = Graph()
        new_g.add(( Literal("true", datatype=XSD.boolean), log_ns.implies, premise) )
        new_g.serialize( temporary_file_path, format="n3" )
        self._substitute_vars_for_fake_uris( temporary_file_path )
        
    def _substitute_vars_for_fake_uris(self, file_path):
        fake_prefix = r"@prefix fake: <%s>." % fake_ns
        with open(file_path, 'r+') as infile:
            data = re.sub('\?(?P<var_name>\w+)', 'fake:\g<var_name>', infile.read())
            with open(file_path, 'r+') as outfile:
                outfile.write( fake_prefix + "\n" + data)
        
    def create_plan(self):
        input_files = self.rule_paths + self._create_fake_rules()
        output = self.reasoner.query_proofs( input_files, self.query_goal_path )
        with open (self.output_folder + "/plan.n3", "w") as output_file:
            output_file.write( output )
    
    def process_plan(self):
        uie = UsefulInformationExtractor(self.output_folder + "/plan.n3", self.output_folder, self.reasoner)
        uie.extract_all()
        
        self.lemma_graph = LemmaPrecedencesGraph(self.output_folder + "/" + UsefulInformationExtractor.get_output_filename("precedences"))
        
        lp = LemmaParser( self.output_folder + "/" + UsefulInformationExtractor.get_output_filename("services"),
                          self.output_folder + "/" + UsefulInformationExtractor.get_output_filename("bindings"),
                          self.output_folder + "/" + UsefulInformationExtractor.get_output_filename("evidences") )
        self.lemma_graph.add_lemmas_info( lp.lemmas )
        self.lemma_graph.create_nx_graph()
        #self.lemma_graph.to_image( output_file = options.output + "/lemma_precedences.png" )
        #self.lemma_graph.to_gml( output_file = self.output_folder + "/lemma_precedences.gml" )
    
    def discard_paths(self, space_cache):
        """Discards paths which cannot be followed because we do not have input data"""        
        i = 0
        for path in self.lemma_graph.get_all_paths():
            print "PATH %d" % i
            i += 1
            
            for node in path:
                rest = self.lemma_graph.get_rest_call(node)
                if rest is None:
                    print "No service for %s" % node
                else:
                    for template in rest.evicence_templates:
                        space_cache.add_query( template.get_template() )
                    space_cache.launch_requests()
                    #print rest
                    print "------"
                    print space_cache.cache.serialize(self.output_folder + "/cached.n3", format="n3")
                    
                    self._create_fake_query_rule( rest.evicence_templates )
    
    def _create_fake_query_rule(self, templates):
        tpls_to_str = ""
        for t in templates:
            tpls_to_str += t.n3()
        
        fq = """
{
    %s
} => {
    %s
}            
        """ % (tpls_to_str, tpls_to_str)
        
        with open(self.output_folder + "/query.n3", 'w') as fil:
            fil.write(fq)
            
    # TODO
    #      1. con el query creado y el cache.n3, sacar las pruebas
    #      2. extraer de las pruebas los bindings
    #      3. almacenarlos en algun lado por si se usan despues.
    #      4. comprobar siguiente lemma y ver que caminos funcionan
    #  Con eso:
    #      1. mirar si se podria vender lo de los caminos de forma facil
    #      2. Si no, venderlo como que se ofrece juntar ambos mundos (un poco lo de siempre... :-S)