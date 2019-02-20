from data import DATAP, load_articledict
from data.eval.random_sampling import get_random_data
from string import Template, ascii_uppercase
from collections import deque
from json import dump

QP = DATAP + "/survey/questions"


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


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

    qnr = 1
    for a in chunk:
        f_questions.write(questionTemplate.substitute(title=a, qnr=qnr) + "\n")
        qnr += 1

    f_questions.write(END)
    f_questions.close()


A_traintest, y = get_random_data()
ad = load_articledict()
A_seed = [a for a in ad if ad[a]["Seed"]]
A_eval = [a for a in ad if a not in A_seed and a not in A_traintest]

letters = ascii_uppercase
letters2 = [c1 + c2 for c1 in letters for c2 in letters]
nr = 1
for ls in letters2:
    if nr > 40:
        break
    print(str(nr) + " = " + ls)
    print(str(nr+1) + " = " + ls)
    nr += 2
letterids = deque(letters2[:-2])

chunk_lists = []
chunks_A_traintest = chunks(A_traintest, 94)
Qs_seedtemp = A_seed * 12
print(len(A_traintest) / 94)
assert (len(A_traintest) / 94) <= len(letterids)
for Qs_traintest in chunks_A_traintest:
    Qs_seedi = Qs_seedtemp[:5]
    Qs_seedtemp = Qs_seedtemp[5:]
    chunkname = letterids.popleft()
    generate_pack("test", Qs_seedi + Qs_traintest, chunkname)

chunk_lists = []
chunks_A_eval = chunks(A_eval, 94)
chunks_queue = deque(chunks_A_eval)
Qs_seedtemp = A_seed * 24
print(len(A_eval) / 94)
letterids = deque(letters2[:-2])
while letterids:
    Qs_eval = chunks_queue.popleft()
    Qs_seedi = Qs_seedtemp[:5]
    assert len(Qs_seedi) == 5
    Qs_seedtemp = Qs_seedtemp[5:]
    chunkname = letterids.popleft()
    generate_pack("eval", Qs_seedi + Qs_eval, chunkname)

generate_questionnaire()
