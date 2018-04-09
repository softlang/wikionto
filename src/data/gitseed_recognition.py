"""
Script support for recognizing Git languages in Wikipedia.
"""
import re
from mine.dbpedia import articles_with_redirects, CLURI, CFFURI

def namenorm(name):
    x = re.sub("\(.*?\)", "", name).lower().strip()
    x = re.sub("[_ /]","",x).strip()
    return x

f = open('../softwarelanguages.csv','r',encoding="utf8")
softwarelanguages = []
for line in f:
    l = line.split("\t")[0]
    x = namenorm(l)
    softwarelanguages.append(x)
f.close

f = open('gitseed.txt','r',encoding="utf8")
git_langs = []
for line in f:
    if line.startswith('#'):
        continue
    try:
        x,y = line.split(',')
    except ValueError:
        print(line)
    git_langs.append((x,namenorm(x)))
f.close

git_recalledlangs = []
git_missinglangs = []
for (l,g) in git_langs:
    if not g in softwarelanguages:
        git_missinglangs.append(l)
    else:
        git_recalledlangs.append(l)


#Redirect strategy

git_recalledredirects = []
redirects = []
results = articles_with_redirects(CLURI, 0, 7)
results.update(articles_with_redirects(CFFURI, 0, 7))

print(len(results))
for result in results:
    language = result["language"]["value"].replace("http://dbpedia.org/resource/", "")
    redirect = result["redirect"]["value"].replace("http://dbpedia.org/resource/", "")
    redirects.append((language,redirect))
    if redirect in git_missinglangs:
        git_missinglangs.remove(redirect)
        git_recalledredirects.append((language,redirect))   
    
print(str(len(git_langs)-len(git_missinglangs))+" of "+str(len(git_langs)))
print(100-(len(git_missinglangs)/len(git_langs))*100)

f=open('gitseed_annotated.txt','w',encoding="utf8")
for l in sorted(git_recalledlangs,key=str.lower):
    f.write(l+",recalled\n")
for (language,redirect) in sorted(git_recalledredirects,key=lambda pair:str.lower(pair[0])):
    f.write(redirect+",recalled redirect to \""+language+"\"\n")
for l in sorted(git_missinglangs,key=str.lower):
    f.write(l+"\n")
f.flush
f.close