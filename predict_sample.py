from Class import Data
from Class import Model

import sys
import argparse
import torch
import torch.nn as nn
from sklearn.metrics import classification_report
import torchtext


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
    vocab_vectors = torchtext.vocab.Vectors(name = './corpus/entity_vector.model.txt')
    data_set.make_vocab(vocab_vectors)
    data_set.make_iter()

    vocab_size = data_set.texts.vocab.vectors.size()[0]
    embedd_dim = data_set.texts.vocab.vectors.size()[1]
    hidden_dim = 4
    vocab_vectors = data_set.texts.vocab.vectors

    rnn = Model.simplernn(embedd_dim, hidden_dim, vocab_size, vocab_vectors)
    # パラメータの読み込み
    parameter = torch.load('./model_weight/model1.pt',
                           map_location=torch.device(device))
    rnn.load_state_dict(parameter)

    # 評価モードに変更
    rnn = rnn.eval()
    rnn.to(device)

    losses = []
    batch_sizes = []

    pred = []
    Y = []

    cnt = 0
    sum_ = 0

    batch_len = 0
    data_len = len(data_set.train_iter)

    for batch in iter(data_set.train_iter):

        concat_vec = rnn.concat_input(batch)
        input_texts = batch.Texts
        input_texts = input_texts.to(device)
        input_ = concat_vec
        input_ = input_.to(device)
        target = batch.Favorites_cnt # label
        # torch.eye(クラス数)[対象tensor]でonehotへ
        # target = torch.eye(6, dtype=torch.long)[target]
        target = target.squeeze()  # 次元変換
        # print(target)
        target = target.to(device)
        output_texts = rnn.text_forward(input_texts)
        output_texts = output_texts.squeeze()  # 次元変換
        input_ = torch.cat((input_, output_texts), 1) # add
        output_ = rnn.forward(input_)
        output_ = output_.squeeze()  # 次元変換
        batch_outputs = output_
        #print('batch_len', batch_len, '/', 'data_len', data_len)
        # print('predict', batch_outputs.argmax(), 'target', target)
        for output in batch_outputs:
            p = int(output.argmax())
            pred.append(p)

        Y += [int(t) for t in target]
        print('output_len', len(pred), 'target_len', len(Y))
        batch_sizes.append(batch_len)
        batch_len = batch_len + 1

    print(classification_report(Y, pred))
    """
    for p, t in zip(pred, Y):
        sum_ += 1
        if p == t:
            cnt += 1
    print(sum_, cnt)
    """


if __name__ == '__main__':
    main()
