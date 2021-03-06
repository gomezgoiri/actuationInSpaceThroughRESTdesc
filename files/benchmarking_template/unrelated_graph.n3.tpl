@prefix : <http://example.org/(?id)>.
@prefix ssn: <http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix dbpedia: <http://dbpedia.org/resource/>.
@prefix dbpedia-owl: <http://dbpedia.org/ontology/>.
@prefix sweet: <http://sweet.jpl.nasa.gov/>.
@prefix ucum: <http://purl.oclc.org/NET/muo/ucum/>.
@prefix dul: <http://www.loa.istc.cnr.it/ontologies/DUL.owl#>.
@prefix foaf: <http://xmlns.com/foaf/0.1/>.
@prefix frap: <http://purl.org/frap/>.
@prefix dc: <http://purl.org/dc/elements/1.1/>.
@prefix ns1: <http://helheim.deusto.es/bizkaisense/resource/station/>.
@prefix ns10: <http://sweet.jpl.nasa.gov/2.3/propPressure.owl#>.
@prefix ns11: <http://sweet.jpl.nasa.gov/2.3/propTemperature.owl#>.
@prefix ns12: <http://purl.oclc.org/NET/ssnx/meteo/WM30#>.
@prefix ns13: <http://sweet.jpl.nasa.gov/2.3/matrIsotope.owl#>.
@prefix ns15: <http://helheim.deusto.es/bizkaisense/resource/station/AZPEIT#>.
@prefix ns5: <http://sweet.jpl.nasa.gov/2.3/propFraction.owl#>.
@prefix ns6: <http://sweet.jpl.nasa.gov/2.3/propSpeed.owl#>.
@prefix ns7: <http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#>.
@prefix ns8: <http://sweet.jpl.nasa.gov/2.3/matrElementalMolecule.owl#>.
@prefix ns9: <http://sweet.jpl.nasa.gov/2.3/matrAerosol.owl#>.
@prefix angle: <http://purl.oclc.org/NET/muo/ucum/unit/plane-angle/>.

# Sensor / station

:AZPEIT a ssn:Sensor;
     ssn:observes ns12:WindDirection,
         ns9:PM10,
         ns9:PM2point5,
         ns7:CO,
         ns7:NO,
         ns7:NO2,
         ns7:SO2,
         ns8:O3,
         ns13:Radiation,
         ns5:Humidity,
         ns10:BarometricPressure,
         ns6:WindSpeed,
         ns11:Temperature;
     dc:description "Azpeitia (AZPEIT) @ Azpeitia (Alto Urola/Urola garaia (UROLA) - GIPUZKOA)";
     dc:identifier "AZPEIT";
     dc:title "Azpeitia";
     dul:hasLocation ns15:point;
     dul:nearTo <http://www.geonames.org/6325201> .

# Measure of one of the sensors
:measure1 a ssn:Observation;
    ssn:observationResult :sensoroutput;
    ssn:observedBy :AZPEIT;
    ssn:observedProperty ns12:WindDirection;
    dc:date "2009-05-01T00:00:00".

:sensoroutput a ssn:SensorOutput;
    ssn:hasValue :outputvalue. 

:outputvalue a ssn:ObservationValue;
    dul:hasDataValue "268"^^<http://www.w3.org/2001/XMLSchema#integer>;
    dul:isClassifiedBy angle:degree.