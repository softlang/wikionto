from collections import deque
from data import DATAP, INDICATORS
from json import load


def stratify_thoughts_and_statistics():
    f = open(DATAP + "/catdict.json", "r")
    cd = load(f)
    f = open(DATAP + "/articledict.json", "r")
    ld = load(f)

    strat_cat_none = [c for c in cd if cd[c]["#Positive"] + cd[c]["#Negative"] == 0]
    strat_cat_small = [c for c in cd if "articles" in cd[c] and len(cd[c]["articles"]) < 5]
    strat_cat_tp = [c for c in cd if
                    c not in strat_cat_none + strat_cat_small and cd[c]["#Negative"] < 0.25 * len(cd[c]["articles"])]
    strat_cat_tn = [c for c in cd if cd[c]["#Negative"] > 0 and cd[c]["#Positive"] == 0]
    strat_cat_fp = [c for c in cd if cd[c]["#Negative"] > cd[c]["#Positive"] > 0]
    strat_cat_fn = [c for c in cd if cd[c]["#Positive"] >= cd[c]["#Negative"] > 0]
    strat_cat_f = [c for c in strat_cat_fp + strat_cat_fn]

    strat_a_tp = set(a for c in strat_cat_tp for a in cd[c]["articles"])
    strat_a_tn = set(a for c in strat_cat_tn for a in cd[c]["articles"])

    strat_a_fp = set(a for c in strat_cat_fp for a in cd[c]["articles"])
    strat_a_fp_cand = set(a for a in strat_a_fp if any(ld[a][i] for i in INDICATORS))
    strat_a_fp_noise = set(a for a in strat_a_fp if not any(ld[a][i] for i in INDICATORS))

    strat_a_fn = set(a for c in strat_cat_fn for a in cd[c]["articles"])
    strat_a_fn_cand = set(a for a in strat_a_fn if any(ld[a][i] for i in INDICATORS))
    strat_a_fn_noise = set(a for a in strat_a_fn if not any(ld[a][i] for i in INDICATORS))

    strat_a_f = set(a for c in strat_cat_f for a in cd[c]["articles"])
    strat_a_f_cand = set(a for a in strat_a_f if any(ld[a][i] for i in INDICATORS) and a not in strat_a_tp)
    strat_a_f_noise = set(a for a in strat_a_f if not any(ld[a][i] for i in INDICATORS) and a not in strat_a_tn)

    print("True positive hypothetical: " + str(len(strat_a_tp)))
    print("True negative hypothetical: " + str(len(strat_a_tn)))
    print("False positive hypothetical: " + str(len(strat_a_fp)))
    print("  with:")
    print("        " + str(len(strat_a_fp_cand)) + " candidates")
    print("        " + str(len(strat_a_fp_noise)) + " noise")
    print("False negative hypothetical: " + str(len(strat_a_fn)))
    print("  with:")
    print("        " + str(len(strat_a_fn_cand)) + " candidates")
    print("        " + str(len(strat_a_fn_noise)) + " noise")
    print("Total: " + str((len(strat_a_fn) + len(strat_a_fp) + len(strat_a_tn) + len(strat_a_tp))))
    print()
    print("False hypothetical: " + str(len(strat_a_f)))
    print("  with:")
    print("        " + str(len(strat_a_f_cand)) + " candidates")
    print("        " + str(len(strat_a_f_noise)) + " noise")
    print("Alternative Total: " + str((len(strat_a_f_cand) + len(strat_a_f_noise) + len(strat_a_tn) + len(strat_a_tp))))
    print()

    z = 100.0 / (len(strat_a_fn) + len(strat_a_fp) + len(strat_a_tp))
    print(z)
    print("True positive sampled: " + str(len(strat_a_tp) * z))
    print("True negative sampled: " + str(len(strat_a_tn) * z))
    print("False positive candidates sampled: " + str(len(strat_a_fp_cand) * z))
    print("False positive noise sampled: " + str(len(strat_a_fp_noise) * z))
    print("False negative candidates sampled: " + str(len(strat_a_fn_cand) * z))
    print("False negative noise sampled: " + str(len(strat_a_fn_noise) * z))
    print()
    z = 180.0 / (len(strat_a_f_cand) + len(strat_a_f_noise) + len(strat_a_tp))
    print("True positive sampled: " + str(len(strat_a_tp) * z))
    print("True negative sampled: " + str(len(strat_a_tn) * z))
    print("False candidates sampled:" + str(len(strat_a_f_cand) * z))
    print("False noise sampled:" + str(len(strat_a_f_noise) * z))

    print(len([a for a in strat_a_tp if ld[a]["ValidInfobox"] or ld[a]["URLBracesPattern"]]))


def get_subcats_with_articles_transitive(cd, c):
    subcats = set()
    cqueue = deque([c])
    visited = set()
    while cqueue:
        c = cqueue.pop()
        visited.add(c)
        if "articles" in cd[c]:
            subcats.add(c)
        if "subcats" in cd[c]:
            for subcat in cd[c]["subcats"]:
                if subcat not in visited:
                    cqueue.append(subcat)
    return subcats


if __name__ == '__main__':
    stratify_thoughts_and_statistics()
