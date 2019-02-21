from data import DATAP, load_articledict, save_articledict, valid_article
from data.eval.random_sampling import get_random_data
from string import Template, ascii_uppercase
from collections import deque
from json import dump
import random

QP = DATAP + "/survey/questions"


def randomchunks(articles, articledict, chunksize, chunknumber):
    visited = set()
    articles.sort()

    chunks = []
    chunkindex = 0
    chunks.append([])
    while len(visited) != len(articles):
        index = random.randint(0, len(articles))
        article = articles[index]

        if article in visited:
            continue
        visited.add(article)

        chunks[chunkindex].append(article)
        articledict[article]["Eval"] = 1

        if len(chunks[chunkindex]) == chunksize:
            chunkindex += 1
            if chunkindex == chunknumber:
                break
            chunks.append([])
    return chunks, articledict


def randomize_order(articles):
    rand_articles = []
    while len(articles) != len(rand_articles):
        index = random.randint(0, len(articles)-1)
        article = articles[index]
        if article not in rand_articles:
            rand_articles.append(article)
    return rand_articles


def generate_questionnaire():
    pageTemplate = Template("""
    <page intID="${intID1}">
    <php intID="${intID2}"><![CDATA[
    $$code = value('ZY01x01', 'label');
    $$kennung = $$code.'${qnr}'; 
    question($$kennung);
    ]]></php>
    <question id="ZZ${qnr}" intID="${intID3}" />
    </page>
    """)

    f_questionnaire = open(QP + "/questionnaire.xml", "w", encoding="utf-8")
    f_questionnaire.write("""<?xml version="1.0"?>
    <questionnaire>
    <page intID="1">
    <question id="ZY02" intID="2" />
    <question id="ZY01" intID="3" />
    </page>""")

    qnr = 1
    intID = 3
    while qnr < 100:
        if qnr < 10:
            f_questionnaire.write(
                pageTemplate.substitute(intID1=intID + 1, intID2=intID + 2, intID3=intID + 3, qnr="0" + str(qnr)))
        else:
            f_questionnaire.write(
                pageTemplate.substitute(intID1=intID + 1, intID2=intID + 2, intID3=intID + 3, qnr=qnr))
        qnr += 1
        intID += 3

    f_questionnaire.write("</questionnaire>")
    f_questionnaire.close()


def generate_pack(foldername, chunk, chunkname):
    assert len(chunk) <= 99
    # Preparation

    HEADER = """<?xml version="1.0" encoding="UTF-8" ?>
    <!DOCTYPE surveyContent SYSTEM "https://www.soscisurvey.de/templates/doctype.survey.dtd">
    <surveyContent version="2.4" type="question">
    <program>oFb</program>
    <version>3.1.06-i</version>
    <timestamp>2019-02-04 12:54:29</timestamp>
    <language>eng</language>
    <title>Wikipedia Topic Survey</title>
    <description />
    """
    END = "\n</surveyContent>"

    # Templates
    with open(DATAP + "/survey/sosci_template.xml", "r", encoding="utf-8") as f:
        text = f.read()
    questionTemplate = Template(text)

    # file resources
    f_questions = open(QP + "/" + foldername + "/" + str(chunkname) + "_questions.xml", "w", encoding="utf-8")
    f_questions.write(HEADER)

    # util json file for assignments
    qid_to_a = dict()

    qnr = 1
    for a in chunk:
        f_questions.write(questionTemplate.substitute(title=a, qnr=qnr) + "\n")
        qid_to_a[chunkname + str(qnr)] = a
        qnr += 1

    with open(QP + "/qid_to_article.json", "w", encoding="utf-8") as f:
        dump(qid_to_a, f)

    f_questions.write(END)
    f_questions.close()


A_traintest, y = get_random_data()
ad = load_articledict()
for a in ad:
    ad[a]["Eval"] = 0
A_seed = [a for a in ad if ad[a]["Seed"]]
A_eval = [a for a in ad if
          a not in A_seed
          and a not in A_traintest
          and valid_article(a, ad)]

letters = ascii_uppercase
letters2 = [c1 + c2 for c1 in letters for c2 in letters]
nr = 1
for ls in letters2:
    if nr > 20:
        break
    print(str(nr) + " = " + ls)
    nr += 1
letterids = deque(letters2[:-2])

chunks_A_eval, ad = randomchunks(A_eval, ad, 90, 20)
print(len(chunks_A_eval))
assert len([a for c in chunks_A_eval for a in c]) == (90 * 20)
chunks_queue = deque(chunks_A_eval)
seedtitles = A_seed * 40
print("The number of chunks is actual " + str(len(chunks_A_eval)) + " vs estimated " + str(len(A_eval) / 90))
while len(chunks_queue) != 0:
    chunkname = letterids.popleft()
    print("Generating "+chunkname)
    chunk = chunks_queue.popleft()
    seedchunk = seedtitles[:9]
    assert len(seedchunk) == 9
    seedtitles = seedtitles[9:]
    # starter questions + mixin
    finalchunk = seedchunk[:5] + randomize_order(seedchunk[5:] + chunk)
    assert len(finalchunk) == 99
    generate_pack("eval", finalchunk, chunkname)

print("Generate Questionnaire")
generate_questionnaire()
print("Save articledict")
save_articledict(ad)
