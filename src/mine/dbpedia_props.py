from json import load, dump
from data import DATAP
import pandas as pd
import matplotlib.pyplot as plt
from mine.dbpedia import properties_in, articles_out_with,CLURI,CFFURI


def properties():
    propdict = properties_in(CLURI,0,6)
    resultsCFF = properties_in(CFFURI,0,6)
    for propname in resultsCFF:
        if propname in propdict:
            propdict[propname]["in_count"] = propdict[propname]["in_count"] + resultsCFF[propname]["in_count"]
        else:
            propdict[propname] = dict()
            propdict[propname]["in_count"] = resultsCFF[propname]["in_count"]
    for propname in propdict:
        print(propname)
        propdict[propname]["out_count"] = len(articles_out_with(propname, 0, 6))
    with open(DATAP+'/all_props.json', 'w',encoding="UTF8") as f:
        dump(obj=propdict, fp=f, indent=2)
        f.flush()
        f.close()

def plot_props():
    f = open(DATAP + '/all_props.json', 'r', encoding="UTF8")
    pf = pd.DataFrame(load(f)).transpose()

    pf = pf[pf.out_count < pf.in_count + 500].reindex(columns=['in_count','out_count']).sort_values(by='out_count')
    print(pf.to_csv())
    fig, axes = plt.subplots(nrows=1, ncols=1)
    pf.plot(kind='bar', ax=axes, color='orange', y='in_count', label='#in_CL')
    pf.plot(kind='line', ax=axes, color='blue', y='out_count', label='#not_CL')
    plt.xticks(rotation=80)
    plt.show()

if __name__ == '__main__':
    properties()
    #plot_props()
