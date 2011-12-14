#!/usr/bin/python
# -*- coding: utf-8 -*-
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
import sys,os

if __name__ == "__main__":
    #~ sys.argv=["","test/resolver.py","my_artit","his_track"]

    if len(sys.argv)==4:
        path,artist,track = sys.argv[1:]
        p=Resolver( path )
        print "SETTINGS:"
        for k,v in p.settings.items():
            print "-",k,"=",v
        print p.query( artist=artist,track=track,qid="123456789" )
    else:
        print """USAGE: %s <path_to_resolver> <artist> <track>
Script helper to test a resolver""" % os.path.basename(sys.argv[0])
