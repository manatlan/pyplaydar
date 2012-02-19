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
""" TESTS ALL THINGS """
import urllib,urllib2,re,json,sys,time,threading
from pyplaydar import web,resolver
from StringIO import StringIO
import urlparse


APP=web.default_app()
resolver.RESOLVERS = [['resolvers/test/resolver.py']]   # OVERWRITE RESOLVERS (to use test only)

#~ sys.exit()
def call(url,data=None,headers=None):
    """
        call url with POST method if data is not none, else GET method, with dict of headers
        WSGI-CALL

        return tuple :
            - http status code (int)
            - dict of response headers
            - body
    """
    if headers is None: headers={}

    e={"wsgi.errors":StringIO(),}

    su=urlparse.urlsplit(url)
    e["PATH_INFO"]=su.path
    e["QUERY_STRING"] = su.query
    e["HTTP_HOST"] = su.netloc
    for k,v in headers.items():
        e["HTTP_"+k]=v;

    if data:
        post = urllib.urlencode(data)
        e['wsgi.input']=StringIO()
        e['REQUEST_METHOD'] = 'POST'
        e['CONTENT_LENGTH'] = str(len(post))
        e['wsgi.input'].write(post)
        e['wsgi.input'].seek(0)
    else:
        e['REQUEST_METHOD'] = 'GET'

    t={}
    def h(*s):
        assert len(s)==2
        t["s"],t["h"]=s[0],s[1]
    time.sleep(0.05)                            #slow down the process
    body="".join( APP(e,h) )  # wsgi call
    e['wsgi.errors'].seek(0)
    assert not e['wsgi.errors'].read(10000)
    h=dict( [(a.lower(),b) for a,b in t["h"]])
    return int(re.match("^\d+",t["s"]).group(0)),h,body

def mcall(path,data=None,headers=None):
    return call("http://localhost:60210"+path,data,headers)



def test_server():
    assert mcall("/unknown_path")[0]==404
    assert "Not found" in mcall("/unknown_path")[2]

    r=mcall("/")
    assert r[0]==200
    assert "PyPlaydar Server is running" in r[2]
    assert "UTF-8" in r[1]["content-type"]

    assert mcall("/api/")[0]==400
    assert mcall("/api/?method=kokokkokoko")[0]==400

    assert mcall("/sid/")[0]==404
    assert mcall("/sid/gfdsgfdsgfds")[0]==404

def test_auth():
    r=mcall("/auth_1/?receiverurl="+urllib.quote("http://X/P"))
    assert r[0]==302
    assert r[1]["location"] == "http://X/P#myauth"

    assert mcall("/authcodes?revoke=myauth")[0]==200
    assert mcall("/authcodes?revoke=myauth")[0]==200

def test_api_stat():

    r=mcall("/api/?method=stat")
    assert r[0]==200
    assert r[1]['content-type']=='application/json'
    d=json.loads(r[2])
    assert d=={u'version': u'0.1.1', u'authenticated': False, u'name': u'playdar', u'capabilities': []}
    assert not d['authenticated']

    r=mcall("/api/?method=stat&auth=test")
    assert r[0]==200
    assert r[1]['content-type']=='application/json'
    d=json.loads(r[2])
    assert d=={u'version': u'0.1.1', u'authenticated': True, u'name': u'playdar', u'capabilities': []}
    assert d['authenticated']

    #test jsonp
    r=mcall("/api/?method=stat&auth=test&jsonp=kiki")
    assert r[0]==200
    assert r[1]['content-type'] != 'application/json'
    assert r[2]=="""kiki({"version": "0.1.1", "authenticated": true, "name": "playdar", "capabilities": []})"""

def test_api_resolve():
    nimp="XHXJSHUXS17281728749JJJ"

    assert mcall("/api/?method=resolve")[0]==400
    assert mcall("/api/?method=resolve&auth=test")[0]==400
    assert mcall("/api/?method=resolve&auth=test&artist=toto")[0]==400

    # classical search
    r=mcall("/api/?method=resolve&auth=test&artist=%(nimp)s&track=%(nimp)s"%locals())
    assert r[0]==200
    assert r[1]['content-type']=='application/json'
    d=json.loads(r[2])
    assert d.keys()==["qid"]

    # provide its own qid
    r=mcall("/api/?method=resolve&auth=test&artist=%(nimp)s&track=%(nimp)s&qid=123456789"%locals())
    assert r[0]==200
    assert r[1]['content-type']=='application/json'
    d=json.loads(r[2])
    assert d["qid"]=="123456789"

def test_api_results():
    assert mcall("/api/?method=get_results")[0]==400
    assert mcall("/api/?method=get_results&auth=test")[0]==400
    assert mcall("/api/?method=get_results&auth=test&qid=789789778978")[0]==400 #unknown qid

    def test(A,T):
        r=mcall("/api/?method=resolve&auth=test&artist=%s&track=%s" % (A,T))
        d=json.loads(r[2])
        qid=d["qid"]
        r=mcall("/api/?method=get_results&auth=test&qid=%s"%qid)
        assert r[0]==200
        assert r[1]['content-type']=='application/json'
        d=json.loads(r[2])
        assert d["qid"]==qid
        assert d["query"]["artist"]==A
        assert d["query"]["track"]==T
        assert d["query"]["qid"]==qid
        assert d["query"]["solved"]==False
        assert d["results"]==[]

        time.sleep(1.5) # wait for results

        r=mcall("/api/?method=get_results&auth=test&qid=%s"%qid)
        assert r[0]==200
        assert r[1]['content-type']=='application/json'
        d=json.loads(r[2])
        assert d["qid"]==qid
        assert d["query"]["artist"]==A
        assert d["query"]["track"]==T
        assert d["query"]["qid"]==qid
        assert d["query"]["solved"]==True
        assert len(d["results"])==1
        r=d["results"][0]
        assert r["artist"]==A
        assert r["track"]==T
        assert r["sid"]
        assert r["source"]
        return r["sid"]

    sid=test("testa","web")
    r=mcall("/sid/"+sid)
    assert r[0]==302
    assert "location" in r[1]

    sid=test("testa","local")
    r=mcall("/sid/"+sid)
    assert r[0]==200
    assert r[1]['content-type']=='audio/mp3'
    assert r[2]


def test_my_resolvers():    #TODO: can do better here !
    import resolvers

    import os
    prec=os.getcwd()
    try:
        os.chdir("resolvers")
        resolvers.test_this()

    finally:
        os.chdir(prec)

if __name__=="__main__":
    test_my_resolvers()
    resolver.test_this()

    # web tests
    test_server()
    test_auth()
    test_api_stat()
    test_api_resolve()
    test_api_results()

    for thread in threading.enumerate():
        if thread is not threading.currentThread():
            thread.join()


