########################################################################
##
##    Copyright (C) 2011 manatlan manatlan[at]gmail(dot)com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation; version 2 only.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
########################################################################

from __init__ import Resolver

class Test(Resolver):

    priority=1
    timeout=1

    def __init__(self):
        print self.__class__.__name__,"CREATED !!!"

    def resolve( self, qid, artist, album, title ):
        data = {
            "qid": qid,
            "results": [],
        }

        if artist=="testa" and title=="web":
            data["results"].append( {
                "artist": artist,
                "track": title,
                "duration": 0,
                "source": self.__class__.__name__,
                "extension": "mp3",
                "mimetype": "audio/mp3",
                "url": "http://manella.free.fr/mp3/manella_-_zmorlockfunk.mp3",
                "score":1,
                }
            )

        if artist=="testa" and title=="local":
            data["results"].append( {
                "artist": artist,
                "track": title,
                "duration": 0,
                "source": self.__class__.__name__,
                "extension": "mp3",
                "mimetype": "audio/mp3",
                "url": "libs/bottle.pyc",
                "score":1,
                }
            )

        return data

if __name__=="__main__":
    r=Test()
    print r.resolve("x","testa","","")
    print r.resolve("x","testa","","web")
    print r.resolve("x","testa","","local")
