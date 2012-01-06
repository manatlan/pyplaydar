**pyplaydar** try to implement [Playdar](http://www.playdar.org/) in pure python. It should work with python 2.X, and use [bottle](http://bottlepy.org/) and [cherrypy wsgi server](http://docs.cherrypy.org/stable/refman/wsgiserver/init.html).

It's fully compatible with [JS clients](http://www.playdarjs.org/)

----

**IMPORTANT NOTE** (06/01/2012)

A coming release (in january 2012) will come with a resolver which will be able to use the [Tomahawk's resolvers](https://github.com/tomahawk-player/tomahawk-resolvers), using [pyv8](http://code.google.com/p/pyv8/).
The web frontend page will be able to configure resolvers too !

----

Current notes about current implementation :

* **It (should) supports the original playdar's resolvers** !!!
* **Works on linux/windows as is** (should work on mac)
* for web-clients : Note that it auto-authenticate all clients
* there is a **test/resolver.py** (which resolve artist/title : testa/web & testa/local)

Current notes about "playdar protocol"'s implementation :

* resolve method : for a same query : it's always the same QID which is returned
* get_results : for a same file/object : it's always the same SID which is returned
