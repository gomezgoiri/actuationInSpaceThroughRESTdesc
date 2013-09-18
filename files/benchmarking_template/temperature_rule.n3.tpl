@prefix : <http://example.org/thermo/(?id)>.
@prefix http: <http://www.w3.org/2011/http#>.
@prefix ssn: <http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#>.
@prefix dbpedia: <http://dbpedia.org/resource/>.
@prefix dbpedia-owl: <http://dbpedia.org/ontology/>.
@prefix sweet: <http://sweet.jpl.nasa.gov/>.
@prefix ucum: <http://purl.oclc.org/NET/muo/ucum/>.
@prefix dul: <http://www.loa.istc.cnr.it/ontologies/DUL.owl#>.
@prefix foaf: <http://xmlns.com/foaf/0.1/>.
@prefix frap: <http://purl.org/frap/>.
@prefix op: <http://www.w3.org/2000/10/swap/math#>.
@prefix lookfor: <http://pending.of/search/>.


{
  :heater a dbpedia:Heater ;
         dul:hasLocation ?room .

  ?thermo a ssn:Sensor ;
              a dbpedia:Thermometer ;
              ssn:observes sweet:Heat ; # TODO: check a real prop
              dul:hasLocation ?room ;
              dul:hasDataValue ?last_value ;
              dul:state "off" .


  # ...preferencia de luz a ?desired_value...
  ?preference a frap:Preference ;
              frap:about ?pab .

  ?pab a frap:Pattern ;
       a ssn:ObservationValue ;
       dul:isClassifiedBy  ucum:celsius ;
       dul:hasDataValue ?desired_value .

   
   # ...y ?desired_value > ?last_value
   #?desired_value op:greaterThan ?last_value . # op:numeric-greater-than
}
=>
{
  _:request http:methodName "POST";
            http:requestURI "/heater/";
            http:body ?preference; # and ?last_value and ?light (or if they already exist is not necessary?)
            http:resp [ http:body _:outputvalue ].
  
  # is dynamic
  # ?thermo dul:hasDataValue ?desired_value . # avoid confussions due to our oversimplification!
  ?thermo dul:state "on" .
}.
