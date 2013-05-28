'''
Created on May 27, 2013

@author: tulvur
'''

import re
from os import remove
from os.path import basename, splitext
from rdflib import Graph, Namespace, Literal, RDF, RDFS
from rdflib.namespace import XSD
from wot2013.proofs.interpretation.variable import fake_ns

log_ns = Namespace("http://www.w3.org/2000/10/swap/log#")
op_ns = Namespace("http://www.w3.org/2000/10/swap/math#")


class ActuationPlanCreator(object):
    
    def __init__(self, query_goal_path, output_folder, reasoner, debug = False):
        self.query_goal_path = query_goal_path
        self.output_folder = output_folder
        self.reasoner = reasoner
        self.debug = debug
    
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
    
    def _substitute_vars_for_fake_uris(self, file_path):
        fake_prefix = r"@prefix fake: <%s>." % fake_ns
        with open(file_path, 'r+') as infile:
            data = re.sub('\?(?P<var_name>\w+)', 'fake:\g<var_name>', infile.read())
            with open(file_path, 'r+') as outfile:
                outfile.write( fake_prefix + "\n" + data)
    
    def _create_fake_rule(self, premise, temporary_file_path):
        new_g = Graph()
        new_g.add(( Literal("true", datatype=XSD.boolean), log_ns.implies, premise) )
        new_g.serialize( temporary_file_path, format="n3" )
        self._substitute_vars_for_fake_uris( temporary_file_path )
    
    def _create_fake_rules(self, rule_paths, predicates):
        temporary_files = []
        
        for rule_path in rule_paths:
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
                        if str_pred not in predicates:
                            all_in_clues = False
                            break # I got it, so do not check more predicates
            
                if all_in_clues:
                    temporary_file_path = self._get_temporary_file_path( rule_path )
                    self._create_fake_rule( premise, temporary_file_path )
                    temporary_files.append( temporary_file_path )
        return temporary_files
    
    def _remove_temporary_files(self, files):
        for fi in files:
            remove( fi )
        
    def create_plan(self, clues):
        predicates = self._extract_predicates(clues["predicates"])
        rule_paths = self._extract_rules(clues["rule_files"])
        
        # Generate plan using fake rules and remove them after getting it
        fake_rules = self._create_fake_rules( rule_paths, predicates )
        output_file_path = self.reasoner.query_proofs( rule_paths + fake_rules,
                                                         self.query_goal_path,
                                                         self.output_folder + "/plan.n3" ) # Write the plan into a file
        if not self.debug: self._remove_temporary_files( fake_rules )
        return output_file_path