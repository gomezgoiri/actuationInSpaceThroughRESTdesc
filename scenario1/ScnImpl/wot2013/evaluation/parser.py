'''
Created on May 31, 2013

@author: tulvur
'''

import re
from numpy import sum
from optparse import OptionParser

class EYEParser(object):
    def __init__(self, ip_file_path):
        self.input_path = ip_file_path
    
    def _parse_starting(self, to_parse):
        prog = re.compile(r"starting (\d+) \[msec cputime\]")
        return ( int(el) for el in prog.findall(to_parse) )
    
    def _parse_reasoning(self, to_parse):
        prog = re.compile(r"reasoning (\d+) \[msec cputime\]")
        return ( int(el) for el in prog.findall(to_parse) )
    
    def parse(self):
        with open (self.input_path, "r") as input_file:
            content = input_file.read()
            starting = sum( self._parse_starting(content) )
            reasoning = sum( self._parse_reasoning(content) )
            total = starting + reasoning
            print "Total: %d (starting: %d, reasoning: %d)" % ( total, starting, reasoning)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input", default="../../files/simulation_result.out",
                      help="File to process with the EYE output")
    (options, args) = parser.parse_args()
    p = EYEParser( options.input )
    p.parse()