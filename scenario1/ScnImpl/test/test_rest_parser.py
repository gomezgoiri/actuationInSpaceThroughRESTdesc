'''
Created on Nov 28, 2011

@author: tulvur
'''

import unittest
from rdflib import URIRef
from wot2013.proofs.interpretation.rest_parser import RESTCall, RESTServicesParser

class TestRESTCall(unittest.TestCase):
    
    def setUp(self):
        self.rc1 = RESTCall("POST", "/resource1", "x2")
        self.rc1.add_binding("x2", "http://bla")
        self.rc1.add_binding("x1", "http://bla2")
        
        self.rc2 = RESTCall("POST", "/resource1", "x2")
        self.rc2.add_binding("x1", "http://bla2")
        self.rc2.add_binding("x2", "http://bla")
    
    def test_get_var_name(self):
        self.assertEquals( "x3", self.rc1.get_var_name("x3") )
        self.assertEquals( "x4", self.rc1.get_var_name("http://localhost/var#x4") )
        self.assertEquals( "x5", self.rc1.get_var_name("?x5") )
    
    def test_eq_true(self):
        self.assertEquals( self.rc1, self.rc2 )
    
    def test_eq_false_method(self):
        self.rc2.method = "GET"
        self.assertNotEquals( self.rc1, self.rc2 )
    
    def test_eq_false_request_uri(self):
        self.rc2.request_uri = "/plant"
        self.assertNotEquals( self.rc1, self.rc2 )
    
    def test_eq_false_body(self):
        self.rc2.bindings["x2"] = "http://different_body"
        self.assertNotEquals( self.rc1, self.rc2 )
    
    def test_eq_false_bindings(self):
        self.rc1.add_binding("x3", "http://bla5")
        self.rc2.add_binding("x3", "http://bla4")
        self.assertNotEquals( self.rc1, self.rc2 )


class TestRESTServicesParser(unittest.TestCase):
    
    def test_init(self):
        rsp = RESTServicesParser( "../files/services.txt", "../files/bindings.txt" )
        self.assertEquals( 3, len(rsp.calls) )
        self.assertItemsEqual( [URIRef("http://fake#lemma2"), URIRef("http://fake#lemma3"), URIRef("http://fake#lemma4")],
                             rsp.calls.keys() )
        
        expected = RESTCall("POST", "/light1/", "http://localhost/var#x0")
        expected.add_binding("http://localhost/var#x0", "http://example.org/light_scen#light")
        
        self.assertEquals( expected, rsp.calls[URIRef("http://fake#lemma2")] )


if __name__ == '__main__':    
    unittest.main()