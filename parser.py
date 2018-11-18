from bokeh.plotting import figure, show, output_file
import collections
import os
import re
import sys
#import pandas as pd

SCRIPTS_DIR = 'scripts'

SCRIPT_NAME = sys.argv[1] if len(sys.argv) == 2 else 'Batman'

default_regex = re.compile(r"\n[\t ]*([A-Z0-9'\- ]+[A-Z0-9'\-])(?: \(.+\))?\n(([\t ]+(?!\(|\s))?(?(3).*(?:\n\3.*)*|[\t ]+.*(?:\n[\t ]+.*)*))")

def parse(filepath, regex=default_regex):
    with open(os.path.join(SCRIPTS_DIR, filepath)) as content_file:
        matches = re.finditer(regex, content_file.read())
        return {(m.group(1), re.sub('\(.+\)', '', re.sub('\s+', ' ', m.group(2)).strip())) for m in matches}

filename = SCRIPT_NAME + '.txt'
data = parse(filename)

#print(data)
chars = []
lines = []
words = []
for d in data:
    if d[0] not in chars:
        chars.append(d[0])
        lines.append([])
        words.append([])
    lines[chars.index(d[0])].append(d[1])
    words[chars.index(d[0])].extend(re.findall(r"\b[A-Za-z]+(?:[-'][A-Za-z]+)?\b", d[1]))
print(words[0])
print(lines[0])
#for d in data:
#    print("{}:{}{}".format(d[0], " " * (16-len(d[0])), d[1][:84]))

n_lines = collections.Counter([x[0] for x in data])
n_lines = {c: n_lines[c] for c in n_lines if n_lines[c] >= 10}
print(n_lines)

p = figure(title="My Plot",
           tools="hover")

p.xaxis.axis_label = "Average Line Length"
p.yaxis.axis_label = "Average Word Length"



output_file(SCRIPT_NAME + '.html', title=SCRIPT_NAME)
show(p)
