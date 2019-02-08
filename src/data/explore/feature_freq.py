from data import load_articledict


def analyze_feature_frequency(ad, F_SetNames):
    freq = dict()
    for a in ad:
        for F_Name in F_SetNames:
            if F_Name not in ad[a]:
                continue
            for f in ad[a][F_Name]:
                if F_Name + "::" + f not in freq:
                    freq[F_Name + "::" + f] = 0
                freq[F_Name + "::" + f] += 1
    return freq
