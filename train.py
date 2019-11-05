import argparse
import torch
import torch.nn as nn

from Class import Data
from Class import Embeddings
from Class import Network


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
    data.load_Xdata(args.x_data)
    data.load_Ydata(args.y_data)

    embeddings = Embeddings.Embeddings()
    embeddings.load_embeddings(args.embeddings)
    data.train_data = embeddings.train_data2embeddings(data.train_data, 100)
    for user_id in range(len(data.train_data)):
        data.train_data[user_id] = torch.Tensor(data.train_data[user_id])
    y = data.train_Ydata
    y = torch.Tensor(y)
    #y = y.long()
    #y = torch.squeeze(y)
    print(y)
    input_dim = 100
    hidden_dim = 30
    output_dim = 1  # TODO 2
    h0 = torch.zeros(hidden_dim)
    rnn = Network.RNN(input_dim, hidden_dim, output_dim)
    for epoch in range(args.epoch):
        loss = 0
        for user_id in range(len(data.train_data)):  # batch_size
            output = rnn.forward(data.train_data[user_id], h0)
            loss_function = nn.MSELoss()
            #loss_function = nn.CrossEntropyLoss()
            print(output, y[user_id])
            loss += loss_function(output, y[user_id])
            #  loss = loss_function(output, y[user_id])
        optimizer = torch.optim.SGD(rnn.parameters(), lr=1e-2, momentum=0.9)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print('epoch:', epoch, 'loss:', loss.item())
    torch.save(rnn.state_dict(), 'model.pt')


if __name__ == '__main__':
    main()
