#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import test
import sys
import fileinput
import json

import wikipedia
if __name__=="__main__":
    # read complete std in
    
    pageToCheck=base64.b64decode(sys.argv[1])
    

    out = []

    try:
        page = wikipedia.page(pageToCheck,redirect=True)
        allDates = test.find_dates(page.content, max_tokens=50, allow_overlapping=False)
        for d in allDates:
            try:
                out.append(str(d))
            except:
                pass
    except:
        pass

    print json.dumps(out)


