NewsLine
========

A Python system that collects news stories over RSS via [Huginn](https://github.com/cantino/huginn) and uses [Natural Language Processing](http://www.nltk.org/) to interpret and determine up-and-coming news stories. Using [Flask](http://flask.pocoo.org/), the system presents this information to the user with a clean interface.

### Dependencies
 * MySQL >=5.5
 * [Huginn](https://github.com/cantino/huginn)
 * [CouchDB](http://couchdb.apache.org/)
 * [Stanford NLP](http://nlp.stanford.edu/software/)
 * [NLTK](http://www.nltk.org/)
 * Python 2.7
 * Java >=8

### Installation 
Be sure to get:

* couchdb-python
* MySQLDB-python
* NLTK
* Flask


### Execution

Run `python run.py` to start the webserver and the database handler.