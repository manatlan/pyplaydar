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
import urllib,json

HOST = "localhost:60210"

def testm(method,args):
    if "auth" not in args: args["auth"]="test" #!!!!!!!!!!!!!!!!!!!!!!!!!!
    ua="&".join(["%s=%s"%(k,urllib.quote_plus(v)) for k,v in args.items()])
    if ua: ua="?"+ua
    h=testu(method+ua)
    try:
        return json.loads(h)
    except:
        print "**warning** doesn't return a json object !"
        return h


def testu(path):
    return testr(path).read()

def testr(path):
    print "CALL:","http://%s%s"%(HOST,path)
    return urllib.urlopen("http://%s%s"%(HOST,path))


# tests UT in py files
#===========================================================================
import os
old=os.getcwd()
os.chdir("resolvers")
execfile("__init__.py")
os.chdir(old)
execfile("resolver.py")


# test auth mechanism (not really unittest here)
#===========================================================================
import urllib
u=urllib.quote("http://%s/sfdhqsfhd"%HOST) # fake local 404 url
r=testr("/auth_1/?receiverurl=%s"%u)
assert r.code in (400,404)

assert testu("/authcodes?revoke=test")==""
assert testu("/authcodes")==""



# test bad auth token with all api
#===========================================================================
# method stat reply, with authenticated=false
assert not testm("/api/",{"method":"stat","auth":""})["authenticated"]
assert not testm("/api/",{"method":"stat","auth":"bad"})["authenticated"]

# method resolve reply nothing if bad auth
assert testm("/api/",{"method":"resolve","artist":"cake","track":"jolene","auth":"bad"})==""

# method get_results reply nothing if bad auth
assert testm("/api/",{"method":"get_results","qid":"XXX","auth":"bad"})==""



# test stat
#===========================================================================
d=testm("/api/",{"method":"stat"})
assert d["name"]=="playdar"
assert d["authenticated"]
assert type(d["capabilities"])==list
d=testm("/api/",{"method":"stat","jsonp":"myJsonpCallback"})    # test jsonp
assert d.startswith("myJsonpCallback(")

# test resolve
#===========================================================================
d=testm("/api/",{"method":"resolve","artist":"cake","track":"jolene"})
assert d["qid"]
qid=d["qid"]

# test providing its own qid
d=testm("/api/",{"method":"resolve","artist":"cake","track":"jolene","qid":"myownqid"})
assert d["qid"]=="myownqid"


# test get_results
#===========================================================================
assert testm("/api/",{"method":"get_results","qid":"unknown qid"})=="" # unknown qid
assert testm("/api/",{"method":"get_results","qid":"myownqid"})        # test preceding own qid
assert testm("/api/",{"method":"get_results","qid":qid})


# test sid (specifik to pyplaydar(test resolver)
#===========================================================================
d=testm("/api/",{"method":"resolve","artist":"XXXXX","track":"XXXXXX"})
qid=d["qid"]
r=testm("/api/",{"method":"get_results","qid":qid})
assert not r["results"]     # return nothing

# test a local sid
#~ d=testm("/api/",{"method":"resolve","artist":"testa","track":"local"})
#~ qid=d["qid"]
#~ r=testm("/api/",{"method":"get_results","qid":qid})
#~ assert len(r["results"])==1
#~ assert testu("/sid/"+r["results"][0]["sid"])[:10]

#~ # test a web sid
#~ d=testm("/api/",{"method":"resolve","artist":"testa","track":"web"})
#~ qid=d["qid"]
#~ r=testm("/api/",{"method":"get_results","qid":qid})
#~ assert len(r["results"])==1
#~ assert testu("/sid/"+r["results"][0]["sid"])[:10]


