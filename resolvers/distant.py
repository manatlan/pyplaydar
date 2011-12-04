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

class Distant(Resolver):

    priority=90
    timeout=5

    def __init__(self):
        print self.__class__.__name__,"CREATED !!!"

    def resolve( self, qid, artist, album, title ):
        data = {
            "qid": qid,
            "results": [],
        }

        return data
