import os
import re
import sys

default_regex = re.compile(r"\n[\t ]*([A-Z0-9'\- ]+[A-Z0-9'\-])(?: \(.+\))?\n(([\t ]+(?!\(|\s))?(?(3).*(?:\n\3[\t ]*\S+.*)*|[\t ]+\S+.*(?:\n[\t ]+\S+.*)*))")

def parse(filename, directory='scripts', regex=default_regex):
    with open(os.path.join(directory, filename)) as content_file:
        matches = re.finditer(regex, content_file.read())
        return [(m.group(1), re.sub('\(.+\)', '', re.sub('\s+', ' ', m.group(2)).strip())) for m in matches]
