from check.langdictcheck import LangdictCheck


class InfoboxDbEx(LangdictCheck):

    def check(self,langdict):
        print("Checking for infobox existence")
        for cl in langdict:
            langdict[cl]["MultiInfobox"] = 0
            langdict[cl]["Infobox programming language"] = 0
            langdict[cl]["Infobox software"] = 0
            langdict[cl]["Infobox file format"] = 0
            ibs = langdict[cl]["DbpediaInfoboxTemplate"]
            if len(ibs)>1:
                langdict[cl]["MultiInfobox"] = 1
            if "Infobox_software" in ibs:
                langdict[cl]["Infobox software"] = 1
            if "Infobox_programming_language" in ibs:
                langdict[cl]["Infobox programming language"] = 1
            if "Infobox_file_format" in ibs:
                langdict[cl]["Infobox file format"] = 1
        return langdict

if __name__ == "__main__":
    InfoboxDbEx().solo()
