ex_properties = {"recorded","artist","album","thisSingle","accessdate","fromAlbum","lastSingle","nextSingle",
                 "nosales","composer","streaming","writingCredits"
                 ,"thesisYear","workInstitutions","workplaces","thesisUrl","thesisTitle","species","spouse",
                 "battery"}

in_properties = {"paradigm", "typing", "fileExt", "implementation"}


def check_infobox(langdict):
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