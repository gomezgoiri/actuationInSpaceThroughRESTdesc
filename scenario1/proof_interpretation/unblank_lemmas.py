import re
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-i", "--input", dest="input",
                  help="File to process")
parser.add_option("-o", "--output", dest="output", default="/tmp/unblanked.n3",
                  help="Processed file")
(options, args) = parser.parse_args()


fake_prefix = r"@prefix fake: <http://fake#>."

with open (options.input, "r") as input_file:
  data = re.sub('_:lemma(?P<num>\d+)', 'fake:lemma\g<num>', input_file.read())
  with open (options.output, "w") as output_file:
    output_file.write( fake_prefix + "\n" + data)