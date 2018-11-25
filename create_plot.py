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

p = figure(title='My tSNE',
           tools='hover, pan, wheel_zoom, box_zoom, reset',
           tooltips=[('word', '@words')])

for i in range(1, len(sys.argv)):
  arg = sys.argv[i]
  filename = arg + '.txt'

  script_data = parser.parse(filename)
  script_cast = cast.make_cast(script_data)
  script_cast.filter(min_lines=20)
  
  X = words = np.array([])
  y = np.array([], dtype=np.int32)

  for i, c in enumerate(script_cast):
    valid_words = [word for word in c.words if word2vec.is_valid(word)]
    vectors = np.array([word2vec.word_vector(word) for word in valid_words])
    X = np.concatenate((X, vectors)) if X.size else vectors
    y = np.concatenate((y, [i] * vectors.shape[0]))
    words = np.concatenate((words, valid_words))

  feature_cols = ['d{}'.format(i) for i in range(X.shape[1])]

  df = pd.DataFrame(X, columns=feature_cols)
  df['index'] = y
  df['word'] = words

  tsne = TSNE(n_components=2)
  X_embedded = tsne.fit_transform(df.loc[:,feature_cols].values)

  df['x-tsne'] = X_embedded[:, 0]
  df['y-tsne'] = X_embedded[:, 1]

  for i, c in enumerate(script_cast):
    rows = df.loc[df['index'] == i]
    source = ColumnDataSource(data=dict(
        x=rows.loc[:,'x-tsne'].values,
        y=rows.loc[:,'y-tsne'].values,
        words=rows.loc[:,'word'].values,
    ))

    p.circle('x', 'y', color=Category10[10][i % 10], alpha=0.2, size=10, legend=c.name, source=source)

p.legend.location='bottom_right'
p.legend.click_policy='hide'

output_file('vocab.html', title='tSNE')
show(p)
