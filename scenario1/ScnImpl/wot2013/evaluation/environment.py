'''
Created on May 31, 2013

@author: tulvur
'''

import json
import shutil
from tempfile import mkdtemp

class ExperimentalEnvironment(object):
    
    UNREL_GRAPH = "unrelated_graph"
    UNREL_RULE_GRAPH = "thermometer"
    UNREL_RULE_RULE = "temperature_rule"
    NOT_FEASIBLE_RULE = "light2_rule"
    MAIN_GRAPHS = ["facts.n3"]
    MAIN_RULE = ["light3_rule.n3"]
    QUERY_RULE = "light_goal.n3"
    
    def __init__(self):
        self.output_folder = mkdtemp( dir = "/tmp" )
        self.copy_normal_knowledge()
        self.create_unrelated_graphs(100)
        self.create_unrelated_rules(100)
        self.create_not_feasible_rules(100)
        
        self.create_scenario()
        self.create_scenario( unrelated_facts = 100 )
        self.create_scenario( unrelated_rules = 100 )
        self.create_scenario( not_feasible_rules = 100 )
    
    def _get_new_filename(self, filename):
        return self.output_folder + "/" + filename
    
    def _copy_file(self, filename):
        shutil.copyfile( filename, self._get_new_filename( filename ) )
    
    def copy_normal_knowledge(self):
        self._copy_file( ExperimentalEnvironment.QUERY_RULE )
        for normal_graphs in ExperimentalEnvironment.MAIN_GRAPHS:
            self._copy_file( normal_graphs )
        for normal_rule in ExperimentalEnvironment.MAIN_RULE:
            self._copy_file( normal_rule )
    
    def get_template_filepath(self, filename):
        return "%s.n3.tpl" % (filename)
    
    def get_output_filepath(self, filename, num):
        return "%s/%s_%d.n3" % (self.output_folder, filename, num)
    
    def create_files_from_template(self, template_filename, n):
        with open ( self.get_template_filepath(template_filename), "r") as input_file:
            content = input_file.read()
            for i in range(n):
                with open ( self.get_output_filepath(template_filename, i), "w" ) as output_file:
                    output_file.write( content.replace(r"(?id)", str(i)) )
                    
    def create_unrelated_graphs(self, n):
        self.create_files_from_template( ExperimentalEnvironment.UNREL_RULE_GRAPH, n )
    
    def create_unrelated_rules(self, n):
        self.create_files_from_template( ExperimentalEnvironment.UNREL_RULE_RULE, n )
        self.create_files_from_template( ExperimentalEnvironment.UNREL_RULE_GRAPH, n )
    
    def create_not_feasible_rules(self, n):
        self.create_files_from_template( ExperimentalEnvironment.NOT_FEASIBLE_RULE, n )
    
    def create_scenario(self,
                        unrelated_facts = 1,
                        unrelated_rules = 1,
                        not_feasible_rules = 1 ):
        config = {}
        config["query_goal"] = self._get_new_filename( ExperimentalEnvironment.QUERY_RULE )
        config["virtual_nodes"] = []
        one_node = {} # in one node all the content, nothing special since that part is not being evaluated
        one_node["facts"] = []
        one_node["rules"] = []
        
        for i in range(unrelated_facts):
            one_node["facts"].append ( self.get_output_filepath(ExperimentalEnvironment.UNREL_GRAPH, i) )
            one_node["rules"] = []
            
        for i in range(unrelated_rules):
            one_node["facts"].append ( self.get_output_filepath(ExperimentalEnvironment.UNREL_RULE_GRAPH, i) )
            one_node["rules"].append ( self.get_output_filepath(ExperimentalEnvironment.UNREL_RULE_RULE, i) )
            
        for i in range(not_feasible_rules):
            one_node["facts"] = []
            one_node["rules"].append ( self.get_output_filepath(ExperimentalEnvironment.NOT_FEASIBLE_RULE, i) )
            
        config["virtual_nodes"].append( one_node )
        
        
        actuator_node = {}
        actuator_node["facts"] = [ self._get_new_filename(el) for el in ExperimentalEnvironment.MAIN_GRAPHS ]
        actuator_node["rules"] = [ self._get_new_filename(el) for el in ExperimentalEnvironment.MAIN_RULE ]
        
        config["virtual_nodes"].append( actuator_node )
        
        with open ( "%s/scenario_%d_%d_%d.config" % (self.output_folder, unrelated_facts, unrelated_rules, not_feasible_rules), "w" ) as output_file:
            output_file.write( json.dumps(config) )

if __name__ == '__main__':
    ExperimentalEnvironment()
    