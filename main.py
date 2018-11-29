from bokeh.layouts import row
from bokeh.models import HoverTool
from bokeh.palettes import Category10
from bokeh.plotting import figure, output_file, show, ColumnDataSource
import cast
import numpy as np
import pandas as pd
import parser
from sklearn.manifold import TSNE
import sys
import word2vec

if len(sys.argv) < 2:
  print('Please specify a movie to parse.')
  sys.exit(1)

word2vec.load()

plots = []

for i in range(1, len(sys.argv)):
  arg = sys.argv[i]
  filename = arg + '.txt'

  script_data = parser.parse_script(filename)
  script_cast = cast.make_cast(script_data)
  script_cast.filter(min_lines=20)

  plot = figure(title=arg.replace('-', ' '),
             tools='pan, wheel_zoom, box_zoom, reset')
 
  hover = HoverTool(tooltips='<div>@label</div>')
  plot.add_tools(hover)

  X = labels = np.array([])
  y = np.array([], dtype=np.int32)
  
  if True:
    for i, c in enumerate(script_cast):
      vectors = np.array([word2vec.sentence_vector(line) for line in c.lines])
      X = np.concatenate((X, vectors)) if X.size else vectors
      y = np.concatenate((y, [i] * vectors.shape[0]))
      labels = np.concatenate((labels, c.lines))

  else:
    words = np.array([])
    for i, c in enumerate(script_cast):
      valid_words = [word for word in c.words if word2vec.is_valid(word)]
      vectors = np.array([word2vec.word_vector(word) for word in valid_words])
      X = np.concatenate((X, vectors)) if X.size else vectors
      y = np.concatenate((y, [i] * vectors.shape[0]))
      labels = np.concatenate((labels, valid_words))
    

  feature_cols = ['d{}'.format(i) for i in range(X.shape[1])]

  df = pd.DataFrame(X, columns=feature_cols)
  df['char_index'] = y
  df['label'] = labels

  tsne = TSNE(n_components=2)
  X_embedded = tsne.fit_transform(df.loc[:,feature_cols].values)

  df['x-tsne'] = X_embedded[:, 0]
  df['y-tsne'] = X_embedded[:, 1]

  for i, c in enumerate(script_cast):
    source = ColumnDataSource(data=dict(df.loc[df['char_index'] == i, ['x-tsne', 'y-tsne', 'label']]))
    plot.circle('x-tsne', 'y-tsne', color=Category10[10][i % 10], alpha=0.2, size=10, legend=c.name, source=source)

  plot.legend.location='bottom_right'
  plot.legend.click_policy='hide'

  plots.append(plot)

output_file('vocab.html', title='tSNE')
show(row(*plots))

