import operator
from json import load, dump
from itertools import combinations
from data import DATAP,CLDEPTH,CFFDEPTH
import pandas as pd
import matplotlib.pyplot as plt
from mine.dbpedia import properties_in, reverse_properties_in, articles_out_with, articles_out_with_reverse, CLURI, CFFURI

g_properties = {"wordnet_type","title","logo","icon","caption","developer","years","year","screenshot","type","name","website"
                "wikt","after","before","commons","url","align"}

ex_properties = {"recorded","artist","album","thisSingle","accessdate","fromAlbum","lastSingle","nextSingle",
                 "nosales","composer","streaming","writingCredits"
                 ,"thesisYear","workInstitutions","workplaces","thesisUrl","thesisTitle","species","spouse",
                 "battery"}


def properties():
    propdict = properties_in(CLURI, 0, CLDEPTH)
    propdict_cff = properties_in(CFFURI, 0, CFFDEPTH)
    for propname in propdict_cff:
        if propname in propdict:
            propdict[propname]["in_count"] = propdict[propname]["in_count"] + propdict_cff[propname]["in_count"]
        else:
            propdict[propname] = dict()
            propdict[propname]["in_count"] = propdict_cff[propname]["in_count"]
    for propname in propdict:
        print(propname)
        propdict[propname]["out_count"] = articles_out_with(propname, 0, CLDEPTH, 0, CFFDEPTH)
    with open(DATAP + '/all_props.json', 'w', encoding="UTF8") as f:
        dump(obj=propdict, fp=f, indent=2)
        f.flush()
        f.close()


def reverse_properties():
    propdict = reverse_properties_in(CLURI, 0, CLDEPTH)
    resultsCFF = reverse_properties_in(CFFURI, 0, CFFDEPTH)
    for propname in resultsCFF:
        if propname in propdict:
            propdict[propname]["in_count"] = propdict[propname]["in_count"] + resultsCFF[propname]["in_count"]
        else:
            propdict[propname] = dict()
            propdict[propname]["in_count"] = resultsCFF[propname]["in_count"]
    for propname in propdict:
        print(propname)
        propdict[propname]["out_count"] = articles_out_with_reverse(propname, 0, CLDEPTH, 0, CFFDEPTH)
    with open(DATAP + '/all_reverse_props.json', 'w', encoding="UTF8") as f:
        dump(obj=propdict, fp=f, indent=2)
        f.flush()
        f.close()


def properties_to_articles():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    with open(DATAP + '/all_props.json', 'r', encoding="UTF8") as f:
        propdict = load(f)
        for p in propdict:
            propdict[p]["articles"] = []
            for cl in langdict:
                if "properties" not in langdict[cl]:
                    continue
                if p in langdict[cl]["properties"]:
                    propdict[p]["articles"].append(cl)
    with open(DATAP + '/all_props.json', 'w', encoding="UTF8") as f:
        dump(propdict, f, indent=2)


def property_extents():
    f = open(DATAP + '/all_props.json', 'r', encoding="UTF8")
    propdict = load(f)
    prop_extent = dict()
    props0 = sorted(propdict.keys())
    for c in combinations(props0, 2):
        p1 = c[0]
        p2 = c[1]
        articles1 = set(propdict[p1]["articles"])
        articles2 = set(propdict[p2]["articles"])
        articlesx = articles1 & articles2
        if len(articlesx) > 1:
            if p1 in prop_extent:
                prop_extent[p1]["extents"].append(p2)
            else:
                prop_extent[p1] = dict()
                prop_extent[p1]["extents"] = [p2]
            if p2 in prop_extent:
                prop_extent[p2]["extents"].append(p1)
            else:
                prop_extent[p2] = dict()
                prop_extent[p2]["extents"] = [p1]
    for p in prop_extent:
        exsize = len(prop_extent[p]["extents"])
        prop_extent[p]["size"] = exsize
    f = open(DATAP + '/prop_extents.json', 'w', encoding="UTF8")
    dump(prop_extent, f, indent=2)
    f.close()
    ext_size = dict()
    for p in prop_extent:
        ext_size[p] = prop_extent[p]["size"]
    ex_sorted = sorted(ext_size.items(), key=operator.itemgetter(1), reverse=True)
    for p,s in ex_sorted:
        print(p + ' ' + str(s))


def property_lattice():
    f = open(DATAP + '/all_props.json', 'r', encoding="UTF8")
    propdict = load(f)
    prop_lat0 = dict()
    props0 = sorted(list(filter(lambda p: propdict[p]["out_count"] != 10000, propdict.keys())))
    for c in combinations(props0, 2):
        articles1 = set(propdict[c[0]]["articles"])
        articles2 = set(propdict[c[1]]["articles"])
        articlesx = articles1 & articles2
        if len(articlesx) > 1:
            prop_lat0[",".join(c)] = list(articlesx)
    f = open(DATAP + '/prop_lattice2.json', 'w', encoding="UTF8")
    dump(prop_lat0, f, indent=2)
    f.close()

    f = open(DATAP + '/prop_extents.json', 'r', encoding="UTF8")
    prop_extents = load(f)
    x = 3
    while True:
        f = open(DATAP + '/prop_lattice'+str(x-1)+'.json', 'r', encoding="UTF8")
        prop_lat1 = load(f)
        f.close()
        prop_lat2 = dict()
        for p1 in prop_lat1:
            keylist = p1.split(',')
            extents = set(prop_extents[keylist[0]]["extents"])
            for p in keylist:
                extents = extents & set(prop_extents[p]["extents"])
            for p2 in extents:
                if (p2 in keylist) | (propdict[p2]["out_count"] == 10000):
                    continue
                newkeylist = list(keylist)
                newkeylist.append(p2)
                keytext = ",".join(sorted(newkeylist))
                if keytext in prop_lat2:
                    continue
                articles1 = set(prop_lat1[p1])
                articles2 = set(propdict[p2]["articles"])
                articlesx = articles1 & articles2
                if len(articlesx) > 1:
                    prop_lat2[keytext] = list(articlesx)
        print(x)
        print(len(prop_lat2))
        if not prop_lat2:
            break
        f = open(DATAP + '/prop_lattice' + str(x) + '.json', 'w', encoding="UTF8")
        dump(prop_lat2, f, indent=2)
        f.close()
        x += 1


def find_insightful():
    f = open(DATAP + '/prop_extents.json', 'r', encoding="UTF8")
    ed = load(f)
    psdict = dict()
    for p in ed:
        psdict[p] = ed[p]["size"]
    sorted_ps = sorted(psdict.items(),key=operator.itemgetter(1))
    for p,s in sorted_ps:
        print(p + ' ' + str(s))


def plot_props():
    f = open(DATAP + '/all_props.json', 'r', encoding="UTF8")
    pf = pd.DataFrame(load(f)).transpose()

    pf = pf[pf.out_count < pf.in_count + 500].reindex(columns=['in_count', 'out_count']).sort_values(by='out_count')
    print(pf.to_csv())
    fig, axes = plt.subplots(nrows=1, ncols=1)
    pf.plot(kind='bar', ax=axes, color='orange', y='in_count', label='#in_CL')
    pf.plot(kind='line', ax=axes, color='blue', y='out_count', label='#not_CL')
    plt.xticks(rotation=80)
    plt.show()


if __name__ == '__main__':
    #properties()
    #reverse_properties()
    #properties_to_articles()
    #property_extents()
    property_lattice()
    # plot_props()
    #find_insightful()
