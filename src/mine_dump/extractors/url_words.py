import re


def extract_urlpattern(title):
    tag = ''
    rest = title
    if '(' in title:
        tag = title.split('(')[1].split(')')[0]
        rest = title.split('(')[0]
    words = rest.lower()
    words = re.sub(r'[^\w]', ' ', words)
    words = [w.strip() for w in words.split('_')]
    if tag:
        words += [tag]
    return ', '.join(words)
