#!/usr/bin/python
# -*- coding: utf-8 -*-
########################################################################
##
##    Copyright (C) 2012 manatlan manatlan[at]gmail(dot)com
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
import re,string,sys,os
import json
from subprocess import Popen,PIPE
from struct import pack,unpack

import logging
logging.basicConfig(format='>%(asctime)s (%(levelname)s) %(message)s',level=logging.INFO,datefmt="%m/%d/%y %H:%M:%S")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log= lambda x: logger.info("PLUGIN: "+x)
logerr= lambda x: logger.error("PLUGIN: "+x)


#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+ playdar stdin/out protocol
def mkquery(**k):
    cmd=json.dumps(k)
    return pack('!L', len(cmd)) + cmd

def mkresp(std):
    length = std.read(4)
    if length:
        length = unpack('!L', length)[0]
        if length:
            return std.read(length).strip()
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+


class Resolver(object):
    """ class to handle a resolver (communication(sync) thru stdin/stdout)"""
    def __init__(self,cmds):
        # Specific case for py file on win machines (without shebang line)
        if cmds[0].endswith(".py"): cmds.insert(0,sys.executable)

        self._cmds=cmds
        self._p = Popen(self._cmds, shell=False,stdout=PIPE,stdin=PIPE)
        # load settings
        try:
            self.settings = json.loads( mkresp(self._p.stdout) )
        except:
            raise Exception("Resolver %s can't be instanciate (com error)" % cmds)
        self.name=self.settings["name"]
        log(self.name+" INTANCIATED")


    def query(self,**kargs):    # Synchronous /!\
        #~ print "+++",kargs
        msg=mkquery(**kargs)
        log(self.name+" QUERY : "+msg[4:])
        self._p.stdin.write( msg )
        self._p.stdin.flush()
        r=mkresp(self._p.stdout)
        log(self.name+" RETURN : "+str(r))
        return json.loads( r )

    def __repr__(self):
        return "<Resolver:%s:%s>"%(str(self._cmds),str(self.settings))

def test_this():
    try:
        import PyV8
        ISV8=True
    except ImportError:
        ISV8=False

    r=Resolver(["test/resolver.py"])
    assert type( r.settings )==dict
    assert r.settings["name"]==u"Test Resolver"
    assert r.settings["_msgtype"]==u"settings"

    assert len( r.query( artist="testa",track="XqaqaXXX",qid="15111516516" )["results"]) == 0
    assert len( r.query( artist="testa",track="local",qid="1511151651" )["results"]) == 1
    assert len( r.query( artist="testa",track="web",qid="151115165" )["results"]) == 1

    # test tomahawk resolver
    if ISV8:
        r=Resolver(["tomahawk/resolver.py","just_for_tests.js"])
        assert type( r.settings )==dict
        assert r.settings["name"]==u"Dummy Resolver"
        assert r.settings["_msgtype"]==u"settings"
        d=r.query(artist="a",qid=123456,track="t")
        assert d["qid"]==123456
        assert d["_msgtype"]=="results"
        assert len(d["results"])==1
        r=d["results"][0]
        assert "url" in r
        assert "artist" in r
        assert "track" in r
        assert "source" in r

    if os.path.isfile("tomahawk/tomahawk-resolvers/dilandau/dilandau.js"):
        p=Resolver(["tomahawk/resolver.py","tomahawk-resolvers/dilandau/dilandau.js"])
        print p.query( artist="beirut",track="nantes",qid="15111516516")

if __name__ == "__main__":

    test_this()
