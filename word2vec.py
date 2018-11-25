import gensim

model = gensim.models.KeyedVectors.load_word2vec_format('./models/GoogleNews-vectors-negative300.bin', binary=True)

def is_valid(word):
  return word in model.wv

def word_vector(word):
  return model.wv[word]

def sentence_vector(words):
  words = [words for word in words if is_valid(word)]
  return [sum(i) for i in zip(*words)]

