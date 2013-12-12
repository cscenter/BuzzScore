#! /usr/bin/env python
# coding: utf8

import sys
import itertools as itt

import pymorphy2 as pm2
from pymorphy2.tagset import OpencorporaTag as Tag
import graph_tool.all as gt
from nltk.tokenize import wordpunct_tokenize


STATIC = [(u'NOUN', u'NPRO'),
          (u'NOUN', u'NOUN'),
          (u'VERB', u'INFN'),
          (u'VERB', u'COMP'),
          (u'VERB', u'GRND'),
          (u'VERB', u'ADVB'),
          (u'INFN', u'COMP'),
          (u'INFN', u'GRND'),
          (u'INFN', u'ADVB')]
STATIC = set(tuple(sorted(p)) for p in STATIC)

MORPH_ANALYZER = pm2.MorphAnalyzer()

KEYWORD_TAG = Tag('NOUN')


def is_connectable(p1, p2):
    if p2 == KEYWORD_TAG:
        p1, p2 = p2, p1
    if p1 == KEYWORD_TAG and p2.POS == 'INTJ':
        return True

    if tuple(sorted((p1.POS, p2.POS))) in STATIC:
        return True

    if p2.POS == 'VERB':
        p1, p2 = p2, p1
    if p1.POS == 'VERB':
        return p1.gender == p2.gender and p1.number == p2.number

    if p2.POS in ('NOUN', 'NPRO'):
        p1, p2 = p2, p1
    if p1.POS in ('NOUN', 'NPRO'):
        if p2.POS in ('ADJF', 'ADJS'):
            return p1.case == p2.case and p1.number == p2.number \
                   and p1.gender == p2.gender
        if p2.POS in ('PRTF', 'PRTS'):
            return p1.gender == p2.gender and p1.number == p2.number

    return False


def calc_weight(pu, pv, x1, x2, size):
    weight = 0.0
    for x in pu:
        for y in pv:
            if not is_connectable(x[0], y[0]):
                continue
            weight = max(weight, x[1] * y[1])
    dist = (1.0 - abs(x1 - x2 + 0.0) / size) ** 2
    weight = 1.0 - weight * dist
    assert(weight > 0)
    return weight


NEGS = [u'не', u'ни']

STOPWORDS = [u'и', u'в', u'во', u'что', u'на', u'с', u'со', u'как', u'а',
             u'то', u'так', u'но', u'к', u'у', u'же', u'за', u'бы', u'по',
             u'вот', u'от', u'о', u'из', u'ну', u'ли', u'если', u'уже', u'или',
             u'до', u'нибудь', u'уж', u'ведь', u'где', u'для', u'чем', u'чтоб',
             u'чего', u'под', u'ж', u'кто', u'потому', u'чтобы', u'куда',
             u'при', u'об', u'после', u'над', u'тот', u'эти', u'про', u'перед'] 

def tokenize(text, keyword):
    text = u' '.join(wordpunct_tokenize(text.lower()))
    keyword = u' '.join(wordpunct_tokenize(keyword.lower()))
    big_tokens = []
    while text:
        tkn, kw, text = text.partition(keyword)
        big_tokens.extend((tkn, kw))
    tokens = []
    for tkn in big_tokens:
        if tkn == keyword:
            tokens.append(keyword)
        else:
            tokens.extend(wordpunct_tokenize(tkn))
    check = lambda w: (w == keyword or w.isalpha()) and not w in STOPWORDS
    tokens = filter(check, tokens)
    for i in xrange(1, len(tokens)):
        if tokens[i - 1] in NEGS:
            tokens[i] = tokens[i - 1] + u' ' + tokens[i]
            tokens[i - 1] = None
    tokens = filter(None, tokens)
    return tokens, (keyword if keyword in big_tokens else None)


def parse(word, keyword):
    if word == keyword:
        return [(KEYWORD_TAG, 1.0)]
    parts = word.split()
    word = parts[1] if len(parts) > 1 else word
    return [(p.tag, p.estimate) for p in MORPH_ANALYZER.parse(word)]


def create_mst(words, keyword):
    size = len(words)
    parses = [parse(w, keyword) for w in words]

    graph = gt.Graph(directed=False)
    vertices = list(graph.add_vertex(size))
    words_vp = graph.new_vertex_property('string')
    for v, w in itt.izip(vertices, words):
        words_vp[v] = w.encode('utf8')
    graph.vp['words'] = words_vp
    root = vertices[words.index(keyword)]

    weights_ep = graph.new_edge_property('double')
    vp1 = itt.izip(vertices, parses)
    for i, (u, pu) in enumerate(vp1):
        vp2 = itt.islice(itt.izip(vertices, parses), i + 1, size)
        for j, (v, pv) in enumerate(vp2):
            e = graph.add_edge(u, v)
            weights_ep[e] = calc_weight(pu, pv, i, i + j + 1, size)
    graph.ep['weights'] = weights_ep

    mst = gt.min_spanning_tree(graph, root=root, weights=weights_ep)
    graph.set_edge_filter(mst)
    return (graph, root)


EPSILON = 10.0 ** -7

def calc_weights(text, keyword):
    words, keyword = tokenize(text, keyword)
    if not keyword:
        return dict(itt.izip(words, itt.cycle((1.0,))))

    mst, root = create_mst(words, keyword)
    weights_vp = mst.new_vertex_property('double')
    weights_vp[root] = 1.0

    class Visitor(gt.DFSVisitor):
        def __init__(self, w_vp, w_ep):
            self.w_vp = w_vp
            self.w_ep = w_ep
        def examine_edge(self, e):
            s, t = e.source(), e.target()
            if not self.w_vp[t]:
                self.w_vp[t] = self.w_vp[s] * (1.0 - self.w_ep[e])
    gt.dfs_search(mst, root, Visitor(weights_vp, mst.ep['weights']))

    words_vp = mst.vp['words']
    weights = dict((words_vp[v], weights_vp[v]) for v in mst.vertices())
    min_w = min(itt.ifilter(lambda x: x > 0, weights.values())) ** 1.5
    for w in weights.keys():
        if weights[w] <= EPSILON:
            weights[w] = min_w
    return weights


def main(text, keyword):
    words, keyword = tokenize(text, keyword)
    print u' | '.join(words)

    mst, root = create_mst(words, keyword)
    weights_str_ep = mst.new_edge_property('string')
    weights_ep = mst.ep['weights']
    for e in mst.edges():
        weights_str_ep[e] = str(weights_ep[e])
    gt.graph_draw(mst,
                  vertex_text=mst.vp['words'],
                  edge_text=weights_str_ep,
                  output_size=(1111, 1111),
                  output='mst.png')


if __name__ == '__main__':
    text = sys.stdin.read().strip().decode('utf8')
    keyword = sys.argv[1].decode('utf8')
    main(text, keyword)
    print '\n'.join('(%s: %f)' % (k, v)
                     for k, v in calc_weights(text, keyword).items())
