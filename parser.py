import collections
import os
import re

SCRIPTS_DIR = 'scripts'

default_regex = re.compile(r"\n[\t ]*([A-Z0-9'\- ]+[A-Z0-9'\-])(?: \(.+\))*[\t ]*\n([\t ]*)(.+\n(?:(?:\2).+\n)*)")

def parse(filepath, regex=default_regex):
    with open(os.path.join(SCRIPTS_DIR, filepath)) as content_file:
        matches = re.finditer(regex, content_file.read())
        return {(m.group(1), re.sub('\s+', ' ', m.group(3))) for m in matches}

data = parse("Badlands.txt")

for d in data:
    print("{}:{}{}".format(d[0], " " * (16-len(d[0])), d[1][:84]))

n_lines = collections.Counter([x[0] for x in data])
n_lines = {c: n_lines[c] for c in n_lines if n_lines[c] >= 10}
print(n_lines)
