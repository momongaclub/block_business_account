import sys
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchtext
import spacy
import matplotlib.pyplot as plt
import MeCab

PATH = '../'
TRAIN = 'sample_data'
TEST = 'sample_data'
VALIDATION = 'sample_data'
FORMAT = 'tsv'
TRAIN_BATCH_SIZE = 64
VAL_BATCH_SIZE = 256
TEST_BATCH_SIZE = 16

SEP = ','


def tokenizer(text):
    preprocessed_texts = []
    texts = text.split(SEP)
    m = MeCab.Tagger("-Owakati")
    for text in texts:
        text = m.parse(text)
        text = text.rstrip('\n')
        preprocessed_texts.append(text)
    return preprocessed_texts

class Data():

    def __init__(self):
        # batch_first は [batch, x, x]のように一番最初にbatchの次元を持ってくる
        """
            self.name is string.
            self.id is string.
            self.description is short text written by japanese
            self.location is None or string.
        """
        self.name = torchtext.data.Field(batch_first=True, lower=True)
        self.id = torchtext.data.Field(batch_first=True, lower=True)
        self.description = torchtext.data.Field(batch_first=True)
        self.location = torchtext.data.Field(batch_first=True)
        self.url = torchtext.data.Field(batch_first=True)
        self.created_at = torchtext.data.Field(batch_first=True)
        self.followers_count = torchtext.data.Field(batch_first=True)
        self.friends_count = torchtext.data.Field(batch_first=True)
        self.favorites_count = torchtext.data.Field(batch_first=True)
        self.texts = torchtext.data.Field(tokenize=tokenizer, sequential=True, batch_first=True, lower=True)
        
        self.train_ds = 0
        self.val_ds = 0
        self.test_ds = 0
        self.train_iter = 0
        self.val_iter = 0
        self.test_iter = 0

    def make_dataset(self):
        self.train_ds, self.val_ds, self.test_ds = \
            torchtext.data.TabularDataset.splits(
                path=PATH, train=TRAIN, test=TEST,
                validation=VALIDATION, format=FORMAT,
                fields=[('Name', self.name), ('Id', self.id), ('Description', self.description),
                        ('Location', self.location), ('Url', self.url),
                        ('Created_at',self.created_at), ('Followers_cnt', self.followers_count),
                        ('Friends_cnt', self.friends_count),
                        ('Favorites_cnt', self.favorites_count), ('Texts', self.texts)
                        ])

    def make_vocab(self):
        # 3種類の辞書を作成,vectorsを指定すると事前学習した分散表現を読み込める
        self.texts.build_vocab(self.train_ds.Texts, self.val_ds.Texts,
                               self.test_ds.Texts,
                               vectors=torchtext.vocab.FastText(language="ja"))
        #                       vectors='../corpus/wiki_data.vec')
        #self.head.build_vocab(self.train_ds.Head, self.val_ds.Head,
        #                      self.test_ds.Head, vectors=torchtext.vocab.GloVe(name='6B', dim=300))
        #self.label.build_vocab(self.train_ds.Label,
        #                       self.val_ds.Label, self.test_ds.Label)

    def make_iter(self):
        self.train_iter, self.val_iter, self.test_iter = \
            torchtext.data.Iterator.splits(
                (self.train_ds, self.val_ds, self.test_ds), batch_sizes=(
                    TRAIN_BATCH_SIZE,
                    VAL_BATCH_SIZE,
                    TEST_BATCH_SIZE), repeat=False
                )


def main():
    data = Data()
    data.make_dataset()
    data.make_vocab()
    data.make_iter()


if __name__ == '__main__':
    main()
