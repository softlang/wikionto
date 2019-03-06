import xml.etree.ElementTree as ET
import os
from json import dump

QEP = "S:\Data\Wikipedia\survey\questions\eval"

qdictfile = open(QEP + "/qid_to_a.json", "w", encoding="utf-8")
qdict = {}
for filename in os.listdir(QEP):
    if filename.endswith(".xml"):
        print(filename)
        text = open(QEP + "/" + filename, "r", encoding="utf-8").read()
        root = ET.fromstring(text)
        questions = root.findall("./question")
        assert len(questions) == 99
        for question in questions:
            titletext = question.findall("./title")[0]
            title = titletext.text.split('</a>')[0].split('blank">')[1].strip()
            qid = question.findall("./attributes.specific/attr[@id='id']")[0].text.strip()
            if len(qid) == 1:
                qid = '0' + qid
            qsetchars = filename.split("_")[0].strip()
            qdict[qsetchars + qid] = title

dump(qdict, qdictfile)
qdictfile.close()
