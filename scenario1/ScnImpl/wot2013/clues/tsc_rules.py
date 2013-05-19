from optparse import OptionParser
from rdflib import Graph, RDF, RDFS


class TSCRulesCreator(object):
    
    def __init__(self, input_file_path, output_file_path):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path

    def _extract_predicates(self):
        g = Graph()
        g.parse(self.input_file_path, format="n3")
        
        predicates = set()
        for predicate in g.predicates(None, None):
            # Too general properties to predict anything... :-S
            if not predicate.startswith( str(RDF) ) or predicate.startswith( str(RDFS) ):
                predicates.add( str(predicate) )
        return predicates

    def _get_rule(self, predicate):
        return """
{
    ?subject ?predicate ?object .
}
=>
{
    # something to call TSC
    _:tsc tsc:primitive tsc:query . 
    ?s1 <%s> ?o2 .
}.
                """ % (predicate)

    def create_rules_file(self):
        predicates = self._extract_predicates()
        fake_pref = """@prefix tsc: <http://www.morelab.deusto.es/tsc#>.
tsc:sub tsc:pred tsc:obj .
        """
    
        if self.output_file_path is not None:
            with open (self.output_file_path, "w") as output_file:
                output_file.write( fake_pref + "\n")
                for predicate in predicates:
                    output_file.write( self._get_rule(predicate) + "\n")
                output_file.write( self._get_rule(str(RDF.type)) + "\n")
        else:
            output_file.write( fake_pref + "\n")
            for predicate in predicates:
                print self._get_rule(predicate)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input",
                      help="N3 file to process")
    parser.add_option("-o", "--output", dest="output", default=None,
                      help="Predicates of the input file")
    (options, args) = parser.parse_args()
    
    rule_creator = TSCRulesCreator(options.input, options.output)
    rule_creator.create_rules_file()