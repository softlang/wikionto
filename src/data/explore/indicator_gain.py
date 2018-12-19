from data import load_articledict
from collections import Counter

ad = load_articledict()
n = len([a for a in ad if ad[a]["Seed"]])
print("Number of seed articles: " + str(n))

# Infobox Configuration
print()
print("Infobox Configuration")
infoboxavailable = [a for a in ad if "DbpediaInfoboxTemplate" in ad[a] and ad[a]["Seed"]]
print("  "+str(len(infoboxavailable)) + " seed articles have an infobox")
infoboxes = [template for a in ad if "DbpediaInfoboxTemplate" in ad[a] for template in ad[a]["DbpediaInfoboxTemplate"]
             if ad[a]["Seed"]]
counter = Counter(infoboxes)
for infobox, count in counter.items():
    print("  "+infobox + " : " + str(count))

# Infobox Configuration
print()
print("URL Pattern Configuration")
urlpatternavailable = [a for a in ad if "(" in a and ad[a]["Seed"]]
print("  "+str(len(infoboxavailable)) + " seed articles have a URL pattern")
urlwords = [urlword for a in ad if '(' in a for urlword in a.split('(')[1].split(')')[0].split('_') if ad[a]["Seed"]]
counter = Counter(urlwords)
for urlword, count in counter.items():
    if count > 10:
        print("  "+urlword + " : " + str(count))
