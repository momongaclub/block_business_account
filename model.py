import argparse
import numpy as np
import tensorflow
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Embedding
from keras.layers.recurrent import LSTM

import Data

"""
input: vector of sentence writtenby japanese
output: binary value.
"""


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='config_file have any parametors.')
    parser.add_argument('training_data', help='To training_data')
    parser.add_argument('embeddings_data', help='To embeedings_data')
    args = parser.parse_args()
    return args


class BILSTM_Model():

    def __init__(self):
        self.model = None
        self.length_of_sequence = 10
        self.batch_size = 10
        self.configs = {}

    def load_model(self):
        self.model = Sequential()
        #self.model.add(Embedding(input_dim=1000, output_dim=1000,
        #                         input_length=100, mask_zero=True))
        #self.model.add(LSTM(units = 100,input_shape=(270, 94)))
        self.model.add(Dense(units=int(self.configs['n_out'])))
        self.model.add(Activation('softmax'))

    def load_config(self, config_file):
        with open(config_file, 'r') as fp:
            for line in fp:
                line = line.rstrip('\n')
                name, value = line.split(':')
                self.configs[name] = value

    def compile(self):
        self.model.compile(loss=self.configs['loss'],
                           optimizer=self.configs['optimizer'],
                           metrics=[self.configs['metrics']])


def main():
    args = parse()
    #embeddings = Embeddings()
    #embeddings.load_training_data(args.training_data)
    #embeddings.load_embeddings(args.embeddings_data)
    #embeddings.sentences2embeddings()
    #embeddings.sentences2index()
    #embeddings.padding_vectors()

    embeddings = Data.Tweets2vec()
    embeddings.load_data(args.training_data)
    embeddings.load_embedding(args.embeddings_data)
    embeddings.tweets2vec()

    bilstm_model = BILSTM_Model()
    bilstm_model.load_config(args.config_file)
    bilstm_model.load_model()
    bilstm_model.compile()

    bilstm_model.model.fit(embeddings.train_data, embeddings.y_train, epochs = 100)

if __name__ == '__main__':
    main()

