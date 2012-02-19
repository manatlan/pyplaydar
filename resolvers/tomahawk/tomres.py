#!/usr/bin/python
# -*- coding: utf-8 -*-
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
import urllib,shutil,zipfile
import stat

def walktree (top = ".", depthfirst = True):
    names = os.listdir(top)
    if not depthfirst:
        yield top, names
    for name in names:
        try:
            st = os.lstat(os.path.join(top, name))
        except os.error:
            continue
        if stat.S_ISDIR(st.st_mode):
            for (newtop, children) in walktree (os.path.join(top, name), depthfirst):
                yield newtop, children
    if depthfirst:
        yield top, names

TOMAHAWKJS="tomahawk.js"
FOLDER="tomahawk-resolvers"
ZIP="tomahawk-resolvers.zip"
USAGE="""USAGE: %s <command>
Utility to manage tomahawk resolvers for pyplaydar
(c)2012 manatlan (Licence GPL2)

command:
    - install   : install the tomahawk resolvers
    - uninstall : uninstall the tomahawk resolvers
    - list      : list tomahawk js resolvers which are compatible
""" % os.path.basename(sys.argv[0])

if __name__ == "__main__":
    #~ sys.argv=["","list"]

    #ensure that the script is running in its folder
    try:
        os.chdir(os.path.split(sys.argv[0])[0])
    except:
        pass


    if len(sys.argv)!=2:
        print USAGE
    else:
        cmd = sys.argv[1].strip().lower()
        if cmd=="install":
            if os.path.isfile(TOMAHAWKJS): os.unlink(TOMAHAWKJS)
            print "Install",TOMAHAWKJS
            urllib.urlretrieve("https://raw.github.com/tomahawk-player/tomahawk/master/data/js/tomahawk.js",TOMAHAWKJS)

            print "Install",FOLDER
            shutil.rmtree(FOLDER,True)
            if os.path.isfile(ZIP): os.unlink(ZIP)
            urllib.urlretrieve("https://github.com/tomahawk-player/tomahawk-resolvers/zipball/master",ZIP)
            z = zipfile.ZipFile(ZIP)
            folder=z.namelist()[0]
            z.extractall(".")
            z.close()
            os.unlink(ZIP)
            shutil.move(folder,FOLDER)
        elif cmd=="uninstall":
            print "Uninstall",TOMAHAWKJS
            if os.path.isfile(TOMAHAWKJS): os.unlink(TOMAHAWKJS)
            print "Uninstall",FOLDER
            shutil.rmtree(FOLDER,True)
        elif cmd=="list":
            if not os.path.isdir(FOLDER):
                print "Error: Please Install first, tomahawk's resolvers are not here"
                sys.exit(-1)
            else:
                for (basepath, children) in walktree(FOLDER,True):
                    for child in children:
                        path=os.path.join(basepath, child)
                        if path.lower().endswith(".js"):
                            if "Tomahawk.resolver.instance" in file(path).read():
                                print path
