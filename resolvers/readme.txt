Here are the PlayDar resolvers
==============================
(They are compatible with the original playdar system,
see http://wwww.github.com/RJ/playdar-core/tree/master/contrib)


To use a resolver in pyplaydar
------------------------------
You should configure "pyplaydar.conf", to add the path to it


To test a resolver in console
-----------------------------
you can use the provided script, like that :

    $ ./test_a_resolver.py artist track test/resolver.py

to test the dilandau tomahawk js resolver :

    $ ./test_a_resolver.py beirut nantes tomahawk/resolver.py tomahawk-resolvers/dilandau/dilandau.js
