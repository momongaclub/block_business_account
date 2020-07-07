from Class import Data
from Class import Model

import sys
import argparse
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import torchtext


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('epochs')
    parser.add_argument('batch_size')
    parser.add_argument('lr')
    parser.add_argument('momentum')


def plot_progress(x_axis, y_axis, time=0.1):
    """
    x_axis and y_axis is list
    """
    plt.plot(x_axis, y_axis)
    plt.draw()
    plt.pause(time)
    plt.cla()


def main():

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)

    data_set = Data.Data()
    data_set.make_dataset()
    vocab_vectors = torchtext.vocab.Vectors(name='./corpus/entity_vector.model.txt')
    data_set.make_vocab(vocab_vectors)
    data_set.make_iter()
    vocab_size = data_set.texts.vocab.vectors.size()[0]
    embedd_dim = data_set.texts.vocab.vectors.size()[1]
    hidden_dim = 4
    text_hidden_dim = 4
    
    vocab_vectors = data_set.texts.vocab.vectors
    rnn = Model.simplernn(embedd_dim, hidden_dim, vocab_size, vocab_vectors)
    rnn.to(device)
    loss_function = nn.CrossEntropyLoss()  # softmaxを含む
    optimizer = torch.optim.SGD(rnn.parameters(), lr=0.001, momentum=0.9)

    losses = []
    batch_sizes = []
    epochs = []

    for epoch in range(20):
        data_len = len(data_set.train_iter)
        batch_len = 0
        for batch in iter(data_set.train_iter):
            batch_len = batch_len + 1
            concat_vec = rnn.concat_input(batch)
            input_texts = batch.Texts
            input_texts = input_texts.to(device)
            input_ = concat_vec
            input_ = input_.to(device)
            target = batch.Favorites_cnt # label
            target = target.squeeze()  # 次元変換
            target = target.to(device)
            optimizer.zero_grad()
            # 後使うべき入力 Name, Id, Descriptipn, Location, Url, Created_at,
            # concat_vec = torch.cat((batch.Name, batch.Id, batch.Url, batch.Created_at)
            output_texts = rnn.text_forward(input_texts)
            output_texts = output_texts.squeeze()  # 次元変換
            input_ = torch.cat((input_, output_texts), 1) # add
            print(input_.size())
            break
            output = rnn.forward(input_)
            output = output.squeeze()  # 次元変換
            loss = loss_function(output, target)
            loss.backward()
            optimizer.step()
            print('epoch:', epoch, 'batch_len', batch_len,
                  '/', data_len, 'loss:', loss.item())
            batch_sizes.append(batch_len + (epoch*16))
            losses.append(loss)
            plot_progress(batch_sizes, losses)
        torch.save(rnn.state_dict(), './model_weight/' 'model' + str(epoch) + '.pt')


if __name__ == '__main__':
    main()
