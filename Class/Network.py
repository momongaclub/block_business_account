import torch
import torch.nn as nn
import torch.nn.functional as F
import sys


class RNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, user_vec_dim):
        super(RNN, self).__init__()
        self.input2hidden = nn.Linear(input_dim + hidden_dim, hidden_dim)
        self.lstm = nn.LSTM(input_dim, hidden_dim)
        self.uservec2binary = nn.Linear(user_vec_dim, output_dim) # TODO hidden_dim * sentence_n

    def forward(self, input_, hidden):
        tweet_vecs = []
        for tweet_n in range(len(input_)):  # ツイート数回
            for sentence_n in range(len(input_[tweet_n])):  # 文長回
                word_vec = input_[tweet_n, sentence_n, :]
                combined = torch.cat((word_vec, hidden), dim=0)
                hidden = self.input2hidden(combined)
                hidden = torch.tanh(hidden)
            #L, _ = self.lstm(input_, hidden)
            #print(L)
            tweet_vec = hidden
            tweet_vecs.append(tweet_vec)
        user_vec = torch.cat(tweet_vecs)  # ユーザのツイートを集約したベクトル
        print(user_vec)
        output = self.uservec2binary(user_vec)
        #output = torch.sigmoid(output)  # TODO softmaxと検討
        #output = torch.nn.Softmax(output)  # TODO softmaxと検討
        return output


def main():
    input_dim = 100
    hidden_dim = 20
    output_dim = 2
    rnn = RNN(input_dim, hidden_dim, output_dim)


if __name__ == '__main__':
    main()
