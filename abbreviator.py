# coding: utf-8
from tokenizer import JumanTokenizer, MeCabTokenizer

class Abbreviator(object):

    def __init__(self):
        self._t = JumanTokenizer()
        self._t_neologd = MeCabTokenizer(sys_dic_path='/usr/local/lib/mecab/dic/mecab-ipadic-neologd')

    def abbreviate(self, str, min_filter=2, max_filter=4):

        if min_filter >= len(str):
            return [str]

        words = self._t.separate_words(str)

        # 1-gram + 2-gram
        words_list = [list(word) + n_gram(word, 2) for word in words]

        start = 0
        end = len(words_list) - 1
        words_list = [words + [""] if idx != start else words for (idx, words) in enumerate(words_list)]

        import itertools
        abbreviateds = list(itertools.product(*words_list))
        abbreviateds = ["".join(abbreviated) for abbreviated in abbreviateds]

        abbreviateds = list(filter(lambda x: max_filter >= len(x) >= min_filter, abbreviateds))
        abbreviateds = self.eval_abbreviates_by_neologd(abbreviateds)

        return abbreviateds

    def eval_abbreviates_by_neologd(self, abbreviateds, min_mora=3, max_mora=99):
        result_list = []

        for abbreviated in abbreviateds:
            if len(self._t_neologd.separate_words(abbreviated)) == 1 and min_mora <= len(self._t_neologd.yomi(abbreviated)) <= max_mora:

                result_list.append(abbreviated)

        return result_list


def n_gram(word, n):
    return [word[k: k + n] for k in range(len(word) - n + 1)]


if __name__ == '__main__':
    strs = ("短期大学", "関西国際空港", "経営財団", "伊豆急行", "逃げるは恥だが役に立つ", "慶應義塾大学")

    abbreviator = Abbreviator()
    result_list = [abbreviator.abbreviate(str) for str in strs]

    [print(result) for result in result_list]
