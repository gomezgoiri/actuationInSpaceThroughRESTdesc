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
    
    def __init__(self, input_file, euler_path='../../../../../'):
        self.input_file = input_file
        self.euler_path = euler_path + "" if euler_path.endswith("/") else "/"
    
    def _execute_query(self, query_file):
        call = ['java', '-jar', self.euler_path + 'Euler.jar', '--nope',
                            self.input_file, '--query', query_file]
        return subprocess.check_output( call )
    
    def execute_and_save(self, query_file, output_file_path):
        with open (output_file_path, "w") as output_file:
            output_file.write( self._execute_query(query_file) )
    
    def execute_and_show(self, query_file):        
        if self.output_file_path is None:
            print self._execute_query(query_file)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest = "input",
                      help = "File to process")
    parser.add_option("-q", "--query", dest = "query",
                      help = "File with the N3QL goal")
    parser.add_option("-o", "--output", dest = "output", default=None,
                      help = "File where the results will be written. If no results are provided the result will be shown in the screen.")
    parser.add_option("-e", "--euler", dest = "euler", euler_path='../../../../../',
                      help = "Path to Euler.jar")
    (options, args) = parser.parse_args()

    qe = QueryExecutor(options.input, options.euler)
    if options.output is None:
        qe.execute_and_show(options.query)
    else:
        qe.execute_and_save(options.query, options.output)