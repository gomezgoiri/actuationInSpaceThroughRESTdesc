'''
Created on May 20, 2013

@author: tulvur
'''
from tempfile import mkdtemp

from wot2013.tsc.actuation.plan import ActuationPlanCreator
from wot2013.proofs.extract_info import UsefulInformationExtractor
from wot2013.proofs.interpretation.graphs import LemmaPrecedencesGraph
from wot2013.proofs.interpretation.lemma_parser import LemmaParser



class ActuationStarterNode(object):
    
    def __init__(self, query_goal_path, output_folder, reasoner):
        self.query_goal_path = query_goal_path
        self.output_folder = mkdtemp( dir = output_folder )
        self.reasoner = reasoner
        self.apc = ActuationPlanCreator( query_goal_path, self.output_folder, reasoner )
    
    def add_clues(self, clues):
        self.apc.add_clues(clues)
    
    def create_plan(self):
        self.plan_path = self.apc.create_plan()
    
    def process_plan(self):
        uie = UsefulInformationExtractor( self.plan_path, self.output_folder, self.reasoner )
        uie.extract_all()
        
        self.lemma_graph = LemmaPrecedencesGraph(self.output_folder + "/" + UsefulInformationExtractor.get_output_filename("precedences"))
        
        lp = LemmaParser( self.output_folder + "/" + UsefulInformationExtractor.get_output_filename("services"),
                          self.output_folder + "/" + UsefulInformationExtractor.get_output_filename("bindings"),
                          self.output_folder + "/" + UsefulInformationExtractor.get_output_filename("evidences") )
        self.lemma_graph.add_lemmas_info( lp.lemmas )
        self.lemma_graph.create_nx_graph()
        #self.lemma_graph.to_image( output_file = options.output + "/lemma_precedences.png" )
        #self.lemma_graph.to_gml( output_file = self.output_folder + "/lemma_precedences.gml" )
    
    def discard_paths(self, space_cache):
        """Discards paths which cannot be followed because we do not have input data"""        
        i = 0
        for path in self.lemma_graph.get_all_paths():
            print "PATH %d" % i
            i += 1
            
            for node in path:
                rest = self.lemma_graph.get_rest_call(node)
                if rest is None:
                    print "No service for %s" % node
                else:
                    for template in rest.evicence_templates:
                        space_cache.add_query( template.get_template() )
                    space_cache.launch_requests()
                    #print rest
                    print "------"
                    print space_cache.cache.serialize(self.output_folder + "/cached.n3", format="n3")
                    
                    self._create_fake_query_rule( rest.evicence_templates )
    
    def _create_fake_query_rule(self, templates):
        tpls_to_str = ""
        for t in templates:
            tpls_to_str += t.n3()
        
        fq = """
{
    %s
} => {
    %s
}            
        """ % (tpls_to_str, tpls_to_str)
        
        with open(self.output_folder + "/query.n3", 'w') as fil:
            fil.write(fq)
            
    # TODO
    #      1. con el query creado y el cache.n3, sacar las pruebas
    #      2. extraer de las pruebas los bindings
    #      3. almacenarlos en algun lado por si se usan despues.
    #      4. comprobar siguiente lemma y ver que caminos funcionan
    #  Con eso:
    #      1. mirar si se podria vender lo de los caminos de forma facil
    #      2. Si no, venderlo como que se ofrece juntar ambos mundos (un poco lo de siempre... :-S)