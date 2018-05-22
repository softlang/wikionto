from check.langdictcheck import LangdictCheck

ex_properties = {"battery", "connectivity", "cpu", "display", "form", "input", "memory", "memoryCard", "networks",
                 "platform", "related", "slogan", "soc", "storage"}

in_properties = {"paradigm", "typing", "fileExt", "implementation"}


class InfoboxProp(LangdictCheck):

    def check(self, langdict):
        print("Checking Infobox properties")
        for cl in langdict:
            if "properties" not in langdict[cl]:
                langdict[cl]["DbpediaInfobox"] = -1
                continue
            for p in ex_properties:
                if p in langdict[cl]["properties"]:
                    langdict[cl]["DbpediaInfobox"] = 0
                    break
            for p in in_properties:
                if p in langdict[cl]["properties"]:
                    langdict[cl]["DbpediaInfobox"] = 1
                    break
        return langdict


if __name__=='__main__':
    InfoboxProp().solo()