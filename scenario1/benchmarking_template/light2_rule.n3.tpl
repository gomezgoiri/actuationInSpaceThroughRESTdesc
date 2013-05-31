@prefix : <http://example.org/light_scen/light/(?id)>.
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
  # Uppps almost all the premise is right, but :lamp2 does not exist in the space!!!
  :lamp2 a dbpedia:Lamp ;
         dul:hasLocation ?room .

  ?light_snr1 a ssn:Sensor;
              ssn:observes sweet:Light ;
              dul:hasLocation ?room ;
              dul:hasDataValue ?last_value .


  # ...preferencia de luz a ?desired_value...
  ?preference a frap:Preference ;
              frap:about ?pab .

  ?pab a frap:Pattern ;
       a ssn:ObservationValue ;
       dul:isClassifiedBy  ucum:lux ;
       dul:hasDataValue ?desired_value .

   
   # ...y ?desired_value > ?last_value
   ?desired_value op:greaterThan ?last_value . # op:numeric-greater-than
}
=>
{
  # Hago llamada HTTP POST a light/
  _:request http:methodName "POST";
            http:requestURI "/light/";
            http:body ?preference; # and ?last_value and ?light (or if they already exist is not necessary?)
            http:resp [ http:body _:outputvalue ].
  
  # para obtener que el sensor ahora tiene luz a 21
  ?light_snr1 dul:hasDataValue 21 .

}.
