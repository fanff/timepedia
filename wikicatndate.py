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

def processBirth(res):
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


def fu(searchStr):
    """
    """

    res = wikipedia.page(searchStr)

    #pprint(res.content)
    html = res.html()
    soup = bs(html)
    birthres = soup.find("span",{"id":"Births"})
    birthres = processBirth(birthres)
    
    deathres = soup.find("span",{"id":"Deaths"})
    deathres = processBirth(deathres)

    eventsres = soup.find("span",{"id":"Events"})
    eventsres = processBirth(eventsres)
    resDic = {"births":birthres,"deaths":deathres,"events":eventsres}


    return resDic

if __name__=="__main__":
    ""
    ""

    for ck in range(1600,1990):

        resDic = fu(str(ck))
        fileName = "%s.json"%ck
        with codecs.open(fileName,"w") as out:
            out.write(json.dumps(resDic,indent=True))

