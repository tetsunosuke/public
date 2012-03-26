# -*- coding: utf-8 -*-
import os
import glob
import docclass

dbfile = "default.db"
path = "training_data"
try:
    os.unlink(dbfile)
except:
    pass

cl = docclass.fisherclassifier(docclass.getjawords)
cl.setdb(dbfile)
dirpath, dirnames, filenames = os.walk(path)

categories = dirpath[1]
for c in categories:
    files = glob.glob("%s/%s/*.txt" % (path, c))
    for file in files:
        f = open(file, "r")
        s = "".join([st for st in f])
        cl.train(s, c)
