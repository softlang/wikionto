VARIANT_IDS = ['The', 'isa', 'isoneof', 'isnameof', 'ismemberof', 'isfamilyof']


class HearstAutomaton():

    # processes the token dictionary for one sentence
    def __init__(self, token_dict):
        self.token_dict = token_dict
        self.state = dict()
        for variant in VARIANT_IDS:
            self.state[variant] = self.initial
        self.state["The"] = self.the_initial
        self.hypernyms = dict()
        for variant in VARIANT_IDS:
            self.hypernyms[variant] = []

    def run(self):
        for index in range(1, len(self.token_dict)):
            wdict = self.token_dict[index]
            for variant in VARIANT_IDS:
                self.state[variant](variant, wdict['word'], wdict['pos'])
        return self.hypernyms

    def finalstate(self, variant, word, tag):
        pass

    def the_initial(self, variant, word, tag):
        if variant == 'The' and word == 'The' and tag == 'DT':
            self.state["The"] = self.the_catchnn
        else:
            self.state["The"] = self.finalstate

    def initial(self, variant, word, tag):
        if tag == 'VBZ' and word in ['is', 'refers', 'denotes', 'specifies'] or \
                tag == 'VBD' and word in ['was', 'referred', 'denoted', 'specified']:
            self.state[variant] = self.cdordt

    def the_catchnn(self, variant, word, tag):
        if tag in ['JJ', 'NNP', 'NNS']:
            return
        elif tag == 'NN':
            self.hypernyms[variant].append(word)
        else:
            self.state[variant] = self.finalstate

    def cdordt(self, variant, word, tag):
        if variant == 'isoneof' and word == 'one' and tag == 'CD':
            self.state[variant] = self.catchof
        elif word in ['a', 'an', 'the'] and tag == 'DT':
            if variant == 'isnameof':
                self.state[variant] = self.catchname
            elif variant in ['ismemberof', 'isfamilyof']:
                self.state[variant] = self.catchmemberfamily
            elif variant == 'isa':
                self.state[variant] = self.catchnn

    def catchname(self, variant, word, tag):
        if word == 'name' and 'tag' == 'NN':
            self.state[variant] = self.catchof

    def catchmemberfamily(self, variant, word, tag):
        if variant == 'ismemberof' and word == 'member' and tag == 'NN':
            self.state[variant] = self.catchof
        elif variant == 'isfamilyof' and word == 'family' and tag == 'NN':
            self.state[variant] = self.catchof

    def catchof(self, variant, word, tag):
        if variant == 'isnameof' and word in ['of', 'for']:
            self.state[variant] = self.catchnn
        elif word in ['of'] and tag == 'IN':
            self.state[variant] = self.catchnns


    def catchnn(self, variant, word, tag):
        if tag == 'NN':
            self.hypernyms[variant].append(word)

    def catchnns(self, variant, word, tag):
        if variant == 'ismemberof' and word == 'family' and tag == 'NN':
            self.hypernyms[variant].append(word)
        if tag == 'NNS':
            self.hypernyms[variant].append(word)
