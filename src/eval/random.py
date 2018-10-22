from data import DATAP
from json import load
import random

with open(DATAP + '/langdict.json', 'r', encoding="UTF8") as f:
    langdict = load(f)
with open(DATAP + '/eval/random.csv', 'w', encoding="UTF8") as f:
    articles = list(langdict.keys())
    articles.sort()
    articles_visited = set()
    for x in range(1483):
        index = random.randint(0, len(langdict))
        article = articles[index]
        if article in articles_visited:
            x -= 1
        else:
            print("https://en.wikipedia.org/wiki/"+article)
            agreement = ""
            while agreement not in ["yes", "no"]:
                agreement = input("Enter 'yes' or 'no'!")
            if agreement == "yes":
                agreement_int = "1"
            if agreement == "no":
                agreement_int = "0"
            f.write("|"+article + "|,|" + agreement_int + "|\n")