from data import DATAP, load_articledict
from data.eval.random_sampling import get_random_data

QP = DATAP + "/survey"

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


A_traintest, y = get_random_data()
ad = load_articledict()
A_seed = [a for a in ad if ad[a]["Seed"]]
A_eval = [a for a in ad if a not in A_seed and a not in A_traintest]

chunks_A_traintest = chunks(A_traintest, 100)

Qs_seedtemp = A_seed * 12

i = 0
for Qs_traintest in chunks_A_traintest:
    Qs_seedi = Qs_seedtemp[:5]
    Qs_seedtemp = Qs_seedtemp[5:]
    questions = Qs_seedi + Qs_traintest
    with open(QP + "/questions_test"+str(i)+".txt", "w", encoding="utf-8") as f:
        for a in questions:
            f.write("https://en.wikipedia.org/wiki/" + a + "\n")
    i += 1

Qs_seedtemp = A_seed * 24
i = 0
chunks_A_eval = chunks(A_eval, 100)
for Qs_eval in chunks_A_eval:
    Qs_seedi = Qs_seedtemp[:5]
    assert len(Qs_seedi) == 5
    Qs_seedtemp = Qs_seedtemp[5:]
    questions = Qs_seedi + Qs_eval
    with open(QP + "/questions_eval"+str(i)+".txt", "w", encoding="utf-8") as f:
        for a in questions:
            f.write("https://en.wikipedia.org/wiki/" + a + "\n")
    i += 1
