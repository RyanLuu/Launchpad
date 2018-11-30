from bokeh.layouts import row
from bokeh.palettes import viridis
from bokeh.plotting import figure, output_file, show, ColumnDataSource
import cast
import math
import parser
import sys

if len(sys.argv) < 2:
  print('Please specify a movie to parse.')
  sys.exit(1)

plots = []

for i in range(1, len(sys.argv)):
  arg = sys.argv[i]
  filename = arg + '.txt'

  script_data = parser.parse_script(filename)
  script_cast = cast.make_cast(script_data).filter(min_lines=20)

  plot = figure(title=arg.replace('-', ' '),
             tools='hover, pan, wheel_zoom, box_zoom, reset',
             tooltips=[('name', '@name'), ('lines', '@lines')])
 
  source = ColumnDataSource(data=dict(
    name = [c.name for c in script_cast],
    wpL = [c.average_wpL for c in script_cast],
    lpw = [c.average_lpw for c in script_cast],
    lines = [len(c.lines) for c in script_cast],
    size = [4*math.sqrt(len(c.lines)) for c in script_cast],
    color = [viridis(26)[ord(c.name[0].lower()) - 97] for c in script_cast]
  ))
  plot.circle('wpL', 'lpw', color='color', source=source, alpha=0.2, size='size')
  
  plot.xaxis.axis_label = 'Words per Line'
  plot.yaxis.axis_label = 'Letters per Word'

  plots.append(plot)

output_file('complexity.html', title='Complexity')
show(row(*plots))
