**pyplaydar** try to implement [Playdar](http://www.playdar.org/) in pure python. It should work with python 2.X, and use [bottle](http://bottlepy.org/) and [cherrypy wsgi server](http://docs.cherrypy.org/stable/refman/wsgiserver/init.html).

----

**IMPORTANT NOTE** (06/01/2012)

A coming release (in january 2012) will come with a resolver which will be able to use the [Tomahawk's resolvers](https://github.com/tomahawk-player/tomahawk-resolvers), using [pyv8](http://code.google.com/p/pyv8/).
The web frontend page will be able to configure resolvers too !

----

Features :

* Fully compatible with [JS clients](http://www.playdarjs.org/)
* Works with original playdar's resolvers
* Works on *nix/win as is (should work on mac)
* Web frontend to easily test resolvers
* there is only a **test/resolver.py** (which resolve artist/title : testa/web & testa/local)
* Simple and test'able

Current notes about "playdar protocol"'s implementation :

* for web-clients : Note that it auto-authenticate all clients
* resolve method : for a same query : it's always the same QID which is returned
* get_results : for a same file/object : it's always the same SID which is returned
