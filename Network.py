import torch
import torch.nn as nn
import torch.nn.functional as F

n = 50
# 140の入力をn件
emb_word_num = 100
emb_dim = 100


input_dim = 100
h1_dim = 120
h2_dim = 2

input_size = 4
num_layers = 3

class Network(nn.Module):

    def __init__(self):
        super(Network, self).__init__()
        self.h1 = nn.Linear(input_dim, h1_dim)
        self.h2 = nn.Linear(h1_dim, h2_dim)

    def forward(self, input_):
        y1 = torch.tanh(self.h1(input_))
        y2 = torch.tanh(self.h2(y1))
        return y2

class Encoder(nn.Module):

    def __init__(self, input_size, hidden_size):
        super(Encoder, self).__init__()
        self.hidden_size = hidden_size
        self.h1 = nn.LSTM(input_size, hidden_size, num_layers)

    def forward(self, input_, hidden):
        output, hidden = self.h1(input_, hidden, 3)
        return output, hidden

    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size)


class RNN(nn.Module):

    def __init__(self, input_dim, hidden_dim, output_dim):
        super(RNN, self).__init__()
        self.input2hidden = nn.Linear(input_dim + hidden_dim, hidden_dim)
        self.uservec2binary = nn.Linear(1620, output_dim)

    def forward(self, input_, hidden):
        tweet_vecs = []
        for tweet_n in range(len(input_)): # ツイート数回
            for sentence_n in range(len(input_[tweet_n])):# 文長回
                word_vec = input_[tweet_n, sentence_n, :]
                combined = torch.cat((word_vec, hidden), dim=0)
                hidden = self.input2hidden(combined)
                hidden = torch.tanh(hidden)
            tweet_vec = hidden
            tweet_vecs.append(tweet_vec)
        user_vec = torch.cat(tweet_vecs)# ユーザのツイートを集約したベクトル
        print(user_vec)
        output = self.uservec2binary(user_vec)
        output = torch.sigmoid(output)
        return output


def main():
    net = Network()
    rnn = RNN(10, 10, 1)

if __name__ == '__main__':
    main()
