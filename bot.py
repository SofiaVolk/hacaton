from gensim.models import KeyedVectors
import pandas as pd
import numpy as np
from annoy import AnnoyIndex

data = pd.read_pickle('/data/file.pkl')
w2v = KeyedVectors.load("/data/word2vec.model")
a = AnnoyIndex(300)
a.load('/data/annoy_15')


def ret_news(x):
    k = []
    c = 0
    for s in x:
        try:
            k.append(w2v.wv[s])
        except KeyError:
            c += 1
            k.append(np.array([0]*300))
    if len(k) == c:
        return "Cорян, нет похожих новостей"
    else:
        k = np.mean(k, axis=0)
        best_index = a.get_nns_by_vector(k, 1)[0]
        tags = []
        for i in data[best_index]['tokens_wo_upper']:
            if len(i) != 0:
                tags.append(i[0])
        tags = '#'+'#'.join(tags)
        return '\n'.join([tags, data[best_index]['text'][:4000], '...'])
