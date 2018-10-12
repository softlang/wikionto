import re
import warnings

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.corpora.wikicorpus import filter_wiki
from nltk.tokenize import sent_tokenize
import mwparserfromhell


def extract_first_sentence(text):
    # extraction section 0
    summary_content = text.encode('UTF-8').decode('UTF-8')
    top_level_heading_regex = r"\n==[^=].*[^=]==\n"
    summary_content = re.split(top_level_heading_regex, summary_content)[0]
    summary_content = filter_wiki(summary_content)
    summary_content = re.sub(r"'''", "", summary_content)
    summary_content = re.sub(r'\\n', ' ', summary_content)
    summary_content = re.sub(r'\\', '', summary_content)
    summary_content = re.sub(r"(\(.*?\))", "", summary_content)
    summary_content = summary_content.strip()
    sents = sent_tokenize(summary_content)
    if len(sents) < 1:
        return ""
    first = sents[0]
    if sents[0] is "." or sents[0] is "" or sents[0].startswith("See also"):
        if len(sents) > 1:
            first = sents[1]
        else:
            return ""
    return first.strip()


# TODO: Sometimes returns infobox even though we use strip code
def mwparserfromhell_first_sentence(text):
    try:
        wikicode = mwparserfromhell.parse(text)
    except:
        return ("------Error text------\n" + text)
    sections = wikicode.get_sections()
    if not sections:
        return ""
    summary = sections[0].strip_code(normalize=True)
    summary = re.sub('\\n', ' ', summary)
    sents = sent_tokenize(summary)
    if len(sents) < 1:
        return ""
    first = sents[0]
    if sents[0] is "." or sents[0] is "" or sents[0].startswith("See also"):
        if len(sents) > 1:
            first = sents[1]
        else:
            return ""
    return first
