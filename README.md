**pyplaydar** try to implement [Playdar](http://www.playdar.org/) in pure python. It should work with python 2.X, and use [bottle](http://bottlepy.org/) and [cherrypy wsgi server](http://docs.cherrypy.org/stable/refman/wsgiserver/init.html).

It's fully compatible with [JS clients](http://www.playdarjs.org/)


Current notes about current implementation :

* Note that it auto-authenticate all clients
* Currently, it uses its own *stupid resolvers* (which are plugin'able), but I'd like to make it compatible with original playdar's resolvers.
* there is a **test resolver** (which resolve artist/title : testa/web & testa/local)

Current notes about implementation of the playdar protocol :

* resolve method : for a same query : it's always the same QID which is returned
* get_results : for a same file/object : it's always the same SID which is returned
