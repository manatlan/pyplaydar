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
import re,string,sys
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
    def __init__(self,cmd):
        # Specific case for py file on win machines (without shebang line)
        if cmd.endswith(".py"): cmd=[sys.executable,cmd]

        self._cmd=cmd
        self._p = Popen(self._cmd, shell=False,stdout=PIPE,stderr=PIPE,stdin=PIPE)
        # load settings
        self.settings = json.loads( mkresp(self._p.stdout) )
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
        return "<Resolver:%s:%s>"%(str(self._cmd),str(self.settings))


if __name__ == "__main__":
    p=Resolver("test/resolver.py")
    assert len( p.query( artist="testa",track="XqaqaXXX",qid="15111516516" )["results"]) == 0
    assert len( p.query( artist="testa",track="local",qid="1511151651" )["results"]) == 1
    assert len( p.query( artist="testa",track="web",qid="151115165" )["results"]) == 1
    print "resolver ok"
