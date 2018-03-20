def check_eponymous(catdict, langdict):
    print("Checking for Eponymous")
    for cat in catdict:
        if cat in langdict:
            catdict[cat]["Eponymous"] = 1
        else:
            catdict[cat]["Eponymous"] = 0
    return catdict