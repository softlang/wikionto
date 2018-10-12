import mwparserfromhell


def extract_names(text):
    brac_count = 0

    TOKEN = ""
    READING_NAME = False
    NAME = ""
    NAMES = []

    for c in text:
        if c == '{':
            brac_count += 1
            TOKEN = ""
        elif c == '}':
            brac_count -= 1
            TOKEN = ""
        elif c == ' ':
            if TOKEN.lower() == 'infobox' and brac_count % 2 == 0:
                READING_NAME = True
            elif READING_NAME:
                NAME += ' ' + TOKEN
            TOKEN = ""
        elif c == '\n':
            if TOKEN.lower() == 'infobox' and brac_count % 2 == 0:
                NAMES.append('infobox')
            elif READING_NAME:
                READING_NAME = False
                NAME += ' ' + TOKEN
                NAMES.append(('infobox' + NAME).lower().strip())
                NAME = ""
            TOKEN = ""
        # isalpha : is c a letter?
        elif not c.isalpha() and READING_NAME:
            READING_NAME = False
            NAMES.append(('infobox' + NAME).lower().strip())
            NAME = ""
            TOKEN = ""
        else:
            TOKEN += c
    return ', '.join(NAMES)


def mwparserfromhell_extract_names(text):
    try:
        wikicode = mwparserfromhell.parse(text)
    except:
        return "------Error text------\n" + text
    templates = wikicode.filter_templates(recursive=True)
    return ', '.join([t.name.lower().strip() for t in templates if 'infobox' in t.name.lower()])
