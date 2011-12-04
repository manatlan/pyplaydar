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
import libs.bottle as web # http://bottle.paws.de/page/docs
import resolver
import uuid,json
import logging
logging.basicConfig(format='>%(asctime)s (%(levelname)s) %(message)s',level=logging.INFO,datefmt="%m/%d/%y %H:%M:%S")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

"""
Lame http implementations of http://www.playdar.org/api.html
"""

TOKENS=[]

createToken=lambda: "myauth"
isAuthentOk=lambda auth: (auth in TOKENS) or auth=="test"
log= lambda x: logger.info("SERVER: "+x)
logerr= lambda x: logger.error("SERVER: "+x)

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ authent
@web.get('/auth_1/')
def auth1():
    receiverurl=web.request.query.receiverurl
    token=createToken()
    TOKENS.append(token)
    redirect=receiverurl+"#"+token
    log("ASK AUTH -> create token(%s) and redirect to %s"%(token,redirect))
    web.redirect(redirect)

@web.get('/authcodes')
def authcodes():
    revoke=web.request.query.revoke
    if revoke in TOKENS:
        log("ASK AUTHCODES -> remove token (%s) "%revoke)
        TOKENS.remove(revoke)
    else:
        log("ASK AUTHCODES -> for nothing ;-)")
#//////////////////////////////////////////////////////////////////////////////

@web.get('/api/')
def playdarApi():
    mkjson=lambda cb,d: cb and "%s(%s)"%(cb,json.dumps(d)) or d
    auth = web.request.query.auth
    authenticated=isAuthentOk(auth)

    method = web.request.query.method.lower()
    callback = web.request.query.jsonp

    msg="ASK API.%s (auth=%s,cb=%s), auth is %s -> " % (method,auth,callback,authenticated and "OK" or "KO")

    if method=="stat":
        log(msg+"return stat")
        return mkjson(callback,{"name":"playdar","version":"0.1.1","authenticated":authenticated,"capabilities": []})
    elif method=="resolve":
        if authenticated:
            artist=web.request.query.artist.strip()
            album=web.request.query.album.strip()
            track=web.request.query.track.strip()
            qid=web.request.query.qid or str(uuid.uuid5(uuid.NAMESPACE_DNS,(artist+album+track).encode("utf_8")))
            if resolver.initSearch(qid,artist,album,track):
                log(msg+"reply a qid(%s)"%qid)
                return mkjson(callback,{"qid":qid} )
            else:
                logerr(msg+"can't initiate relovers!")
        else:
            logerr(msg+"can't reply coz auth is KO")
    elif method=="get_results":
        if authenticated:
            qid=web.request.query.qid
            if qid:
                result=resolver.fetchSearch(qid)
                if result:
                    query,liste=result
                    log(msg+"return %d result(s) for qid(%s)" % (len(liste),qid))
                    return mkjson(callback,{
                        "qid":qid,
                        "refresh_interval":1000,
                        "query": query,
                        "results": liste,
                    })
                else:
                    logerr(msg+"can't reply coz qid is unknown")
            else:
                logerr(msg+"can't reply coz qid is missing")
        else:
            logerr(msg+"can't reply coz auth is KO")
    else:
        logerr(msg+"unknown method ?!?")

@web.get('/sid/<sid>')
def play(sid):
    contentType,size,obj = resolver.song(sid)
    if isinstance(obj,basestring):
        log("ASK SID."+sid+"-> redirect to URL(%s)"%obj)
        web.redirect(obj) #headers are (perhaps) set by its own server
    else:
        log("ASK SID."+sid+"-> will return to a file-like (%s) of size (%s)"%(contentType,str(size)))
        if contentType: web.response.content_type = contentType
        if size: web.response.content_length = str(size)
        return obj

if __name__=="__main__":
    web.run(host="0.0.0.0",port=60210,server="cherrypy")
