import argparse
import torch
import torch.nn as nn

import Data
import Embeddings
import Network

def parser():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('x_data')
    argparser.add_argument('y_data')
    argparser.add_argument('embeddings')
    argparser.add_argument('epoch', type=int)
    args = argparser.parse_args()
    return args

def main():
    args = parser()
    data = Data.Train_data()
    data.load_data(args.x_data)
    embeddings = Embeddings.Embeddings()
    embeddings.load_embeddings(args.embeddings)
    data.train_data = embeddings.sentences2embeddings(data.train_data)
    data.train_data = torch.Tensor(data.train_data)
    tweets_size = len(data.train_data)
    tweet_sentence_size = len(data.train_data[0])
    print(data.train_data.size())
    y = torch.zeros(1) #TODO 正解データの持ち方
    input_dim = 100
    hidden_dim = 30
    output_dim = 1
    h0 = torch.zeros(hidden_dim)
    rnn = Network.RNN(input_dim, hidden_dim, output_dim)
    for epoch in range(args.epoch):
        #user回数分回す
        output = rnn.forward(data.train_data, h0)
        loss_function = nn.MSELoss()
        loss = loss_function(output, y)
        optimizer = torch.optim.SGD(rnn.parameters(), lr=1e-2, momentum=0.9)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print(loss.item())


if __name__ == '__main__':
    main()
