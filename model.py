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

N_IN = 100
N_HIDDEN = 100
N_OUT = 100
BATCH_SIZE = None
LENGTH_OF_SEQUENCE = 100


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file',
                         help = 'config_file have any parametors.')
    args = parser.parse_args()
    return args


def load_model():
    model = Sequential()
    #model.add(LSTM(units = N_HIDDEN, input_shape=(LENGTH_OF_SEQUENCE, N_IN)))
    model.add(Dense(units = N_OUT))
    model.add(Activation('sigmoid'))

    return model


def load_config_file(config_file):
    columm2value = {}
    with open(config_file, 'r') as fp:
        for line in fp:
            line = line.rstrip('\n')
            columm, value = line.split(' ')
            columm2value[columm] = value
    return columm2value



class Model():

    def __init__(self):
        self.n_in = 100
        self.n_hidden = 100
        self.n_out = 100
        self.length_of_sequence = 10
        self.batch_size = 10
        self.model = load_model()


    def load_training_data(self):
        return 0


    def load_config_file(self):
        return 0


def main():
    args = parse()
    config__file = load_config_file(args.config_file)
    model = Model()

    model.model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    x_train = np.random.random((100, 100))
    y_train = np.random.randint(100, size=(100, 100))

    model.model.fit(x_train, y_train)

if __name__ == '__main__':
    main()
