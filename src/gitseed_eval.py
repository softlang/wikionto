import re

f = open('gitseed_annotated.txt','r',encoding="utf8")
annotationeval = []
evaldict = dict()
#(method,lang)
for line in f:
    annotation = re.sub("\".*?\"","",line.split(",")[1]).strip()
    lang = line.split(",")[0]
    if annotation not in evaldict:
        evaldict[annotation] = [lang]
    else:
        langlist = evaldict[annotation]
        langlist.append(lang)
for k,v in evaldict.items():
    print(k+","+str(len(v)))