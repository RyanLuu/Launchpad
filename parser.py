import collections
import os
import re
import sys

SCRIPTS_DIR = 'scripts'

default_regex = re.compile(r"\n[\t ]*([A-Z0-9'\- ]+[A-Z0-9'\-])(?: \(.+\))?\n(([\t ]+(?!\(|\s))?(?(3).*(?:\n\3.*)*|[\t ]+.*(?:\n[\t ]+.*)*))")

def parse(filepath, regex=default_regex):
    with open(os.path.join(SCRIPTS_DIR, filepath)) as content_file:
        matches = re.finditer(regex, content_file.read())
        return {(m.group(1), re.sub('\s+', ' ', m.group(2))) for m in matches}

filename = sys.argv[1] if len(sys.argv) == 2 else "Batman.txt"
data = parse(filename)

for d in data:
    print("{}:{}{}".format(d[0], " " * (16-len(d[0])), d[1][:84]))

n_lines = collections.Counter([x[0] for x in data])
n_lines = {c: n_lines[c] for c in n_lines if n_lines[c] >= 10}
print(n_lines)
