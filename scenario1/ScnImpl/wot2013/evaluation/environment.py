'''
Created on May 31, 2013

@author: tulvur
'''

import json
import shutil
from tempfile import mkdtemp

class ExperimentalEnvironment(object):
    
    UNREL_FACT_FILENAME = "unrelated_graph_%d.n3"
    UNREL_FACT_TEMPLATE = "unrelated_graph.n3.tpl"
    MAIN_GRAPHS = ["facts.n3"]
    MAIN_RULE = ["light3_rule.n3"]
    QUERY_RULE = "light_goal.n3"
    
    def __init__(self):
        self.output_folder = mkdtemp( dir = "/tmp" )
        self.copy_normal_knowledge()
        self.create_unrelated_graphs(100)
        self.create_scenario()
        self.create_scenario( unrelated_facts = 100 )
    
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
    
    def create_unrelated_graphs(self, n):
        with open (ExperimentalEnvironment.UNREL_FACT_TEMPLATE, "r") as input_file:
            content = input_file.read()
            for i in range(n):
                with open ( self.output_folder + "/" +  ExperimentalEnvironment.UNREL_FACT_FILENAME % i, "w" ) as output_file:
                    output_file.write( content.replace(r"(?id)", str(i)) )
    
    def create_scenario(self,
                        unrelated_facts = 1,
                        unrelated_goals = 1,
                        not_feasible_goals = 1 ):
        config = {}
        config["query_goal"] = self._get_new_filename( ExperimentalEnvironment.QUERY_RULE )
        config["virtual_nodes"] = []
        one_node = {}
        one_node["facts"] = []
        one_node["rules"] = []
        
        for i in range(unrelated_facts):
            one_node["facts"].append ( self.output_folder + "/" + ExperimentalEnvironment.UNREL_FACT_FILENAME % i )
            one_node["rules"] = []
        config["virtual_nodes"].append( one_node )
        
        
        actuator_node = {}
        actuator_node["facts"] = [ self._get_new_filename(el) for el in ExperimentalEnvironment.MAIN_GRAPHS ]
        actuator_node["rules"] = [ self._get_new_filename(el) for el in ExperimentalEnvironment.MAIN_RULE ]
        
        config["virtual_nodes"].append( actuator_node )
        
        with open ( "%s/scenario_%d_%d_%d.config" % (self.output_folder, unrelated_facts, unrelated_goals, not_feasible_goals), "w" ) as output_file:
            output_file.write( json.dumps(config) )

if __name__ == '__main__':
    ExperimentalEnvironment()
    