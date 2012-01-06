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
import uuid
import os,sys

from resolvers import Resolver

import logging
logging.basicConfig(format='>%(asctime)s (%(levelname)s) %(message)s',level=logging.INFO,datefmt="%m/%d/%y %H:%M:%S")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log= lambda x: logger.info("RESOLVER: "+x)
logerr= lambda x: logger.error("RESOLVER: "+x)




#==============================================================================
# INITIALIZE (import resolvers, shelve, ...)
#==============================================================================
RESOLVERS=[]
print "Resolvers:"
try:
    for r in [i.strip() for i in file("pyplaydar.conf") if i.strip()]:
        path = os.path.normcase(os.path.join("resolvers",r))
        if not os.path.isfile( path ):
            raise Excetion("Can't found the resolver : "+r)
        else:
            # try to instanciate it
            print "-",Resolver(path)

            RESOLVERS.append(path)
except Exception,e:
    print "problem with resolvers ?!",e
    sys.exit(-1)
#TODO: sort according settings[weight]


#~ QUERY=shelve.open("query.shelve")
#~ RESPONSE=shelve.open("response.shelve")
#~ SID=shelve.open("sid.shelve")

QUERY={}
RESPONSE={}
SID={}


###############################################################################
def initSearch(qid,artist,album,track):
###############################################################################
    """ return True if search has been initiated """
    qid=str(qid)
    msg="initSearch(%s,...) : "%qid
    if qid in QUERY.keys():
        log(msg+"this qid is already process(ed|ing), do nothing!")
    else:
        QUERY[qid]=[artist,album,track,False]    # save the query (isResolversEnded==False)

        # here is synchronous,
        for idx,path in enumerate(RESOLVERS):
            info="%d/%d"%(idx+1,len(RESOLVERS))
            resolver=Resolver(path)
            data=resolver.query(artist=artist,album=album,track=track,qid=qid )
            RESPONSE[qid]= data
            if [True for obj in data["results"] if int(obj["score"])>=1]:
                # break toolchain if a resolver has found 1 exact match
                log(msg+"%s %s found %d result(s), and an exact ! stop searching" % (info,resolver.__class__.__name__,len(data["results"])))
                break
            else:
                log(msg+"%s %s  found %d result(s), but not exact" % (info,resolver.__class__.__name__,len(data["results"])))

        QUERY[qid][3]=True  # mark as solved (isResolversEnded==True)

    return True



###############################################################################
def fetchSearch(qid):
###############################################################################
    qid=str(qid)

    msg="fetchSearch(%s) -> "%qid
    if qid in QUERY.keys():
        artist,album,track,isResolversEnded = QUERY[qid]

        liste=[]

        isAResult=False
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

            if result["score"]>=1: isAResult=True

        liste.sort(lambda a,b: cmp(int(a["score"]),int(b["score"])) )

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


if __name__ == "__main__":
    assert initSearch(u"qid1","testaa","","XXXX")    # test a not found query
    qr,ll=fetchSearch(u"qid1")
    assert qr["solved"]
    assert len(ll)==0

    assert initSearch(u"qid2","testa","","local")    # test a local file
    qr,ll=fetchSearch(u"qid2")
    assert qr["solved"]
    assert type(song(ll[0]["sid"])[2]) == file

    assert initSearch(u"qid3","testa","","web")     # test a web file
    qr,ll=fetchSearch(u"qid3")
    assert qr["solved"]
    assert isinstance(song(ll[0]["sid"])[2],basestring)

    print "methods ok"
