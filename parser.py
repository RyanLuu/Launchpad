import os
import re
import sys
import unidecode

default_regex = re.compile(r"\n[\t ]*([A-Z0-9'\- ]+[A-Z0-9'\-])(?: \(.+\))?(?: \[.+\])?\n(([\t ]+(?!\(|\[|\s))?(?(3).*(?:\n\3[\t ]*\S+.*)*|[\t ]+\S+.*(?:\n[\t ]+\S+.*)*))")

def parse_script(filename, directory='scripts', regex=default_regex):
    with open(os.path.join(directory, filename)) as content_file:
        matches = re.finditer(regex, unidecode.unidecode(re.sub(u'u\0092', '\'', content_file.read())))
        return [(m.group(1), re.sub('\(.+\)|\[.+\]', '', re.sub('\s+', ' ', m.group(2)).strip())) for m in matches]

def line_to_words(line):
  
  return re.findall(r'\'?[\w]+(?:[\'\u2019-][\w]+)*\'?', line)

