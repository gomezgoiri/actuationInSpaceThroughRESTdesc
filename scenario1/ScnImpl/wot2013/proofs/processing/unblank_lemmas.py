import re
from optparse import OptionParser


def unblank_lemmas(input_file_path, output_file_path):
    fake_prefix = r"@prefix fake: <http://fake#>."
    with open (input_file_path, "r") as input_file:
        data = re.sub('_:lemma(?P<num>\d+)', 'fake:lemma\g<num>', input_file.read())
        with open (output_file_path, "w") as output_file:
            output_file.write( fake_prefix + "\n" + data)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input",
                      help="File to process")
    parser.add_option("-o", "--output", dest="output", default="/tmp/unblanked.n3",
                      help="Processed file")
    (options, args) = parser.parse_args()
    
    unblank_lemmas(options.input, options.output)