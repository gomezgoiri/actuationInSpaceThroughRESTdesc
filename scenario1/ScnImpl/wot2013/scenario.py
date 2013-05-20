'''
Created on May 20, 2013

@author: tulvur
'''

import json
from optparse import OptionParser
from tsc.virtual import VirtualNode
from tsc.actuation import ActuationStarterNode


class ScenarioSimulator(object):
    
    def __init__(self, configuration_file, options, euler):
        with open (configuration_file, "r") as input_file:
            config = json.loads( input_file.read() )
            self.configure_scenario( config )
    
    def configure_scenario(self, config):
        self.nodes = []
        for node in config["virtual_nodes"]:
            vn = VirtualNode()
            for fact_file in node["facts"]:
                vn.add_graph( fact_file )
            
            for rule_file in node["rules"]:
                vn.add_rule( rule_file )
            
            self.nodes.append( vn )
                
        self.actuation_starter = ActuationStarterNode( config["query_goal"] )


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input",
                      help="File to configure the scenario")
    parser.add_option("-o", "--output", dest="output", default="/tmp",
                      help="Output folder where the processed results will be written.")
    parser.add_option("-e", "--euler", dest = "euler", default='../../../../',
                      help = "Path to Euler.jar")
    (options, args) = parser.parse_args()

    uie = ScenarioSimulator(options.input, options.output, options.euler)
    uie.extract()