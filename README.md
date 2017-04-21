# InferenceBot - Digital Humanities
This bot uses predicate logic to infer concepts from the facts that it has been able to fetch on Wikipast pages.

## Inference engine

## Data structures
Data that has been collected from the internet can be stored using classes from the Datastructs
module. The classes available are the following:

Classes that can be converted into an Atom:

* Person (Name, Lastname)
* Location (Name)
* Date (Year, Month, Day, Hour, Minute, Second)

Classes that can be converted into a Predicate

* Events
    * Birth: [Person, Date]
    * Encounter: [Person 1, Person 2, Date]

Each class in this module provides either a method to convert the object into an Atom 
or a Predicate for the inference engine. Refer to the documentation in the source code for further details.

## Wiki scrapping
### Scrapping engine

### Scrapper classes
The scrapper classes look for so called "concepts". Concepts are features appearing in pages that are of certain 
relevance for the Bot. For example, an encounter between two individuals is a concept.
The actual scrapping work is done in scrapper classes. Each of those classes specialize in scrapping a given concept
and they must define the following functions:

* `keyword`: returns the keyword used to identify useful concepts  
* `find`: returns a list of tags in which the concept was identified
* `extract`: return an object corresponding to the concept 

To add scrapper classes, simply make them inherit from the abstract Scrapper class in WikiScrapper.py file and
implement the function listed above.
 
Refer to the documentation in the source code for further details.

## Wiki editing

## Wiki format specifications

## Test pages

### Title

A list of all test pages can be found here: [InferenceBot - Liste des pages de test](http://wikipast.epfl.ch/wikipast/index.php/InferenceBot_-_Listes_des_pages_de_test)

In order to test the behavior of the bot, all test pages must have a name starting with "InferenceBot page test - "
followed by the name of the page. For example, a test page for an individual named John Doe would have the following
title:

```
InferenceBot page test - John Doe
```

### Format
Unles mentionned otherwise, Wikipast pages format should follow the convention adopted in class.
#### People
Dummy people name can be generated from [this website](http://www.behindthename.com/random/). Use of ancient latin
names is encouraged as it is easier to differentiate them from actual people names.

Facts and events regarding a person should be under a section named `Biographie`.
#### Places

#### Event