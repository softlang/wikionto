from os.path import dirname, abspath, join

DATAP = join(dirname(abspath(__file__)), '..', '..', 'data')
CLDEPTH = 7
CFFDEPTH = 7

WIKIDATA = "https://query.wikidata.org/sparql"

KEYWORDS = ['language', 'format', 'notation']

# stretched keywords resulting which maybe hint at languages. Here, maybe means that we subjectively know that such
# software has its own language, but! we cannot objectively present proof in the summary.
XKEYWORDS = [['file', ''], ['template', 'engine'], ['templating', 'system'], ['build', 'tool'],
             ['template', 'system'], ['theorem', 'prover'], ['parser', 'generator'], ['typesetting', 'system']]

#  ex_pattern = ["List_of","comparison","Comparison"]
#  ex_brack = ["song","video_game","TV_series"]