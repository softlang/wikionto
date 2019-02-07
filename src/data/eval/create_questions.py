from data import DATAP, load_articledict
from data.eval.random_sampling import get_random_data
from string import Template, ascii_uppercase
from collections import deque


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def generate_pack(foldername, chunk, chunkname):
    assert len(chunk) <= 99
    # Preparation
    QP = DATAP + "/survey/questions"

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
    with open(DATAP + "/survey/sosci_template.txt", "r", encoding="utf-8") as f:
        text = f.read()
    questionTemplate = Template(text)
    Tpage = Template("<page intID=\"${intID}\">\n")
    Tquest = Template("<question id=\"${letterid}${idx}\" intID=\"${intID}\" />\n")
    Ttext = Template("<question id=\"ZZ${idx}\" intID=\"${intID}\" />\n")
    Tembed = Template("""<html intID="${intID}"><![CDATA[
<iframe src="https://en.wikipedia.org/wiki/${title}" title="${title}" width="100%" height="300">
  <p>Your browser does not support iframes.</p>
</iframe>
]]></html>""")

    # file resources
    f_questionnaire = open(QP + "/" + foldername + "/" + str(chunkname) + "_questionnaire.txt", "w", encoding="utf-8")
    f_questionnaire.write("<?xml version=\"1.0\"?>\n<questionnaire>\n")
    f_questions = open(QP + "/" + foldername + "/" + str(chunkname) + "_questions.xml", "w", encoding="utf-8")
    f_questions.write(HEADER)

    intID = 1
    idx = 1
    for a in chunk:
        f_questions.write(questionTemplate.substitute(title=a) + "\n")
        f_questionnaire.write(Tpage.substitute(intID=intID))
        intID += 1
        if idx < 10:
            f_questionnaire.write(Tquest.substitute(letterid=chunkname, idx="0" + str(idx), intID=intID))
            intID += 1
            f_questionnaire.write(Ttext.substitute(idx="0" + str(idx), intID=intID))
        else:
            f_questionnaire.write(Tquest.substitute(letterid=chunkname, idx=idx, intID=intID))
            intID += 1
            f_questionnaire.write(Ttext.substitute(idx=idx, intID=intID))
        intID += 1
        f_questionnaire.write(Tembed.substitute(title=a, intID=intID))
        f_questionnaire.write("</page>\n")
        idx += 1
        intID += 1

    f_questions.write(END)
    f_questions.close()
    f_questionnaire.write("</questionnaire>")
    f_questionnaire.close()


A_traintest, y = get_random_data()
ad = load_articledict()
A_seed = [a for a in ad if ad[a]["Seed"]]
A_eval = [a for a in ad if a not in A_seed and a not in A_traintest]

letters = ascii_uppercase
letters2 = [c1 + c2 for c1 in letters for c2 in letters]
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
