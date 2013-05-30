'''
Created on May 31, 2013

@author: tulvur
'''

import json
from tempfile import mkdtemp

class ExperimentalEnvironment(object):
    
    UNREL_FACT_FILENAME = "unrelated_fact_%d.n3"
    UNREL_FACT_TEMPLATE = "unrelated_fact.n3.tpl" 
    
    def __init__(self):
        self.output_folder = mkdtemp( dir = "/tmp" )
        self.create_unrelated_facts(100)
        self.create_scenario()
        self.create_scenario( unrelated_facts = 100 )
    
    def create_unrelated_facts(self, n):
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
        config["query_goal"] = "light_goal.n3"
        config["virtual_nodes"] = []
        one_node = {}
        one_node["facts"] = []
        one_node["rules"] = []
        
        for i in range(unrelated_facts):
            one_node["facts"].append ( self.output_folder + "/" + ExperimentalEnvironment.UNREL_FACT_FILENAME % i )
            one_node["rules"] = []
        config["virtual_nodes"].append( one_node )
        
        with open ( "%s/scenario_%d_%d_%d.config" % (self.output_folder, unrelated_facts, unrelated_goals, not_feasible_goals), "w" ) as output_file:
            output_file.write( json.dumps(config) )

if __name__ == '__main__':
    ExperimentalEnvironment()
    