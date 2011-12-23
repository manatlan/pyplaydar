**pyplaydar** try to implement [Playdar](http://www.playdar.org/) in pure python. It should work with python 2.X, and use [bottle](http://bottlepy.org/) and [cherrypy wsgi server](http://docs.cherrypy.org/stable/refman/wsgiserver/init.html).

It's fully compatible with [JS clients](http://www.playdarjs.org/)

----

**IMPORTANT NOTE** (23/12/2011)

The next release (january 2012) will come with a resolver which will be able to use the [Tomahawk's resolvers](https://github.com/tomahawk-player/tomahawk-resolvers), using [pyv8](http://code.google.com/p/pyv8/).
And with a web frontend page to test playdar's api easily in a browser !

----

Current notes about current implementation :

* **It (should) supports the original playdar's resolvers** !!!
* for web-clients : Note that it auto-authenticate all clients
* there is a **test/resolver.py** (which resolve artist/title : testa/web & testa/local)
* Currently it doesn't work on Win's machines : but can be easily corrected in file ``resolvers/__init__.py``

Current notes about implementation of the playdar protocol :

* resolve method : for a same query : it's always the same QID which is returned
* get_results : for a same file/object : it's always the same SID which is returned
