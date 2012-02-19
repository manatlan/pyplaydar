#!/usr/bin/python
# -*- coding: utf-8 -*-
# Modified by <manatlan@gmail.com> 2012, to make this plugin
# Created by Paul Lamere<Paul.Lamere@gmail.com> twitter.com/plamere
# Based on the seeqpod resolver by:
# Max Howell <max@methylblue.com> twitter.com/mxcl
# Licensed the same as Playdar

########################################################################
import sys,traceback
from httplib import HTTP
import json
from urlparse import urlparse
import urllib, urllib2
import socket
from xml.dom import minidom
from struct import unpack, pack

def ERROR(m):
    print >> sys.stderr, "ERROR:", m
    sys.exit(-1)

try:
    import PyV8
except ImportError:
    ERROR("You'll need to install PyV8 (http://code.google.com/p/pyv8/) to be able to use this resolver !")

from lib import TomRes
###################################################################### functions
def print_json(o):
    s = json.dumps(o)
    sys.stdout.write(pack('!L', len(s)))
    sys.stdout.write(s)
    sys.stdout.flush()

import os,sys
#ensure that the script is running in its folder
try:
    os.chdir(os.path.split(sys.argv[0])[0])
except:
    pass


if not len(sys.argv)>1:
    ERROR("Tomahawk resolver should be called with an argument (relative path to js file)")

t=TomRes(sys.argv[1])

####################################################################### settings
print_json( t.settings )
###################################################################### main loop
while 1:
    length = sys.stdin.read(4)

    if not length:
        break;

    length = unpack('!L', length)[0]
    if not length:
        break
    # something probably went wrong, most likely we're out of sync and are
    # reading the 4 bytes length header in the middle of a json string. We can't
    # recover. Bail.
    if length > 4096 or length < 0:
        break
    if length > 0:
        msg = sys.stdin.read(length)
        try:
            request = json.loads(msg)
            # print request
            tracks = t.search(request['qid'],request['artist'],request.get('album',""), request['track'])
            response = { 'qid':request['qid'], 'results':tracks, '_msgtype':'results' }
            print_json(response)
        except:
            traceback.print_exc(file=sys.stderr)
            # safe to continue, skipping this msg, because at least
            # we consumed enough input so next iteration hits size header.
            pass

