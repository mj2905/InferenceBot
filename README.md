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

## Wiki scraping

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