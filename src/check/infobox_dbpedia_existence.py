from check.langdictcheck import LangdictCheck

validibs = ["infobox_programming_language", "infobox_file_format"]
nonnegibs = ["infobox_software", "infobox_technology_standard", "infobox_software_license"] + \
            ["infobox", "infobox_unit", "infobox_data_structure", "infobox_writing_system",
             "infobox_quality_tool", "infobox_identifier"]

class InfoboxDbEx(LangdictCheck):

    def check(self, langdict):
        print("Checking for infobox existence")

        for cl in langdict:
            langdict[cl]["ValidInfobox"] = 0
            if "DbpediaInfoboxTemplate" not in langdict[cl]:
                langdict[cl]["negativeSeedCandidate"] = 0
                continue
            ibs = langdict[cl]["DbpediaInfoboxTemplate"]
            langdict[cl]["MultiInfobox"] = len(ibs)
            langdict[cl]["negativeSeedCandidate"] = int(not any(ib in ibs for ib in nonnegibs+validibs) and bool(ibs))
            for ib in validibs:
                if ib in ibs:
                    langdict[cl][ib] = 1
                    langdict[cl]["ValidInfobox"] = 1

        return langdict


if __name__ == "__main__":
    InfoboxDbEx().solo()
