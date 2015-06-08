#!/usr/bin/env python
# -*- coding: utf-8 -*-


from twisted.internet import reactor,threads,task,defer
import base64
import json
import time
import wikipedia
import dateutil.parser as dparser
import dateutil
import subprocess

from itertools import chain
import re
from pprint import pprint 
from collections import Counter

# Add more strings that confuse the parser in the list
UNINTERESTING = set(chain(dateutil.parser.parserinfo.JUMP, 
                              dateutil.parser.parserinfo.PERTAIN,
                                                        ['a']))

def callparse(text):
    try:
        return dparser.parse(text,fuzzy=True)
    except Exception as e:
        pass
def _get_date(tokens):
    for end in xrange(len(tokens), 0, -1):
        region = tokens[:end]
        if all(token.isspace() or token in UNINTERESTING
               for token in region):
            continue
        text = ''.join(region)
        try:
            date = dateutil.parser.parse(text,fuzzy=True)
            return end, date
        except ValueError:
            pass
        except TypeError:
            pass

def find_dates(text, max_tokens=50, allow_overlapping=False):
    tokens = filter(None, re.split(r'(\S+|\W+)', text))
    skip_dates_ending_before = 0
    for start in xrange(len(tokens)):
        region = tokens[start:start + max_tokens]
        result = _get_date(region)
        if result is not None:
            end, date = result
            if allow_overlapping or end > skip_dates_ending_before:
                skip_dates_ending_before = end
                yield date

def outputDic():
    datastr = """
    [
    {id: 1, content: 'item 1', start: '2014-04-20'},
    {id: 2, content: 'item 2', start: '2014-04-14'},
    {id: 3, content: 'item 3', start: '2014-04-18'},
    {id: 4, content: 'item 4', start: '2014-04-16', end: '2014-04-19'},
    {id: 5, content: 'item 5', start: '2014-04-25'},
    ]


    """

    with open("basic_temp.html","r") as template:
        with open("basicUsage.html","w") as output:
            for line in template:
                if "{{!!!!!!}}" in  line:
                    output.write(datastr)
                else:
                    output.write(line)

def searchRelatedPages(searchStr):
    """
    return counter on related Pages
    """
    res ,suggest = wikipedia.search(searchStr,results=10,suggestion=True)
    
    allPagesToCheck = list(res)
    # find many pages to find :
    for pageToCheck in res:
        try:
            page = wikipedia.page(pageToCheck,redirect=True)
            #print page.categories
            allPagesToCheck += page.links
        except:
            pass

    rankedpages = Counter(allPagesToCheck)

    print "end finding  %s pages" % ( len(rankedpages),)
    return defer.succeed(rankedpages)


def extractDatesFromPage( rankedpages):
    """

    """
    def __extractor(pageToCheck):
        print "running on ",pageToCheck
        extractor_start = time.time()
        extractedDates = []
        try:
            encodedTitle = base64.b64encode(pageToCheck)
            res = subprocess.check_output(
                ["python","matcher.py",encodedTitle],
                )
            allDates = json.loads(res)
            for d in allDates:
                print "date : %s, %s"%(d,pageToCheck)
                extractedDates.append((d,pageToCheck))

        except Exception as e:
            print "wrong run :'( ",e
            return []

        print "runned on %s. getPage %.2f " % (pageToCheck,time.time()-extractor_start)
        return extractedDates

    def __reduce(listResult):
        allDates=[]
        for success,data in listResult:
            allDates+=data

        print "end reduce %s"% ( len(allDates))

        return allDates


    dlist = []
    for pageToCheck,pageCount in rankedpages.most_common()[:30]:
        d = threads.deferToThread(__extractor,pageToCheck)
        dlist.append(d)

    dl = defer.DeferredList(dlist)
    dl.addCallback(__reduce)
    print "runned %s task :)" % (len(dlist),)

    return dl

def searchDates(searchStr):
    d = searchRelatedPages(searchStr)
    d.addCallback(extractDatesFromPage)
    d.addCallback(ending)
    return d

def ending(allDates):
    print "received %s dates" % (len(allDates),)


if __name__=="__main__":
    #searchDates("Hilbert")

    reactor.callLater(0,searchDates,"Hilbert")
    reactor.run()


    #res = subprocess.check_output(
    #        ["python","matcher.py","Z29kZWw="],
    #    )

    #print res











