from data import DATAP
from json import load
import re

def transform():
    with open(DATAP+'/f_to_id.json', 'r', encoding='utf-8') as f:
        f_to_id = load(f)
        id_to_f = {fid:fname for fname, fid in f_to_id.items()}

    with open(DATAP+'/sltree_names.dot', 'w', encoding='utf-8') as f2:
        with open(DATAP+'/sltree.dot', 'r', encoding='utf-8') as f:
            for line in f:
                if 'X[' not in line:
                    f2.write(line)
                    continue
                else:
                    m = re.search(r'X\[([0-9]+)\]', line)
                    fid = int(m.group()[2:-1])
                    fname = id_to_f[fid]
                    line2 = re.sub(r'X\[' + str(fid) + '\]', 'X[' + fname + ']', line)
                    f2.write(line2)
                f2.write('\n')
                f2.flush()

if __name__ == '__main__':
    transform()
