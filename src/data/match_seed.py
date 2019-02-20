import yaml
from data import DATAP
import json

with open(DATAP+"/temp/gitseed.yml", 'r') as stream:
    try:
        gitseed = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

print(len(gitseed))


with open(DATAP+"/temp/gitseed_annotated.json", 'r', encoding="utf-8") as stream:
    gitseed_annotated = json.load(stream)

print(len(gitseed_annotated))

for a in gitseed:
    if a not in gitseed_annotated:
        print(a)
