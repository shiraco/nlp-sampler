# coding: utf-8

import unicodedata


def normalize(str):
    return lowercase(unicodedata.normalize('NFKC', str))


def lowercase(str):
    return str.lower()


def remove_stopword(str):
    pass


def katakana_hyphen_stemmer(str):
    pass


if __name__ == '__main__':
    str = "はじめましてﾜﾀｼﾊ JACK ＳＭＩＴＨです。"
    print("before: {}".format(str))
    normalized_str = normalize(str)
    print("after : {}".format(normalized_str))
