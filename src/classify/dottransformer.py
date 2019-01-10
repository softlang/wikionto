from data import DATAP
from json import load
import re
from subprocess import call


def transform(in_file, out_file):
    with open(DATAP + '/f_to_id.json', 'r', encoding='utf-8') as id_file:
        f_to_id = load(id_file)
        id_to_f = {fid: fname for fname, fid in f_to_id.items()}

    for line in in_file:
        if 'X[' not in line:
            out_file.write(line)
            continue
        else:
            m = re.search(r'X\[([0-9]+)\]', line)
            fid = int(m.group()[2:-1])
            fname = id_to_f[fid]
            line2 = re.sub(r'X\[' + str(fid) + '\]', 'X[' + fname + ']', line)
            out_file.write(line2)
            out_file.write('\n')
            out_file.flush()


def transform_trees():
    pathin = DATAP + "/temp/trees/sltree<n>.dot"
    pathout = DATAP + "/temp/trees/sltree<n>_names.dot"
    for x in range(0, 100, 1):
        with open(pathout.replace("<n>", str(x)), 'w', encoding='utf-8') as out_file:
            with open(pathin.replace("<n>", str(x)), 'r', encoding='utf-8') as in_file:
                transform(in_file, out_file)
        call(["dot", "-Tpdf", pathout.replace("<n>", str(x)), "-o", pathout.replace("<n>",str(x)).replace("dot", "pdf")])


if __name__ == '__main__':
    transform_trees()
