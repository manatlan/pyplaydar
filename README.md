**pyplaydar** try to implement [Playdar](http://www.playdar.org/) in pure python.

it's fully compatible with [JS clients](http://www.playdarjs.org/)

It should be compatible with python 2.X, and use [bottle](http://bottlepy.org/) and [cherrypy wsgi server](http://docs.cherrypy.org/stable/refman/wsgiserver/init.html)

Current notes:

    * Note that it auto-authenticate all clients
    * Implemented resolver do nothing ;-), but are plugin'able
    * there is a **test resolver** (which resolve artist/title : testa/web & testa/local)
