from data import DATAP
from json import load
import re
from subprocess import call

TP = DATAP + "/temp/trees"

def transform(fitted_ids, k):
    in_file_path = TP + "/sltree"+str(k)+".dot"
    in_file = open(in_file_path, 'r', encoding='utf-8')
    out_file_path = TP + "/sltree" + str(k) + "_name.dot"
    out_file = open(out_file_path, 'w', encoding='utf-8')

    with open(DATAP + '/f_to_id.json', 'r', encoding='utf-8') as id_file:
        f_to_id = load(id_file)
        id_to_f = {fid: fname for fname, fid in f_to_id.items()}

    print("Transforming file")
    for line in in_file:
        if 'X[' not in line:
            out_file.write(line)
            continue
        else:
            m = re.search(r'X\[([0-9]+)\]', line)
            fid = int(m.group()[2:-1])
            fname = id_to_f[fitted_ids[fid]]
            line2 = re.sub(r'X\[' + str(fid) + '\]', 'X[' + fname + ']', line)
            out_file.write(line2)
            out_file.write('\n')
            out_file.flush()
    out_file.close()
    in_file.close()
    call(["dot", "-Tpdf", out_file_path, "-o", TP + "/sltree"+str(k)+"_name.pdf"])
