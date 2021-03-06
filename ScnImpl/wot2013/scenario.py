'''
 Copyright (C) 2013 onwards University of Deusto
  
 All rights reserved.
 
 This software is licensed as described in the file COPYING, which
 you should have received as part of this distribution.
 
 This software consists of contributions made by many individuals, 
 listed below:
 
 @author: Aitor Gómez Goiri <aitor.gomez@deusto.es>
'''

import json
from optparse import OptionParser
from wot2013.tsc.virtual.space_manager import VirtualSpaceManager
from wot2013.tsc.actuation.actuation import ActuationStarterNode


class ScenarioSimulator(object):
    
    def __init__(self, configuration_file, output_folder, reasoner):
        self.output_folder = output_folder
        self.reasoner = reasoner
        
        with open (configuration_file, "r") as input_file:
            config = json.loads( input_file.read() )
            self.configure_scenario( config )
    
    def configure_scenario(self, config):
        self.vsm = VirtualSpaceManager()
        for node in config["virtual_nodes"]:
            self.vsm.create_node( node["facts"], node["rules"] )
                
        self.actuation_starter = ActuationStarterNode( config["query_goal"],
                                                       self.output_folder,
                                                       self.reasoner )
        self.actuation_starter.add_space_manager( self.vsm )
    
    def actuate(self):
        self.actuation_starter.create_plan()
        self.actuation_starter.process_plan()
        self.actuation_starter.check_paths_viability()

    def get_calls_to_tsc(self):
        return self.vsm.calls_to_middleware


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input",
                      help="File to configure the scenario")
    parser.add_option("-o", "--output", dest="output", default="/tmp",
                      help="Output folder where the processed results will be written.")
    parser.add_option("-e", "--euler", dest = "euler", default='../../../../',
                      help = "Path to Euler.jar")
    (options, args) = parser.parse_args()
    
    from wot2013.euler.reasoner import EulerReasoner
    reasoner = EulerReasoner( options.euler )
    
    uie = ScenarioSimulator(options.input, options.output, reasoner)
    uie.actuate()
    calls = uie.get_calls_to_tsc()
    print "calls to our middleware %d [msec cputime]" % calls