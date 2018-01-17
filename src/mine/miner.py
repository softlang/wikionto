from mine.dbpedia import articles_below

def writeList(cllist,filename):
    f = open(filename, 'w',encoding='utf8')
    f.write("name\t CLdepth\t CFFdepth\n")
    for (a,d1,d2) in cllist:
        f.write(a+"\t"+str(d1)+"\t"+str(d2)+"\n")
    f.flush
    f.close

cls_result = list(map(lambda x: (x,0),articles_below("<http://dbpedia.org/resource/Category:Computer_languages>",0,0)))
cffs_result = list(map(lambda x: (x,0),articles_below("<http://dbpedia.org/resource/Category:Computer_file_formats>",0,0)))
for i in range(7):
    x=i+1
    cls = articles_below("<http://dbpedia.org/resource/Category:Computer_languages>",x,x)
    cls_result = cls_result + [(cl,x) for cl in cls if cl not in list(zip(*cls_result))[0]]
    cffs = articles_below("<http://dbpedia.org/resource/Category:Computer_file_formats>",x,x)
    cffs_result = cffs_result + [(cff,x) for cff in cffs if cff not in list(zip(*cffs_result))[0]]
    
onlycls = [(cl,x,"-") for (cl,x) in cls_result if cl not in list(zip(*cffs_result))[0]]    
onlycff = [(cff,"-",x) for (cff,x) in cffs_result if cff not in list(zip(*cls_result))[0]]    
both = [(cl,x,y) for (cl,x) in cls_result for (cf,y) in list(filter(lambda p: p[0] == cl,cffs_result))] 
result = onlycls + both + onlycff

writeList(result,"softwarelanguages.csv")