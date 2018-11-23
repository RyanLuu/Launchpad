from bokeh.plotting import figure, show, output_file, ColumnDataSource
import cast
import gensim
import numpy as np
import parser
from sklearn.manifold import TSNE
import sys

model = gensim.models.KeyedVectors.load_word2vec_format('./model/GoogleNews-vectors-negative300.bin', binary=True)

def to_vectors(words):
  return [model.wv[word] for word in words if word in model.wv]

def average_vector(words):
  return np.mean(to_vectors(words), axis=0)

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
  script_cast.filter(min_lines=10)

  #for character in script_cast:
  character = script_cast[1]
  X = np.array(to_vectors(character.words))
  X_embedded = TSNE(n_components=2).fit_transform(X)

  source = ColumnDataSource(data=dict(
      x=X_embedded.T[0],
      y=X_embedded.T[1],
      words=[word for word in character.words if word in model.wv]
  ))

  p.circle('x', 'y', alpha=0.2, size=10, source=source)

output_file('vocab.html', title='tSNE')
show(p)
