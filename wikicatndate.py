#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re
import time
import wikipedia
import dateutil.parser as dparser
import dateutil
import subprocess
from pprint import pprint 
from collections import Counter
from bs4 import BeautifulSoup as bs

import codecs

def dumpwiki(): 
    # dump pages of wikipedia for offline analysis
    for ck in range(1000,2015):
        try:
            res = wikipedia.page(str(ck))
            res.html()

            fileName = "dumphtml/%s.html"%ck
            with codecs.open(fileName,"w",encoding="utf-8") as out:
                txt = res.html()
                out.write(txt)

            print "dumped %s"%fileName
        except Exception as e:
            print "error: ",e


def process10(res):
    """

    for pages ~>1000 quite long time ago

    Events 
        maybe date - text
        text
        text 
    
    Or:

    Events
        By place
            Europe
                date/text
            .. 
        By topic
            ..

    """


def process18(res):
    """

    """


def fu(res):
    """

    """

    month=res.findNext("h3")

    monthList = []
    while month!=None and len(monthList)<12:
        monthName= month.findChildren("span")[0]
        if monthName.text in monthList:
            month=None
        else:
            # process Month
            #print monthName.text
            monthData = []

            dateSection = month.findNext("ul")
            for li in dateSection.find_all("li",recursive=False):

                dateText  = li.findNext("a").text

                children = li.findChildren("li")

                contentForDate = []
                if len(children) > 0:
                    for relatedli in children:
                        datedContent= relatedli.findNext("a").text
                        contentForDate.append(datedContent)
                else:
                    datedContent = li.findNext("a").findNext('a').text
                    contentForDate.append(datedContent)
                monthData.append((dateText,contentForDate))
            
            ##### keepthis !
            month = month.findNext("h3")
            monthList.append((monthName.text,monthData))

    #pprint(monthList)
    #for htmlThing in  res.findNext("ul").li:
    #    print htmlThing
    return monthList


def process19(searchStr):
    """
    
    Return dic with at least : 
    {
        events : [ ]
        births : []
        deaths : []
    }
    
    Simple process for pages ~> 1900
    
    page is like
    Events
        January
            date - event text (some links ) text .. 
            date - event ....
        February
            date - event ...
            date 
                event
                event

        ..


    """

    res = wikipedia.page(searchStr)

    #pprint(res.content)
    html = res.html()
    soup = bs(html)
    birthres = soup.find("span",{"id":"Births"})
    birthres = fu(birthres)
    
    deathres = soup.find("span",{"id":"Deaths"})
    deathres = fu(deathres)

    eventsres = soup.find("span",{"id":"Events"})
    eventsres = fu(eventsres)
    resDic = {"births":birthres,"deaths":deathres,"events":eventsres}


    return resDic




if __name__=="__main__":
    pass
