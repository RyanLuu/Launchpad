from bokeh.layouts import row
from bokeh.models import HoverTool
from bokeh.palettes import Category10
from bokeh.plotting import figure, output_file, show, ColumnDataSource
import cast
from collections import Counter
import numpy as np
import os
import pandas as pd
import parser
from sklearn.manifold import TSNE
import sys
import word2vec

if '-w' in sys.argv and '-l' in sys.argv:
  print('Use -l to analyze lines (default) or -w to analyze words.')
  sys.exit(1)

mode = 'lines'
if '-w' in sys.argv:
  mode = 'words'
  sys.argv.remove('-w')
if '-l' in sys.argv:
  mode = 'lines'
  sys.argv.remove('-l')


if len(sys.argv) < 2:
  print('Please specify a movie to parse.')
  sys.exit(1)

word2vec.load()

plots = []

for i in range(1, len(sys.argv)):
  arg = sys.argv[i]
  filename = arg + '.txt'

  script_data = parser.parse_script(filename)
  script_cast = cast.make_cast(script_data).filter(min_lines=20)

  freq = Counter(script_cast.all_words)

  plot = figure(title=arg.replace('-', ' '),
             tools='pan, wheel_zoom, box_zoom, reset',
             active_scroll='wheel_zoom')

  hover = HoverTool(tooltips='<div>@label</div>')
  plot.add_tools(hover)

  X = labels = np.array([])
  y = np.array([], dtype=np.int32)
  
  for j, c in enumerate(script_cast):
    if mode == 'lines':
      valid_lines = [line for line in c.lines if word2vec.is_valid(parser.line_to_words(line))]
      vectors = np.array([word2vec.sentence_vector(line) for line in valid_lines])
      labels = np.concatenate((labels, valid_lines))
    elif mode =='words':
      valid_words = [word for word in c.words if word2vec.is_valid(word)]
      vectors = np.array([word2vec.word_vector(word) for word in valid_words])
      labels = np.concatenate((labels, valid_words))
    else:
      sys.exit(1)
    
    if vectors.size:
      X = np.concatenate((X, vectors)) if X.size else vectors
      y = np.concatenate((y, [j] * vectors.shape[0]))
    
  feature_cols = ['d{}'.format(i) for i in range(X.shape[1])]

  df = pd.DataFrame(X, columns=feature_cols)
  df['char_index'] = y
  df['label'] = labels

  tsne = TSNE(n_components=2)
  X_embedded = tsne.fit_transform(df.loc[:,feature_cols].values)

  df['x-tsne'] = X_embedded[:, 0]
  df['y-tsne'] = X_embedded[:, 1]
  df['inv-freq'] = df['label'].map(lambda x: 1/freq[x])

  for i, c in enumerate(script_cast):
    source = ColumnDataSource(data=dict(df.loc[df['char_index'] == i, ['x-tsne', 'y-tsne', 'label', 'inv-freq']]))
    plot.circle(0, 0, color=Category10[10][i % 10], alpha=0.5, size=0, legend=c.name) # fixes legend
    plot.circle('x-tsne', 'y-tsne', color=Category10[10][i % 10], alpha='inv-freq', size=10, legend=c.name, source=source)

  plot.legend.location='bottom_right'
  plot.legend.click_policy='hide'
  plot.toolbar.autohide = True

  plots.append(plot)

os.makedirs('out/analysis/' + mode, exist_ok=True)
output_file(os.path.join('out/analysis/' + mode, '{}{}.html'.format(sys.argv[1], '+' + str(len(sys.argv)-2) if len(sys.argv) > 2 else '')), title='Analysis')
show(row(*plots))

