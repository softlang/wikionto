from data import load_articledict, DATAP
import webbrowser

ad = load_articledict()
f = open(DATAP + "/temp/deleted_test.txt", "w", encoding="utf-8")

titles = [a for a in ad if ad[a]["Seed"]]

x = 0
for title in titles:
    webbrowser.open("https://en.wikipedia.org/wiki/" + title, new=2)
    print(title)
    agreement = ""
    while agreement not in ["1", "2"]:
        agreement = input(str(x) + " Enter '1' or '2'! '2' for not recognized as deleted.")
    f.write(title + ";" + agreement)
    x += 1
f.flush()
f.close()
