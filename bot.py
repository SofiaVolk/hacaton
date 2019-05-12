from gensim.models import KeyedVectors
import pandas as pd
import numpy as np
from annoy import AnnoyIndex

data = pd.read_pickle('./data/file.pkl')
w2v = KeyedVectors.load("./data/word2vec.model")
a = AnnoyIndex(300)
a.load('./data/annoy_15')


def ret_vect(x, pos):
    k = []
    for s in x:
        try:
            k.append(w2v.wv[s])
        except KeyError:
            continue
    if len(k) == 0:
        return 0
    else:
        return np.mean(k, axis=0) if pos else -np.mean(k, axis=0)


# def ret_news(x_pos, x_neg):
#     res_vec = ret_vect(x_pos, True) + ret_vect(x_neg, False)
#     if isinstance(res_vec, int):
#         return "Нет новостей"
#     best_index = a.get_nns_by_vector(res_vec, 1)[0]
#     tags = []
#     for i in data[best_index]['tokens_wo_upper']:
#         if len(i) != 0:
#             tags.append(i[0])
#     tags = '#' + '#'.join(tags)
#     return '\n'.join([tags, data[best_index]['text'][:4000], '...'])

def ret_news(word_tuple=None, index=None):
    if word_tuple:
        res_vec = ret_vect(word_tuple[0], True) + ret_vect(word_tuple[1], False)
        if isinstance(res_vec, int):
            return "Нет новостей", None
        indeces = a.get_nns_by_vector(res_vec, 2)[0]
        return print_new(indeces), indeces
    if index:
        new_index = a.get_nns_by_item(index, 2)[1]
        return print_new(new_index), new_index


# def ret_similar_news(index):
#     indeces = a.get_nns_by_item(index, 10)
#     return [print_new(index) for index in indeces]

def get_tags(x):
    tags = []
    for i in data[x]['tokens_wo_upper']:
        if len(i) != 0:
            tags.append(i[0])
    return '#' + '#'.join(tags)


def print_new(x):
    return '\n'.join([get_tags(x), data[x]['text'][:4000], '...'])


if __name__ == '__main__':
    print(ret_news([''], ['япония']))
