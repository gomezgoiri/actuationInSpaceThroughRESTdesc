'''
Created on May 20, 2013

@author: tulvur
'''
from tempfile import mkdtemp

from wot2013.tsc.space_cache import SpaceCache
from wot2013.tsc.actuation.plan import ActuationPlanCreator
from wot2013.tsc.actuation.preconditions import LemmaPreconditionsChecker
from wot2013.proofs.extract_info import UsefulInformationExtractor
from wot2013.proofs.interpretation.graphs import LemmaPrecedencesGraph
from wot2013.proofs.interpretation.lemma_parser import LemmaParser


class ActuationStarterNode(object):
    
    def __init__(self, query_goal_path, output_folder, reasoner):
        self.query_goal_path = query_goal_path
        self.output_folder = mkdtemp( dir = output_folder )
        self.reasoner = reasoner
    
    def add_space_manager(self, space_manager):
        # Used for:
        #   1) provide clues to the actuation plan creator
        #   2) provide where to query to the "space_cache" :)
        self.space_manager = space_manager
    
    def create_plan(self):
        apc = ActuationPlanCreator( self.query_goal_path, self.output_folder, self.reasoner )
        self.plan_path = apc.create_plan( self.space_manager.get_clues() )
    
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
    
    def discard_paths(self):
        """Discards paths which cannot be followed because we do not have input data"""
        # For different actuations, they will use different caches.
        # This can be suitable
        #   (e.g if they happen at different moments, to have a fresher view of the space each time and to save needed storage for the cache)
        # or not
        #    (e.g. if they occur at the same time, you can save queries).
        space_cache = SpaceCache( self.space_manager )
        
        i = 0
        for path in self.lemma_graph.get_all_paths():
            print "PATH %d" % i
            i += 1
            
            for node in path:
                rest = self.lemma_graph.get_rest_call(node)
                if rest is None:
                    print "No service for %s" % node
                else:
                    precond_checker = LemmaPreconditionsChecker( self.output_folder, self.reasoner, rest.evicence_templates, space_cache )
                    precond_checker.cache_data()
                    bind = precond_checker.get_real_bindings()
                    if bind is None:
                        print "could not follow the path"
            
    # TODO
    #      1. con el query creado y el cache.n3, sacar las pruebas
    #      2. extraer de las pruebas los bindings
    #      3. almacenarlos en algun lado por si se usan despues.
    #      4. comprobar siguiente lemma y ver que caminos funcionan
    #  Con eso:
    #      1. mirar si se podria vender lo de los caminos de forma facil
    #      2. Si no, venderlo como que se ofrece juntar ambos mundos (un poco lo de siempre... :-S)