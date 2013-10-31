Actuation through space-based computing and RESTdesc
====================================================

> Failure is simply the opportunity to begin again,
> this time more intelligently.
> <cite>Henry Ford</cite>


With this project we intended to explore the use of [RESTdesc](http://restdesc.org/) together with our own triplespace-based computing middleware.

Initially, we also wanted to explore how to use this space to discriminate the better path to achieve a goal when more than one where found by the reasoner.
However, the time went by and a deadline made us present what we had at that moment (i.e. what this project contains).

I am not sure whether we will resume this work, so I publish it just in case somebody out there finds it helpful for something.


Directories
-----------

 * _files_ contains rules and scripts for different scenarios.
  * _rules&#95;01_ to _rules&#95;05_ are incremental attempts to achieve the initially envisaged scenario.
  * _rules&#95;05&#95;simplified_ contains an equivalent example to _rules&#95;05_ misusing some ontologies to make files less verbosed (both to show them in the paper and to make easier to understand them to a possible reader).
  * _math&#95;example_ is a simple int comparison example.
  * _benchmarking&#95;template_ contains the scripts to prepare the experimental environment of the paper's evaluation.
 * ScnImpl: contains a Python project with the code required for the scripts under _files_


Installation
------------

You will need to install the requirements specified by _ScnImpl/requirements.txt_ in you python environment.

    pip install -r requirements.txt

BTW, I used [virtualenvwrapper](https://bitbucket.org/dhellmann/virtualenvwrapper) and I'm afraid that I might keep some references to my own environment in the scripts ( _workon wot2013_ ). Just fix them.


Basic usage
-----------

I know, the project is underdocumented.

Under _files_, you have several _REST descriptions_ and scripts that you can read and run to understand the project. Besides, you have the code invoked by these scripts in the _ScnImpl_ project.

If you don't understand something but you are really interested in it, just mail me and I'll do my best to help you ;-)


Feedback on the project
-----------------------

With this project's work, we presented a paper to [WoT 2013](http://www.webofthings.org/wot/2013/).
Unfortunately, the paper was rejected.
However, apart of sharing my unfruitful work with you, I also want to share the feedback I obtained.

The following criticisms/suggestions are applicable to the content of this project:

 * _The challenges seem to arise due to the constraints of the devices hosting the middleware and the middleware approach itself i.e. the use of distributed knowledge and semantic reasoning to prove actuation happened, not anything inherent in building a smart space._
 * _It seems as though the system would perform best if a given node had all of the knowledge it needed (e.g. all sensors and actuators on one node)._
 _This scenario could serve as the baseline for an interesting experiment that explores the tradeoffs related to knowledge distribution in the system._
 _With greater distribution (e.g. moving required sensors and actuators to other nodes) and less memory and computing resources per node,_
 _I'd expect the reasoner in a given node to make more middleware queries and the overall time taken to increase._
 _It would be interesting to see how the system performance behaves as the amount of distributed knowledge and nodes involved in completing a goal increases._
 * Some of the rules used give the applications logic, not service description.
 * _From a practical point of view it seems very doubtful that a programmer will be able to define the required rules without errors._
   _So even though your approach might provide a technical solution at best you are achieving a trade-off: more flexibility is traded for less usability, more sources of errors etc._

License
-------

Check [ScnImpl/COPYING.txt](https://github.com/gomezgoiri/actuationInSpaceThroughRESTdesc/blob/master/ScnImpl/COPYING.txt).
