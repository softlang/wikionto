'''
Created on 31.01.2018

@author: MarcelLocal
'''
def check_eponymous(catdict, langdict):
    for cat in catdict:
        if cat in langdict:
            catdict[cat]["Eponymous"] = 1
        else:
            catdict[cat]["Eponymous"] = 0
    return catdict