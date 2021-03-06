'''
 Copyright (C) 2013 onwards University of Deusto
  
 All rights reserved.
 
 This software is licensed as described in the file COPYING, which
 you should have received as part of this distribution.
 
 This software consists of contributions made by many individuals, 
 listed below:
 
 @author: Aitor Gómez Goiri <aitor.gomez@deusto.es>
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
    
    def _parse_middleware_calls(self, to_parse):
        prog = re.compile(r"calls to our middleware (\d+) \[msec cputime\]")
        return ( int(el) for el in prog.findall(to_parse) )
    
    def parse(self):
        with open (self.input_path, "r") as input_file:
            content = input_file.read()
            starting = sum( self._parse_starting(content) )
            reasoning = sum( self._parse_reasoning(content) )
            total = starting + reasoning
            print "Reasoning total: %d (starting: %d, reasoning: %d)" % ( total, starting, reasoning)
            
            middleware = sum( self._parse_middleware_calls(content) ) # just one, but anyway...
            print "Middleware calls: %d" % middleware

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input", default="../../files/simulation_result.out",
                      help="File to process with the EYE output")
    (options, args) = parser.parse_args()
    p = EYEParser( options.input )
    p.parse()