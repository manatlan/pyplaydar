**pyplaydar** try to implement [Playdar](http://www.playdar.org/) in pure python. It should work with python 2.X, and use [bottle](http://bottlepy.org/) and [cherrypy wsgi server](http://docs.cherrypy.org/stable/refman/wsgiserver/init.html).

----

**Future** (19/02/2012)

* The web frontend page will be able to let you easily configure resolvers too !

----

**Features** :

* Fully compatible with [JS clients](http://www.playdarjs.org/)
* Works with original playdar's resolvers
* Compatible with [Tomahawk's resolvers](https://github.com/tomahawk-player/tomahawk-resolvers), using [pyv8](http://code.google.com/p/pyv8/).
* Works on *nix/win as is (should work on mac)
* Web frontend to easily test resolvers
* Simple and test'able

**Current notes about "playdar protocol"'s implementation** :

* for web-clients : Note that it auto-authenticate all clients
* resolve method : for a same query : it's always the same QID which is returned
* get_results : for a same file/object : it's always the same SID which is returned

----
**What's in pyplaydar**

* **libs/** : Contains externals libs provided with pyplaydar ([bottle](http://bottlepy.org/) and [cherrypy wsgi server](http://docs.cherrypy.org/stable/refman/wsgiserver/init.html))
* **static/** : Contains static ressources used by the webserver. Currently, only a template for the web frontend.
* **resolvers/** : This folder contains the playdar's compatible resolvers. Each resolver is a folder, which contains an executable.

    * **test/** : A test resolver

        * **resolver.py** : the executable, which resolve artist/title : testa/web & testa/local), that's all ;-)

    * **tomahawk/** : the resolver which is compatible with tomahawk's resolvers

        * **resolver.py** : the executable
        * **lib.py** : a python lib (to wrap pyv8/js to a python class)
        * **tompres.py** : a command line to install/uninstall tomahawk's resolvers properly.

    * **test_a_resolver.py** : A command line to test a resolver in console.

* **pyplaydar.py** : The main file : the web server, which handle http requests for playdar protocol, and for the web frontend.
* **resolver.py** :  the playdar protocol, low level.
* **tests.py** : a lot of tests, which cover 95% of the pyplaydar's code.
* **pyplaydar.conf** : the conf file

there are a lot of readme.txt files too, which explain some things.

----
**How to start**
