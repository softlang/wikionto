from os.path import dirname, abspath, join
from mine.wikidata import get_computer_languages, get_computer_formats
from mine.yago import get_artificial_languages
from json import load

# UTIL
DATAP = abspath(join(dirname(abspath(__file__)), '..', '..', 'data'))


def load_articledict():
    return load(open(DATAP + "/articledict.json", "r"))


def load_catdict():
    return load(open(DATAP + "/catdict.json", "r"))


# - Wikidata
def wikidata_articles():
    return set(get_computer_languages() + get_computer_formats())


# - Yago
def yago_articles():
    return set(get_artificial_languages())


# - Wikipedia Lists
def retrievelists():
    list_articles = []
    # the file is derived from executing and filtering results of data.explore.explore_lists
    for line in open(DATAP + "/temp/Language_Lists.txt", "r", encoding="UTF8"):
        list_articles.append(line.strip())
    return list_articles


# SCOPING
DEPTH = 8
ROOTS = ["Category:Formal_languages", "Category:Computer_file_formats", "Category:Installation_software"]

INDICATORS = ["POS", "PositiveInfobox", "In_Wikipedia_List", "URLBracesPattern"]

# CONFIG FOR INDICATORS
# - for POS and URLBracesPattern
KEYWORDS = ['language', 'format', 'notation']

# - stretched keywords resulting which maybe hint at languages. Here, maybe means that we subjectively know that such
#   software has its own language, but! we cannot objectively present proof in the summary.
XKEYWORDS = [['file', 'type'], ['template', 'engine'], ['templating', 'system'], ['build', 'tool'],
             ['template', 'system'], ['theorem', 'prover'], ['parser', 'generator'], ['typesetting', 'system']]

# - infobox indication
POSITIVETEMPLATES = ["infobox_programming_language", "infobox_file_format"]

# - Wikipedia Lists
LIST_ARTICLES = retrievelists()

# CONFIG FOR NEGATIVE INDICATION (EXPLORATION USE)
# - Negative categories
NOISY_CATS = ['Category:Statistical_data_types', 'Category:Knowledge_representation',
              'Category:Propositional_attitudes‎',
              'Category:Theorems']
# - Note that all other infoboxes are negative. There are about 600 different templates used in the scope.
NEUTRALTEMPLATES = ["infobox_software", "infobox_technology_standard", "infobox_software_license"] + \
                   ["infobox", "infobox_unit", "infobox_data_structure", "infobox_writing_system",
                    "infobox_quality_tool", "infobox_identifier"]

# - Negative URL keywords
EX_URL_KEYWORD = ["List_of", "comparison", "Comparison"]
EX_URLBRACE_KEYWORD = ["song", "video_game", "TV_series"]
