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

import shelve,uuid
import os,imp
from glob import glob
import logging
logging.basicConfig(format='>%(asctime)s (%(levelname)s) %(message)s',level=logging.INFO,datefmt="%m/%d/%y %H:%M:%S")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log= lambda x: logger.info("RESOLVER: "+x)
logerr= lambda x: logger.error("RESOLVER: "+x)

#==============================================================================
# INITIALIZE (import resolvers, shelve, ...)
#==============================================================================
for r in [i for i in glob("resolvers/*.py") if not os.path.basename(i).startswith("_")]:
    r=r.replace("\\",".").replace("/",".")[:-3]
    log("import "+r)
    exec "from %s import *"%r   # not great ;-)
RESOLVER=Resolver
QUERY=shelve.open("query.shelve")
RESPONSE=shelve.open("response.shelve")
SID=shelve.open("sid.shelve")

#==============================================================================
# Instanciate resolvers
#==============================================================================
RESOLVER.list.sort(lambda a,b:-cmp(a.priority,b.priority))
RESOLVER.instances=[inst() for inst in RESOLVER.list]




def initSearch(qid,artist,album,track):
    """ return True if search has been initiated """
    qid=str(qid)
    msg="initSearch(%s,...) : "%qid
    if qid in QUERY.keys():
        log(msg+"this qid is already process(ed|ing), do nothing!")
    else:
        QUERY[qid]=(artist,album,track)    # save the query

        # here is synchronous,
        if RESOLVER.instances:
            for idx,resolver in enumerate(RESOLVER.instances):
                info="%d/%d"%(idx+1,len(RESOLVER.instances))
                data = resolver.resolve(qid,artist,album,track)
                RESPONSE[qid]= data
                if [True for obj in data["results"] if int(obj["score"])>=1]:
                    # break toolchain if a resolver has found 1 exact match
                    log(msg+"%s %s found %d result(s), and an exact ! stop searching" % (info,resolver.__class__.__name__,len(data["results"])))
                    break
                else:
                    log(msg+"%s %s  found %d result(s), but not exact" % (info,resolver.__class__.__name__,len(data["results"])))
        else:
            logerr(msg+"No resolvers?!")

    return True


def fetchSearch(qid):
    qid=str(qid)

    msg="fetchSearch(%s) -> "%qid
    if qid in QUERY.keys():
        artist,album,track = QUERY[qid]

        liste=[]
        for obj in RESPONSE.get(qid,{"results":[]})["results"]:

            # create the SID element to reference to be able to retrieve obj
            sid=str(uuid.uuid5(uuid.NAMESPACE_DNS,obj["url"].encode("utf_8")))
            SID[sid]=obj

            result= {
                "sid":sid,  # declare the sid ^^
                "artist": obj.get("artist",""),
                "album": obj.get("album",""),
                "track": obj.get("track",""),
                "source": obj.get("source",""),
                "size": obj.get("size",""),
                "mimetype": obj.get("mimetype",""),
                "bitrate": obj.get("bitrate",""),
                "duration": obj.get("duration",""),
                "score": int(obj.get("score","0")),
            }
            liste.append(result)

        liste.sort(lambda a,b: cmp(int(a["score"]),int(b["score"])) )

        query={
            "qid":qid,
            "artist" : artist,
            "album" : album,
            "track" : track,
            "mode" : "normal",
            "solved" : True if [True for obj in liste if int(obj["score"])>=1] else False,
        }
        log(msg+"return %d result(s) and solved=%s"%(len(liste),query["solved"]))
        return query,liste
    else:
        logerr(msg+"can't find qid (not initialized)")

def song(sid):
    sid=str(sid)
    msg="song(%s) -> "%sid
    if sid in SID.keys():
        r=SID[sid]

        url = r.get("url","")
        if url.lower().startswith("http://"):
            log(msg+"return the url(%s)"%url)
            obj=url
        else:
            if os.path.isfile(url):
                log(msg+"return a local file(%s)"%url)
                obj = open(url,"rb")    # a file-like for local file
            else:
                log(msg+"return nothing coz local file(%s) not found"%url)
                obj=None
        if obj:
            return r.get("mimetype",""),r.get("size",""),obj
    else:
        logerr(msg+"return nothing coz sid is not defined (not fetched)")
#-----------------------------------------------------
if __name__=="__main__":
    assert initSearch(u"XXX1","testa","","XXXX")    # test a not found query
    qr,ll=fetchSearch(u"XXX1")
    assert not qr["solved"]
    assert len(ll)==0

    assert initSearch(u"XXX","testa","","local")    # test a local file
    qr,ll=fetchSearch(u"XXX")
    assert qr["solved"]
    assert type(song(ll[0]["sid"])[2]) == file

    assert initSearch(u"XXX2","testa","","web")     # test a web file
    qr,ll=fetchSearch(u"XXX2")
    assert qr["solved"]
    assert isinstance(song(ll[0]["sid"])[2],basestring)
