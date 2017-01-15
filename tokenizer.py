# coding: utf-8
from collections import namedtuple

import MeCab
from pyknp import Juman

class MeCabTokenizer(object):

    def __init__(self, user_dic_path='', sys_dic_path=''):
        option = '-Ochasen'
        if user_dic_path:
            option += ' -u {0}'.format(user_dic_path)
        if sys_dic_path:
            option += ' -d {0}'.format(sys_dic_path)
        self._t = MeCab.Tagger(option)

    def separate_words(self, sent):
        words = [token.surface for token in self.tokenize(sent)]

        return words

    def yomi(self, sent):
        words = [token.reading for token in self.tokenize(sent)]
        result = "".join(words)

        return result

    def tokenize(self, sent):
        tokens = []
        self._t.parse('')  # for UnicodeDecodeError
        node = self._t.parseToNode(sent)

        while node:
            token = namedtuple('Token', 'surface, pos, pos_detail1, pos_detail2, pos_detail3,\
                                                     infl_type, infl_form, base_form, reading, phonetic')
            feature = node.feature.split(',')
            token.surface = node.surface    # 表層形
            token.pos = feature[0]          # 品詞
            token.pos_detail1 = feature[1]  # 品詞細分類1
            token.pos_detail2 = feature[2]  # 品詞細分類2
            token.pos_detail3 = feature[3]  # 品詞細分類3
            token.infl_type = feature[4]    # 活用型
            token.infl_form = feature[5]    # 活用形
            token.base_form = feature[6]    # 原型

            if len(feature) > 7:
                token.reading = feature[7]      # 読み
                token.phonetic = feature[8]     # 発音
            else:
                token.reading = ""
                token.phonetic = ""

            tokens.append(token) if token.pos != 'BOS/EOS' else None
            node = node.next

        return tokens

    def filter_by_pos(self, sent, pos='名詞'):
        tokens = [token for token in self.tokenize(sent) if token.pos == pos]

        return tokens


class JumanTokenizer(object):

    def __init__(self):
        self._t = Juman()

    def separate_words(self, sent):
        words = [token.midasi for token in self.tokenize(sent)]

        return words

    def tokenize(self, sent):
        tokens = []

        res = self._t.analysis(sent)

        for mrph in res.mrph_list():
            token = namedtuple('Token', 'midasi')
            token.midasi = mrph.midasi    # 表層形
            tokens.append(token)

        return tokens

if __name__ == '__main__':
    tokenizer = MeCabTokenizer()
    tokenizer_neologd = MeCabTokenizer(sys_dic_path='/usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    sent = "昨日の新垣結衣が出演していた逃げ恥を見逃した"
    # sent = "昨日のキムタクが出演していたドラマを見逃した"

    token = tokenizer.separate_words(sent)
    yomi = tokenizer.yomi(sent)
    print(token)
    print(yomi)

    token = tokenizer_neologd.separate_words(sent)
    yomi = tokenizer_neologd.yomi(sent)
    print(token)
    print(yomi)
