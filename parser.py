from bokeh.plotting import figure, show, output_file, ColumnDataSource
import os
import re
import sys
import math
sys.path.append(sys.path[0])
from cast import Cast
#import pandas as pd

SCRIPTS_DIR = 'scripts'

SCRIPT_NAME = sys.argv[1] if len(sys.argv) == 2 else 'Batman'

default_regex = re.compile(r"\n[\t ]*([A-Z0-9'\- ]+[A-Z0-9'\-])(?: \(.+\))?\n(([\t ]+(?!\(|\s))?(?(3).*(?:\n\3.*)*|[\t ]+.*(?:\n[\t ]+.*)*))")

def parse(filepath, regex=default_regex):
    with open(os.path.join(SCRIPTS_DIR, filepath)) as content_file:
        matches = re.finditer(regex, content_file.read())
        return [(m.group(1), re.sub('\(.+\)', '', re.sub('\s+', ' ', m.group(2)).strip())) for m in matches]

def to_cast(cl_table):
    cast = Cast()
    for cl in cl_table:
        if cl[0] not in cast:
            cast += cl[0]
        cast.get_character(cl[0]).add_line(cl[1])
    return cast

filename = SCRIPT_NAME + '.txt'
data = parse(filename)
cast = to_cast(data)

source = ColumnDataSource(data=dict(
    x=[c.average_wpL for c in cast],
    y=[c.average_lpw for c in cast],
    num_lines = [len(c.lines) for c in cast],
    alpha = [len(c.lines) / max([len(x.lines) for x in cast]) for c in cast],
    size = [16 * math.sqrt(len(c.lines) / max([len(x.lines) for x in cast])) for c in cast],
    name=[c.name for c in cast]
))

p = figure(title="My Plot",
           tools="hover, pan, wheel_zoom, box_zoom, reset",
           tooltips=[('name', '@name'), ('n_lines', '@num_lines'), ('avg_line_length', '@x'), ('avg_word_length', '@y')])

p.xaxis.axis_label = "Average Line Length (words)"
p.yaxis.axis_label = "Average Word Length (chars)"

p.circle('x', 'y', fill_alpha='alpha', size='size', source=source)

output_file(SCRIPT_NAME + '.html', title=SCRIPT_NAME)
show(p)
