import argparse
import numpy as np
import tensorflow
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers.recurrent import LSTM

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
        # model.add(LSTM(units = N_HIDDEN,
        #                input_shape=(LENGTH_OF_SEQUENCE, N_IN)))
        self.model.add(Dense(units=int(self.configs['n_out'])))
        self.model.add(Activation('sigmoid'))

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


class Embeddings():

    def __init__(self):
        self.vectors = []
        self.embeddings = {}
        self.sentences = []
        self.x_train = np.random.random((100, 100))
        self.y_train = np.random.randint(100, size=(100, 100))
        self.x_test = None
        self.y_test = None

    def load_training_data(self, training_data):
        # TODO split x,y data
        with open(training_data, 'r') as fp:
            for sentence in fp:
                sentence = sentence.rstrip('\n')
                self.sentences.append(sentence)

    def load_embeddings(self, embeddings_data):
        with open(embeddings_data, 'r') as fp:
            for embedding in fp: # TODO pop(0)
                embedding = embedding.rstrip('\n')
                embedding = embedding.split(' ')
                word = embedding.pop(0)
                self.embeddings[word] = embedding

    def sentences2embeddings(self):
        for sentence in self.sentences:
            vector = []
            for word in sentence:
                if self.embeddings.get(word, None) is None:
                    word = '<unk>' #TODO unknown word process
                else:
                    word = self.embeddings[word]
                vector.append(word)
            self.vectors.append(vector)

    def split_data(self):
        return 0

    def embedding_zero(self):
        return 0


def main():
    args = parse()
    embeddings = Embeddings()
    embeddings.load_training_data(args.training_data)
    embeddings.load_embeddings(args.embeddings_data)
    embeddings.sentences2embeddings()

    bilstm_model = BILSTM_Model()
    bilstm_model.load_config(args.config_file)
    bilstm_model.load_model()
    bilstm_model.compile()

    bilstm_model.model.fit(embeddings.x_train, embeddings.y_train, epochs = 100)

if __name__ == '__main__':
    main()

