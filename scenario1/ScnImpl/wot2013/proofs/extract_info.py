from os import remove, path
from optparse import OptionParser
from wot2013.proofs.goal_rules.query import QueryExecutor
from wot2013.proofs.processing.unblank_lemmas import unblank_lemmas

'''
This is the entry point for processing a file with proof results. 
'''


class UsefulInformationExtractor(object):
        
    EXTRACTIONS = {# identifier: (input_filename, output_filename)
                   "precedences": ("lemma_precedences.n3", "precedences.txt"),
                   "bindings": ("rest_bindings.n3", "bindings.txt"),
                   "lemmas": ("lemma_precedences.n3", "lemmas.txt"),
                   "services": ("rest_services.n3", "services.txt"),
                   "rest_services": ("rest_services.n3", "services.txt"),
                   }
    
    def __init__(self, input_file, output_folder, euler_path):
        self.input_file = input_file
        self.output_folder = output_folder
        self.euler_path = euler_path
        self.path_to_goals = path.dirname(__file__) + "/goal_rules"
    
    def start(self):
        self.tmp_file = self.output_folder + "/unblanked.n3"
        unblank_lemmas( self.input_file, self.tmp_file )
        self.default_qe = QueryExecutor( self.tmp_file, self.euler_path )
        
    def stop(self):
        remove( self.tmp_file )
    
    @staticmethod
    def get_input_filename(identifier):
        return UsefulInformationExtractor.EXTRACTIONS[identifier][0]
    
    @staticmethod
    def get_output_filename(identifier):
        return UsefulInformationExtractor.EXTRACTIONS[identifier][1]
    
    def extract_item(self, identifier):
        input_name = UsefulInformationExtractor.get_input_filename(identifier)
        output_name = UsefulInformationExtractor.get_output_filename(identifier)
        self.default_qe.execute_and_save( self.path_to_goals + "/" + input_name,
                                          self.output_folder + "/" + output_name )
    
    def extract_all(self):
        self.start()
        
        #self.extract_item("lemmas") # no longer needed, I think # TODO check
        self.extract_item("precedences")
        self.extract_item("bindings")
        self.extract_item("services")
        
        self.stop()
        # no longer useful since it is parsed using rest_parser module 
        #qe = QueryExecutor( self.output_folder + "/services.txt", self.euler_path )
        #qe.execute_and_save( self.path_to_goals + "/invocation_rules.n3", self.output_folder + "/invocations.txt" )


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input",
                      help="File to process")
    parser.add_option("-o", "--output", dest="output", default="/tmp",
                      help="Output folder where the processed results will be written.")
    parser.add_option("-e", "--euler", dest = "euler", default='../../../../',
                      help = "Path to Euler.jar")
    (options, args) = parser.parse_args()

    uie = UsefulInformationExtractor(options.input, options.output, options.euler)
    uie.extract_all()