import subprocess
from optparse import OptionParser

'''
This module invokes Euler (EYE) in this way:

java -jar ../../Euler.jar --nope result_file.n3 --query goal_file.n3 > refined_results.n3 
'''

class QueryExecutor(object):
    """
    Executes queries over a given proof n3 file.
    """
    
    def __init__(self, input_file, reasoner):
        self.input_file = input_file
        self.reasoner = reasoner
    
    def execute_and_save(self, query_file, output_file_path):
        with open (output_file_path, "w") as output_file:
            output_file.write( self.reasoner.query(self.input_file, query_file) )
    
    def execute_and_show(self, query_file):
        print self.reasoner.query( self.input_file, query_file )


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest = "input",
                      help = "File to process")
    parser.add_option("-q", "--query", dest = "query",
                      help = "File with the N3QL goal")
    parser.add_option("-o", "--output", dest = "output", default=None,
                      help = "File where the results will be written. If no results are provided the result will be shown in the screen.")
    parser.add_option("-e", "--euler", dest = "euler", default='../../../../../',
                      help = "Path to Euler.jar")
    (options, args) = parser.parse_args()
    
    from wot2013.euler.reasoner import EulerReasoner
    reasoner = EulerReasoner( options.euler )
    
    qe = QueryExecutor(options.input, reasoner)
    if options.output is None:
        qe.execute_and_show(options.query)
    else:
        qe.execute_and_save(options.query, options.output)