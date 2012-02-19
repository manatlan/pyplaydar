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


import os,sys,re
import PyV8
import urllib, urllib2,hashlib
import json

import httplib
from urllib2 import urlparse

from xml.dom.minidom import parseString,Document
TOMAHAWKJS="tomahawk.js"

class DOMParser(PyV8.JSClass):
    @staticmethod
    def parseFromString(txt,_):
        return parseString(txt)

class XMLHttpRequest(PyV8.JSClass):
    def __init__(self):
        self.isSend=False
        self.cb=None

    def open(self,method,url,mode):
        _,self.host,self.path,self.query,_=urlparse.urlsplit(url)
        self.method=method.strip().upper()
        self.mode=mode

    def send(self,data=None):
        self.data=data
        self.isSend=True
        self._go()

    def get_onreadystatechange(self): pass
    def set_onreadystatechange(self,cb):
        self.cb=cb
        self._go()
    onreadystatechange=property(get_onreadystatechange,set_onreadystatechange)

    def _go(self):
        """ called only when send and onreadystatechange are setted (coz vkontakte plugin)"""
        if self.isSend and self.cb:
            #~ print self.method,self.host,self.path,self.query,self.mode,self.data

            self.cnx=httplib.HTTPConnection(self.host)
            self.cnx.request(self.method,self.path + ("?"+self.query if self.query else ""),self.data)
            res = self.cnx.getresponse()

            self.readyState=4
            self.status = res.status
            self.responseText = res.read(1000000).strip()
            self.cb(self)

    def setRequestHeader(self,key,val):
        pass

class Global(PyV8.JSClass):

    def pyLog(self):
        def jo(m):
            #~ print "LOG:",m
            pass
        return jo

    def pyaddTrackResults(self):
        def _(m):
            get=lambda d,v: d[v] if v in d else ""  #coz {}.get() doesn't work
            for i in m.results:
                result={
                    "artist":get(i,"artist"),
                    "track":get(i,"track"),
                    "album":get(i,"album"),
                    "url":get(i,"url"),
                    "source":get(i,"source"),
                    "score":get(i,"score"),
                    "duration":get(i,"duration"),
                    "bitrate":get(i,"bitrate"),
                    "mimetype":get(i,"mimetype"),
                }
                self.results.append(result)
        return _

    def pymd5(self):
        def _(x):
            return hashlib.md5(x).hexdigest()
        return _

    def pyGetXMLHttpRequest(self):
        return XMLHttpRequest

    def pyDOMParser(self):
        return DOMParser

    def pyExpose(self):
        def _(x):
            d=dict(x)
            d.update({"_msgtype":"settings"})
            self.settings=d
        return _

class TomRes(object):
    def __init__(self,js):
        assert os.path.isfile(js),"Tomahawk resolver NOT FOUND (%s)"%js

        self._g=Global()
        self._g.results=[]
        ctxt = PyV8.JSContext(self._g)
        ctxt.enter()

        # load tomahawk js (providing helpers)
        ctxt.eval("""
            window={};console={};%s
            XMLHttpRequest=pyGetXMLHttpRequest();
            DOMParser=pyDOMParser();
            Tomahawk.md5=pymd5();
            Tomahawk.log=pyLog();
            console.log=pyLog();
            Tomahawk.addTrackResults=pyaddTrackResults();
            expose=pyExpose();
        """ % file(TOMAHAWKJS).read())

        ctxt.eval( file(js).read() )
        self._ctxt = ctxt

    @property
    def settings(self):
        self._ctxt.eval("""expose(Tomahawk.resolver.instance.settings)""")
        return self._g.settings

    def search(self,qid,artist,album,track):
        r=lambda x: x.replace("'","\'").replace('"','\"')
        artist=r(artist)
        album=r(album)
        track=r(track)
        self._ctxt.eval("""Tomahawk.resolver.instance.resolve("%s","%s","%s","%s")""" % (str(qid),artist,album,track))
        return self._g.results

if __name__ == "__main__":
    #~ plugin=TomRes("tomahawk-resolvers/lastfm/lastfm.js")
    #~ print plugin.settings
    #~ print plugin.search(1,"WU LYF","","dirt")

    #~ plugin=TomRes("tomahawk-resolvers/vkontakte/vkontakte-resolver.js")
    #~ print plugin.settings
    #~ print plugin.search(1,"deus","","for roses")

    #~ plugin=TomRes("tomahawk-resolvers/dilandau/dilandau.js")
    #~ print plugin.settings
    #~ print plugin.search(1,"beirut","","nantes")



    #~ plugin=TomRes("tomahawk-resolvers/youtube/youtube.js")
    #~ print plugin.settings
    #~ print plugin.search(1,"beirut","","nantes")


    #~ plugin=TomRes("tomahawk-resolvers/4shared/4shared-resolver.js")
    #~ print plugin.settings
    #~ print plugin.search(1,"beirut","","nantes")

    plugin=TomRes("tomahawk-resolvers/official.fm/officialfm-resolver.js")
    print plugin.settings
    print plugin.search(1,"beirut","","nantes")




