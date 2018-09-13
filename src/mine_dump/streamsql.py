from json import dump

class StreamCategoryLinks:

    TOKEN = ""
    CSVTEXT = []

    # 0 = find 'VALUES', 1 = find '(', 2 = read cl_from::int until ',', 3 = read cl_to::String with "'" until ','
    # 0 -> 1, 1 -> 2, 2 -> 3, 3 -> 1
    STATE = 0
    QUOTED = False
    ESCAPED = False

    CC = 0
    CL_FROM = ""

    KEY = ""
    OUT = dict()

    def streamsql(self):
        statemap = {
            0: self.findVALUES,
            1: self.find_open,
            2: self.read_cl_from,
            3: self.read_cl_to
        }

        sqlfile = open("../../data/dump/redirect-categorylinks-data.sql", 'rb')
        outfile = open("../../data/dump/category-links.json", 'w', encoding='ISO-8859-1')
        raw = sqlfile.read(256)
        #self.OUT.write("{")
        while raw:
            for c in raw.decode('ISO-8859-1'):
                self.CC += 1
                if self.CC % 100000000 == 0:
                    print(str(self.CC * 100 / 17303311000) + '%')
                if c is '\\':
                    self.ESCAPED = True
                if self.ESCAPED:
                    self.TOKEN+="\\"+c
                    self.ESCAPED = False
                if c is "'":
                    self.QUOTED = not self.QUOTED
                else:
                    statemap[self.STATE](c)
            raw = sqlfile.read(256)
        #self.OUT.write("]}")
        dump(self.OUT, outfile)
        print("Done")
        sqlfile.close()

    def findVALUES(self, c):
        if self.TOKEN == 'VALUES':
            self.STATE = 1
            self.TOKEN = ""
            return
        if c is " " or self.QUOTED:
            self.TOKEN = ""
            return
        self.TOKEN += c

    def find_open(self, c):
        if not self.QUOTED and c == '(':
            self.STATE = 2
            return

    def read_cl_from(self, c):
        if c == ',':
            self.CL_FROM = self.TOKEN
            self.TOKEN = ""
            self.STATE = 3
            return
        self.TOKEN += c

    def read_cl_to(self, c):
        if not self.QUOTED and c is ',':
            self.add_out(self.CL_FROM, self.TOKEN)
            self.TOKEN = ""
            self.STATE = 1
            return
        elif self.QUOTED:
            self.TOKEN += c

    def add_out(self, key, value):
        if key in self.OUT:
            self.OUT[key].append(value)
        else:
            self.OUT[key] = [value]

        #if key == self.KEY:
        #    self.OUT.write(",\"" + value + "\"")
        #else:
        #    if self.KEY != "":
        #        self.OUT.write("],")
        #    self.KEY = key
        #    self.OUT.write("\""+key+"\":[\""+value+"\"")


StreamCategoryLinks().streamsql()
