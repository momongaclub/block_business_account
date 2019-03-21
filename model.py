import argparse
import numpy as np
import tensorflow
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Embedding
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


class Embeddings():

    def __init__(self):
        self.vectors = []
        self.embeddings = {}
        self.sentences = []
        self.train_data = []
        self.x_train = np.random.random((100, 100))
        self.y_train = np.random.randint(100, size=(270, 2))
        self.x_test = None
        self.y_test = None
        self.epochs = 800
        self.max_length = -1
        self.embedding_size = None
        self.word_num = None
        self.train_data_num = 0

    def load_training_data(self, training_data):
        # TODO split x,y data
        with open(training_data, 'r') as fp:
            for sentence in fp:
                sentence = sentence.rstrip('\n')
                sentence = sentence.split(' ')
                self.sentences.append(sentence)
                sentence_length = len(sentence)
                if sentence_length >= self.max_length:
                    self.max_length = sentence_length
                self.train_data_num += 1

    def load_embeddings(self, embeddings_data):
        with open(embeddings_data, 'r') as fp:
            line = fp.readline()
            self.word_num, self.embedding_size = line.split(' ')
            for embedding in fp:
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
            self.train_data.append(vector)

    def sentences2index(self):
        for sentence in self.sentences:
            vector = []
            for word in sentence:
                word = 1
                vector.append(word)
            self.train_data.append(vector)

    def padding_vectors(self):
        vectors = []
        for vector in self.train_data:
            diff = self.max_length - len(vector)
            vector = vector + [0 for i in range(0,diff)]
            vectors.append(vector)
        self.train_data = np.array(vectors)


def main():
    args = parse()
    embeddings = Embeddings()
    embeddings.load_training_data(args.training_data)
    embeddings.load_embeddings(args.embeddings_data)
    #embeddings.sentences2embeddings()
    embeddings.sentences2index()
    embeddings.padding_vectors()

    print(embeddings.train_data_num)
    print(embeddings.embedding_size)

    bilstm_model = BILSTM_Model()
    bilstm_model.load_config(args.config_file)
    bilstm_model.load_model()
    bilstm_model.compile()

    bilstm_model.model.fit(embeddings.train_data, embeddings.y_train, epochs = embeddings.epochs)

if __name__ == '__main__':
    main()

