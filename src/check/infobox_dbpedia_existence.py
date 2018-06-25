from check.langdictcheck import LangdictCheck


class InfoboxDbEx(LangdictCheck):

    def check(self, langdict):
        print("Checking for infobox existence")
        validibs = ["infobox_software", "infobox_programming_language", "infobox_file_format",
                    "infobox_technology_standard", "infobox_software_license", "infobox"]
        for cl in langdict:
            if "DbpediaInfoboxTemplate" not in langdict[cl]:
                langdict[cl]["negativeSeed"] = 0
                continue
            ibs = langdict[cl]["DbpediaInfoboxTemplate"]
            langdict[cl]["MultiInfobox"] = len(ibs)
            langdict[cl]["Infobox programming language"] = int("infobox_programming_language" in ibs)
            langdict[cl]["Infobox software"] = int("infobox_software" in ibs)
            langdict[cl]["Infobox file format"] = int("infobox_file_format" in ibs)
            langdict[cl]["negativeSeed"] = int(not any(ib in ibs for ib in validibs) and bool(ibs))
        return langdict


if __name__ == "__main__":
    InfoboxDbEx().solo()
