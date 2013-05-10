from os import remove, path
from optparse import OptionParser
from wot2013.proofs.goal_rules.query import QueryExecutor
from wot2013.proofs.processing.unblank_lemmas import unblank_lemmas

'''
This is the entry point for processing a file with proof results. 
'''


class UsefulInformationExtractor(object):
    
    def __init__(self, input_file, output_folder, euler_path):
        self.input_file = input_file
        self.output_folder = output_folder
        self.euler_path = euler_path
    
    def extract(self):
        tmp_file = self.output_folder + "/unblanked.n3"        
        path_to_goals = path.dirname(__file__) + "/goal_rules"
        unblank_lemmas(self.input_file, tmp_file)
        
        qe = QueryExecutor(tmp_file, self.euler_path)
        qe.execute_and_save( path_to_goals + "/lemmas.n3", self.output_folder + "/lemmas.txt" )
        qe.execute_and_save( path_to_goals + "/lemma_precedences.n3", self.output_folder + "/precedences.txt" )
        qe.execute_and_save( path_to_goals + "/rest_bindings.n3", self.output_folder + "/bindings.txt" )
        qe.execute_and_save( path_to_goals + "/rest_services.n3", self.output_folder + "/services.txt" )
        
        remove(tmp_file)


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
    uie.extract()