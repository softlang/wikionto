from check.langdictcheck import LangdictCheck
from data import DATAP
from json import load
from mine.wiki import getlinks

lists = ["List_of_XML_markup_languages",
         "List_of_content_syndication_markup_languages",
         "List_of_document_markup_languages",
         "List_of_markup_languages",
         "List_of_stylesheet_languages",
         "Generational_list_of_programming_languages",
         "List_of_C-family_programming_languages",
         "List_of_CLI_languages",
         "List_of_Chinese_programming_languages",
         "List_of_JVM_languages",
         "List_of_Lisp-family_programming_languages",
         "List_of_audio_programming_languages",
         "List_of_concurrent_and_parallel_programming_languages",
         "List_of_constraint_programming_languages",
         "List_of_educational_programming_languages",
         "List_of_object-oriented_programming_languages",
         "List_of_programming_languages",
         "List_of_programming_languages_by_type",
         "List_of_programming_languages_for_artificial_intelligence",
         "List_of_programming_languages_with_algebraic_data_types",
         "List_of_reflective_programming_languages_and_platforms",  # ?
         "List_of_user_interface_markup_languages",
         "List_of_program_transformation_systems",  # ?
         "List_of_functional_programming_languages",
         "List_of_file_formats",
         "List_of_motion_and_gesture_file_formats",
         "List_of_open_formats",
         "List_of_archive_formats"]


def explore_all():
    f = open(DATAP + "/langdict.json", "r", encoding="UTF8")
    langdict = load(f)
    for cl in langdict:
        if ("list" in cl.lower()) & (("language" in cl.lower()) | ("format" in cl.lower())):
            print(cl)


class WikiList(LangdictCheck):
    def check(self,langdict):
        for page in lists:
            links = getlinks(page)
            for l in links:
                ln = l.replace(' ', '_')
                if ln in langdict:
                    langdict[ln]['In_Wikipedia_List'] = 1
                elif not any(w in l for w in ["Wikipedia", "Template", "Category", "Help", "Talk", "Portal"]):
                    print(ln)
        return langdict


if __name__ == "__main__":
    WikiList().solo()
