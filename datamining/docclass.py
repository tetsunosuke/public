# -*- coding: utf-8 -*-

import re
import math
import sqlite3 as sqlite

import MeCab

def getwords(doc):
    splitter = re.compile("\\W*")
    words = [s.lower() for s in splitter.split(doc)
             if len(s) > 2 and len(s) < 20]

    return dict([(w, 1) for w in words])


def getjawords(doc):
    words = []
    tagger = MeCab.Tagger("-Ochasen")
    m = tagger.parseToNode(doc)
    while m:
        if m.feature.startswith("名詞"):
            words.append(m.surface)
        m = m.next

    return dict([(w, 1) for w in words])
    

#print getwords("This is a pen, this is a bread bread")
#print getjawords("これはペンですこれはパンです")


class classfier:
    def __init__(self, getfeatures, filename=None):
        self.fc = {}
        self.cc = {}
        self.getfeatures = getfeatures

    def setdb(self, dbfile):
        self.con = sqlite.connect(dbfile)
        self.con.text_factory = str
        self.con.execute("create table if not exists fc(feature, category, count)")
        self.con.execute("create table if not exists cc(category, count)")


    def incf(self, f, cat):
        count = self.fcount(f, cat)

        # 0なら1を入れて、それ以外なら1カウントアップ
        if count == 0:
            self.con.execute("insert into fc values(?, ?, 1)", (f, cat))
        else:
            self.con.execute("update fc set count=? where feature = ? and category = ?", (count+1, f, cat))
            
    def fcount(self, f, cat):
        res = self.con.execute("select count from fc where feature = ? and category = ?", (f, cat)).fetchone()
        if res == None:
            return 0.0
        else:
            return float(res[0])

    def incc(self, cat):
        count = self.catcount(cat)
        # 0なら1を入れて、それ以外なら1カウントアップ
        if count == 0:
            self.con.execute("insert into cc values(?, 1)", (cat,))
        else:
            self.con.execute("update cc set count=? where category = ?", (count+1, cat))

    def catcount(self, cat):
        res = self.con.execute("select count from cc where category = ?", (cat,)).fetchone()
        if res == None:
            return 0.0
        else:
            return float(res[0])

    def totalcount(self):
        res = self.con.execute("select sum(count) from cc").fetchone()
        if res == None:
            return 0
        return res[0]

    def categories(self):
        cur = self.con.execute("select category from cc")
        return [d[0] for d in cur]


    def train(self, item, cat):
        features = self.getfeatures(item)
    
        for f in features:
            self.incf(f, cat)
        self.incc(cat)
        self.con.commit()

    def fprob(self, f, cat):
        if self.catcount(cat) == 0:
            return 0
        return self.fcount(f, cat) / self.catcount(cat)

    def weightedprob(self, f, cat, prf, weight = 1, ap = 0.5):
        basicprob = prf(f, cat)
        totals = sum([self.fcount(f, c) for c in self.categories()])

        bp = ((weight*ap) + (totals*basicprob)) / (weight + totals)
        return bp

class naivebayes(classfier):
    def __init__(self, getfeatures):
        classfier.__init__(self,getfeatures)
        self.thresholds = {}

    def docprob(self, item, cat):
        features = self.getfeatures(item)

        p = 1
        for f in features:
            p *= self.weightedprob(f, cat, self.fprob)
        return p

    def prob(self, item, cat):
        catprob = self.catcount(cat) / self.totalcount()
        docprob = self.docprob(item, cat)
        return docprob * catprob

    def setthreshold(self, cat, t):
        self.thresholds[cat] = t

    def getthreshold(self, cat):
        if cat not in self.thresholds:
            return 1.0
        return self.thresholds[cat]

    def classify(self, item, default=None):
        probs = {}
        max = 0.0
        for cat in self.categories():
            probs[cat] = self.prob(item, cat)
            if probs[cat] > max:
                max = probs[cat]
                best = cat

        for cat in probs:
            if cat == best:
                continue

            if probs[cat] * self.getthreshold(best) > probs[best]:
                return default

        return best


class fisherclassifier(classfier):
    def __init__(self, getfeatures):
        classfier.__init__(self, getfeatures)
        self.minimums = {}

    def setminimum(self, cat, min):
        self.minimums[cat] = min
    def getminimum(self, cat):
        if cat not in self.minimums:
            return 0
        return self.minimums[cat]

    def cprob(self, f, cat):
        clf = self.fprob(f, cat)
        if clf == 0:
            return 0
        freqsum = sum([self.fprob(f, c) for c in self.categories()])
        p = clf /(freqsum)
        return p

    def fisherprob(self, item, cat):
        p = 1
        features = self.getfeatures(item)
        for f in features:
            p *= (self.weightedprob(f, cat, self.cprob))
        fscore = -2 * math.log(p)
        return self.invchi2(fscore, len(features) * 2)

    def invchi2(self, chi, df):
        m = chi / 2.0
        sum = term = math.exp(-m)
        for i in range(1, df//2):
            term *= m / i
            sum += term
        return min(sum, 1.0)

    def classify(self, item, default = None):
        best = default
        max = 0.0
        for c in self.categories():
            p = self.fisherprob(item, c)
            if p > self.getminimum(c) and p > max:
                best = c
                max = p
        return best

        

    




def main():
    import docclass 
    cl = docclass.classfier(docclass.getwords)
    cl.train("the quick brown fox jumps over the lazy dog", "good")
    cl.train("the brown fox jumps over the lazy dog", "bad")

    print cl.fcount("quick", "bad")
    print cl.fcount("quick", "good")

    cl2 = docclass.classfier(docclass.getjawords)
    cl2.train("私は日本人です", "good")
    cl2.train("私はラーメンが好きです", "bad")
    
    print cl2.fcount("ラーメン", "bad")
    print cl2.fcount("ラーメン", "good")


    


if __name__ == '__main__':
    main()
