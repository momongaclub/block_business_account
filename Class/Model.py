import sys
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np



def parse():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('embeddings', type=str, help='include four keys.')
    args = parser.parse_args()
    return args

class simplernn(nn.Module):
    def __init__(self, embedding_dim, hidden_dim, vocab_size, vocab_vectors, gpu=False, batch_first=True):
        """
        embedding_dim is dimention of vocab
        """
        # embedding_dimは分散表現の次元数,
        super(simplernn, self).__init__()
        self.gpu = gpu
        self.hidden_dim = hidden_dim
        self.embed = nn.Embedding(vocab_size, embedding_dim)
        self.embed.weight.data.copy_(vocab_vectors)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=batch_first)
        output_dim = 2
        self.linear1 = nn.Linear(hidden_dim, output_dim)
        self.linear2 = nn.Linear(hidden_dim, output_dim)
        #self.softmax = nn.LogSoftmax(dim=1) # TODO
        self.softmax = nn.LogSoftmax() # TODO

    def text_forward(self, sentence):
        # lstmの最初の入力に過去の隠れ層はないのでゼロベクトルを代入する
        # self.hidden = self.init_hidden(sentence.size(0))
        embed = self.embed(sentence)
        # print(embed)
        # h_outが最後の出力になる
        y, (h_out, c_out) = self.lstm(embed)
        h_out = torch.tanh(h_out)
        h_out = self.linear1(h_out)
        # y = self.linear1(y)
        # print('y', y)
        return h_out

    def forward(self, vec):
        y = self.linear2(vec)
        y = torch.tanh(y)
        # TODO テキストはembedしてその後 concat する？
        # それとも別ネットワークにして一回層噛ませるか。
        return y

def main():
    return 0


if __name__ == '__main__':
    main()
