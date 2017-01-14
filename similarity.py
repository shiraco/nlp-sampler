# encoding: utf-8
from abc import ABCMeta, abstractmethod
import Levenshtein
import difflib


class CoOccurrence(metaclass=ABCMeta):

    @abstractmethod
    def calculate(self, token_list_x, token_list_y):
        raise NotImplementedError("This method must be implemented.")

    def unique(self, token_list_x, token_list_y):
        x = set(list(token_list_x))
        y = set(list(token_list_y))
        return x, y

    def count(self, token_list):
        token_dict = {}
        for token in token_list:
            if token in token_dict:
                token_dict[token]  = 1
            else:
                token_dict[token] = 1
        return token_dict


class Jaccard(CoOccurrence):

    def calculate(self, token_list_x, token_list_y):
        x, y = self.unique(token_list_x, token_list_y)
        try:
            result = len(x & y) / len(x | y)
        except ZeroDivisionError:
            result = 0.0
        return result


class Simpson(CoOccurrence):

    def calculate(self, token_list_x, token_list_y):
        x, y = self.unique(token_list_x, token_list_y)
        try:
            result = len(x & y) / float(min(map(len, (x, y))))
        except ZeroDivisionError:
            result = 0.0
        return result


def editdistance(str1, str2):
    return Levenshtein.distance(str1, str2)


def jaro_winkler(str1, str2):
    return Levenshtein.jaro_winkler(str1, str2)


def seq_match(str1, str2):
    return difflib.SequenceMatcher(None, str1, str2).ratio()


if __name__ == '__main__':
    from collections import namedtuple

    s = namedtuple("Token", "origin, token_ipa, token_neologd")

    s.origin = "逃げるは恥だが役に立つ"
    s.token_ipa = ["逃げる", "は", "恥", "だ", "が", "役に立つ"]
    s.token_neologd = ["逃げるは恥だが役に立つ"]

    tokens = []

    token = namedtuple("Token", "origin, token_ipa, token_neologd")
    token.origin = "逃げるは恥だが役に立つ"
    token.token_ipa = ["逃げる", "は", "恥", "だ", "が", "役に立つ"]
    token.token_neologd = ["逃げるは恥だが役に立つ"]
    tokens.append(token)

    token = namedtuple("Token", "origin, token_ipa, token_neologd")
    token.origin = "逃げるははじだが役に立つ"
    token.token_ipa = ["逃げる", "は", "はじ", "だ", "が", "役に立つ"]
    token.token_neologd = ["逃げる", "は", "はじ", "だ", "が", "役に立つ"]
    tokens.append(token)

    token = namedtuple("Token", "origin, token_ipa, token_neologd")
    token.origin = "逃げるは聡だが役に立つ"
    token.token_ipa = ["逃げる", "は", "聡", "だ", "が", "役に立つ"]
    token.token_neologd = ["逃げる", "は", "聡", "だ", "が", "役に立つ"]
    tokens.append(token)

    token = namedtuple("Token", "origin, token_ipa, token_neologd")
    token.origin = "逃げ恥"
    token.token_ipa = ["逃げ", "恥"]
    token.token_neologd = ["逃げ恥"]
    tokens.append(token)

    token = namedtuple("Token", "origin, token_ipa, token_neologd")
    token.origin = "明日結婚します"
    token.token_ipa = ["明日", "結婚", "し", "ます"]
    token.token_neologd = ["明日", "結婚", "し", "ます"]
    tokens.append(token)

    print("s: {}".format(s.origin))

    jaccard = Jaccard()
    simpson = Simpson()

    print("\t\t\t\tlev\tjaro\tseq\tjac\tjac_neo\tsim\tsim_neo")

    for token in tokens:
        jac = jaccard.calculate(s.token_ipa, token.token_ipa)
        sim = simpson.calculate(s.token_ipa, token.token_ipa)
        jac_neo = jaccard.calculate(s.token_neologd, token.token_neologd)
        sim_neo = simpson.calculate(s.token_neologd, token.token_neologd)
        lev = editdistance(s.origin, token.origin)
        jaro = jaro_winkler(s.origin, token.origin)
        seq = seq_match(s.origin, token.origin)

        print("{0}\t{1:.3f}\t{2:.3f}\t{3:.3f}\t{4:.3f}\t{5:.3f}\t{6:.3f}\t{7:.3f}".format(token.origin.rjust(15, '　'), lev, jaro, seq, jac, jac_neo, sim, sim_neo))
