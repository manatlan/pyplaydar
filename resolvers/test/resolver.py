#!/usr/bin/python
# -*- coding: utf-8 -*-
# Modified by <manatlan@gmail.com> 2011, to make a test plugin
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

###################################################################### functions
def print_json(o):
    s = json.dumps(o)
    sys.stdout.write(pack('!L', len(s)))
    sys.stdout.write(s)
    sys.stdout.flush()

def resolve(artist, track):
    import time
    time.sleep(1)

    ll=[]

    if artist=="testa" and track=="web":
        ll.append( {
            "artist": artist,
            "track": track,
            "duration": 0,
            "source": __file__,
            "extension": "mp3",
            "mimetype": "audio/mp3",
            "url": "http://manella.free.fr/mp3/manella_-_zmorlockfunk.mp3",
            "score":1,
            }
        )

    if artist=="testa" and track=="local":
        ll.append( {
            "artist": artist,
            "track": track,
            "duration": 0,
            "source": __file__,
            "extension": "mp3",
            "mimetype": "audio/mp3",
            "url": "libs/bottle.py",
            "score":1,
            }
        )

    return ll

####################################################################### settings
settings = dict()
settings["_msgtype"] = "settings"
settings["name"] = "Test Resolver"
settings["targettime"] = 2000 # millseconds
settings["weight"] = 50     # not speediest
print_json( settings )

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
            tracks = resolve(request['artist'], request['track'])
            response = { 'qid':request['qid'], 'results':tracks, '_msgtype':'results' }
            print_json(response)
        except:
            traceback.print_exc(file=sys.stderr)
            # safe to continue, skipping this msg, because at least
            # we consumed enough input so next iteration hits size header.
            pass

