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
    
    # rename to check_paths_viability ???
    def check_paths_viability(self):
        """Discards paths which cannot be followed because we do not have input data"""
        # For different actuations, they will use different caches.
        # This can be suitable
        #   (e.g if they happen at different moments, to have a fresher view of the space each time and to save needed storage for the cache)
        # or not
        #    (e.g. if they occur at the same time, you can save queries).
        space_cache = SpaceCache( self.space_manager )
        
        edges_to_remove = []
        i = 0
        for path in self.lemma_graph.get_all_paths():
            print "PATH %d" % i
            i += 1
            
            previous_node = None
            for node in path:
                lemma = self.lemma_graph.get_lemma_info(node)
                if lemma is None:
                    print "No service for %s" % node
                else:
                    if not lemma.bindings and not lemma.evidence_templates:
                        print "Call without preconditions."
                    else:
                        precond_checker = LemmaPreconditionsChecker( self.output_folder, self.reasoner, lemma.evidence_templates, space_cache )
                        precond_checker.cache_data()
                        bind = precond_checker.get_real_bindings()
                        if not bind: # empty dictio
                            # because graph cannot be changes during iteration!
                            edges_to_remove.append( ( previous_node, node ) )
                            print "could not follow the path"
                            break
                        else:
                            # store them somewhere just in case they are used later?
                            pass
                previous_node = node
            else:
                # http://docs.python.org/release/1.5/tut/node23.html
                print "successful path!"
        
        # discard non-viable paths
        for node1, node2 in edges_to_remove:
            self.lemma_graph.remove_edge( node1, node2 )
    # TODO
    #      3. almacenar bindings en algun lado por si se usan despues.
    #  Con eso:
    #      1. mirar si se podria vender lo de los caminos de forma facil
    #      2. Si no, venderlo como que se ofrece juntar ambos mundos (un poco lo de siempre... :-S)