'''
Created on Apr 29, 2013

@author: tulvur
'''

from StringIO import StringIO
from flask import Flask, Response, request, jsonify, render_template, request
from rdflib import Graph
from rdflib.namespace import Namespace

dul = Namespace("http://www.loa.istc.cnr.it/ontologies/DUL.owl#")

app = Flask(__name__)
app.light_val = 1

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/light', methods=['GET'])
def get_light():
    return Response( render_template('light.n3', value = app.light_val) , mimetype='text/n3')

@app.route('/light', methods=['POST'])
def set_light():
    g = Graph()
    g.parse(StringIO(request.data), format="n3")
    
    triples = g.triples((None,dul["hasDataValue"],None))
    for triple in triples:
        app.light_val = int(triple[2])
        break # just one!
    
    #return g.serialize(format="n3")
    return "200 OK"


if __name__ == '__main__':
    #app.debug = True
    app.run()