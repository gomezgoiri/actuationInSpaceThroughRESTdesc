'''
Created on May 21, 2013

@author: tulvur
'''

import unittest
from rdflib import URIRef
from wot2013.proofs.interpretation.variable import Variable, var_ns
from wot2013.proofs.interpretation.bindings_parser import Binding
from wot2013.proofs.interpretation.rest_parser import RESTCall, RESTServicesParser
from wot2013.proofs.interpretation.lemma_parser import Lemma



class testVariable(unittest.TestCase):
    
    def test_urize(self):
        var = Variable("x4")
        self.assertEquals( URIRef("http://localhost/var#x4"), var.urize() )
        
    def test_create_URIRefs(self):
        self.assertIsNone( Variable.create( URIRef("http://fakeuri/element1") ) )
        self.assertEquals( "x3", Variable.create( var_ns.x3 ).name )
        
    def test_create_strings(self):
        self.assertIsNone( Variable.create( "http://fakeuri/element2" ) )
        self.assertEquals( "varN", Variable.create( "http://localhost/var#varN" ).name )



class TestRESTCall(unittest.TestCase):
    
    def setUp(self):
        self.l1 = RESTCall("POST", "/resource1", "x2")        
        self.l2 = RESTCall("POST", "/resource1", "x2")
    
    def test_get_var_name(self):
        self.assertEquals( "x3", self.l1.get_var_name("x3") )
        self.assertEquals( "x4", self.l1.get_var_name("http://localhost/var#x4") )
        self.assertEquals( "x5", self.l1.get_var_name("?x5") )
    
    def test_eq_true(self):
        self.assertEquals( self.l1, self.l2 )
    
    def test_eq_false_method(self):
        self.l2.method = "GET"
        self.assertNotEquals( self.l1, self.l2 )
    
    def test_eq_false_request_uri(self):
        self.l2.request_uri = "/plant"
        self.assertNotEquals( self.l1, self.l2 )



class TestLemma(unittest.TestCase):
    
    def setUp(self):
        self.l1 = Lemma()
        self.l1.rest = RESTCall("POST", "/resource1", "x2")
        self.l1.bindings.add( Binding("x2", "http://bla") )
        self.l1.bindings.add( Binding("x1", "http://bla2") )
        
        self.l2 = Lemma()
        self.l2.rest = RESTCall("POST", "/resource1", "x2")
        self.l2.bindings.add( Binding("x1", "http://bla2") )
        self.l2.bindings.add( Binding("x2", "http://bla") )
    
    def test_eq_true(self):
        self.assertTrue( self.l1.equivalent_rest_calls( self.l2 ) )
    
    def test_eq_false_rest(self):
        # RESTCall equality already tested on TestRESTCall
        self.l2.rest.method = "GET"
        self.assertFalse( self.l1.equivalent_rest_calls( self.l2 ) )
    
    def test_eq_false_body(self):
        self.l2.set_binding("x2", "http://different_body")
        self.assertFalse( self.l1.equivalent_rest_calls( self.l2 ) )
    
    def test_eq_false_bindings(self):
        self.l1.bindings.add( Binding("x3", "http://bla5") )
        self.l2.bindings.add( Binding("x3", "http://bla4") )
        self.assertFalse( self.l1.equivalent_rest_calls( self.l2 ) )



class TestRESTServicesParser(unittest.TestCase):
    
    def test_init(self):
        rsp = RESTServicesParser( "../files/services.txt" )
        self.assertEquals( 3, len(rsp.calls) )
        self.assertItemsEqual( ["http://fake#lemma2", "http://fake#lemma3", "http://fake#lemma4"],
                             rsp.calls.keys() )
        
        expected = RESTCall("POST", "/light1/", "http://localhost/var#x0")        
        self.assertEquals( expected, rsp.calls["http://fake#lemma2"] )


if __name__ == '__main__':    
    unittest.main()