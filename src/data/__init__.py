from os.path import dirname, abspath, join

DATAP = join(dirname(abspath(__file__)), '..', '..', 'data')
DEPTH = 8

CATS = ["Category:Formal_languages", "Category:Computer_file_formats", "Category:Installation_software"]

WIKIDATA = "https://query.wikidata.org/sparql"

KEYWORDS = ['language', 'format', 'notation']

# stretched keywords resulting which maybe hint at languages. Here, maybe means that we subjectively know that such
# software has its own language, but! we cannot objectively present proof in the summary.
XKEYWORDS = [['file', ''], ['file', 'type'], ['template', 'engine'], ['templating', 'system'], ['build', 'tool'],
             ['template', 'system'], ['theorem', 'prover'], ['parser', 'generator'], ['typesetting', 'system']]

#  ex_pattern = ["List_of","comparison","Comparison"]
#  ex_brack = ["song","video_game","TV_series"]
