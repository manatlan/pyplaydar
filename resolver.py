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
import uuid
import os,sys

from resolvers import Resolver

import logging
logging.basicConfig(format='>%(asctime)s (%(levelname)s) %(message)s',level=logging.INFO,datefmt="%m/%d/%y %H:%M:%S")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log= lambda x: logger.info("RESOLVER: "+x)
logerr= lambda x: logger.error("RESOLVER: "+x)


import shlex

#==============================================================================
# INITIALIZE (import resolvers, shelve, ...)
#==============================================================================
RESOLVERS=[]
print "Resolvers:"
try:
    for cmds in [shlex.split(i.strip()) for i in file("pyplaydar.conf") if i.strip() and not i.strip().startswith("#")]:
        cmds[0] = os.path.normcase(os.path.join("resolvers",cmds[0]))
        if not os.path.isfile( cmds[0] ):
            raise Exception("Can't found the resolver command: "+cmds[0])
        else:
            # try to instanciate it
            print Resolver(cmds).settings

            RESOLVERS.append(cmds)
except Exception,e:
    print "problem with resolvers ?!",e
    sys.exit(-1)
#TODO: sort according settings[weight]


QUERY={}
RESPONSE={}
SID={}


###############################################################################
def initSearch(qid,artist,album,track):
###############################################################################
    """ Initiate the search thru available/configured resolvers """
    qid=str(qid)
    msg="initSearch(%s,...) : "%qid
    if qid in QUERY.keys():
        log(msg+"this qid is already process(ed|ing), do nothing!")
    else:
        QUERY[qid]=[artist,album,track,False]    # save the query (isResolversEnded==False)
        RESPONSE[qid]=[]

        # here is synchronous,
        for idx,path in enumerate(RESOLVERS):
            info="%d/%d"%(idx+1,len(RESOLVERS))
            resolver=Resolver(path)
            data=resolver.query(artist=artist,album=album,track=track,qid=qid )
            RESPONSE[qid]+=data["results"]
            if [True for obj in data["results"] if float(obj.get("score",0) or 0)>=1]:
                # break toolchain if a resolver has found 1 exact match
                log(msg+"%s %s found %d result(s), and an exact ! stop searching" % (info,resolver.__class__.__name__,len(data["results"])))
                break
            else:
                log(msg+"%s %s  found %d result(s), but not exact" % (info,resolver.__class__.__name__,len(data["results"])))

        QUERY[qid][3]=True  # mark as solved (isResolversEnded==True)



###############################################################################
def fetchSearch(qid):
###############################################################################
    """ fetch available result for a QID """

    qid=str(qid)

    msg="fetchSearch(%s) -> "%qid
    if qid in QUERY.keys():
        artist,album,track,isResolversEnded = QUERY[qid]

        liste=[]

        isAResult=False
        for obj in RESPONSE.get(qid,[]):

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
                "score": float(obj.get("score","0") or 0),
            }
            liste.append(result)

            if result["score"]>=1: isAResult=True

        liste.sort(lambda a,b: -cmp(float(a["score"]),float(b["score"])) )

        if isResolversEnded==False:
            # resolver is always searching
            # but perhaps there is already a result
            query_solved = isAResult
        else:
            # resolver has ended its search
            query_solved = True

        query={
            "qid":qid,
            "artist" : artist,
            "album" : album,
            "track" : track,
            "mode" : "normal",
            "solved" : query_solved,
        }
        log(msg+"return %d result(s) and solved=%s"%(len(liste),query_solved))
        return query,liste
    else:
        logerr(msg+"can't find qid (not initialized)")


###############################################################################
def song(sid):
###############################################################################
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

def test_this():
    initSearch(u"qid1","testaa","","XXXX")    # test a not found query
    qr,ll=fetchSearch(u"qid1")
    assert qr["solved"]
    assert len(ll)==0

    initSearch(u"qid2","testa","","local")    # test a local file
    qr,ll=fetchSearch(u"qid2")
    assert qr["solved"]
    assert type(song(ll[0]["sid"])[2]) == file

    initSearch(u"qid3","testa","","web")     # test a web file
    qr,ll=fetchSearch(u"qid3")
    assert qr["solved"]
    assert isinstance(song(ll[0]["sid"])[2],basestring)

    print "methods ok"

if __name__ == "__main__":
    test_this()
