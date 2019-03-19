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
    parser.add_argument('training_data',
                         help = 'training_data is wakati tweets')
    parser.add_argument('embeddings',
                         help = 'embedding made by fasttext')
    args = parser.parse_args()
    return args


def load_embedding(embedding):
    embeddings = []
    with open(embedding, 'r') as fp:
        for embedding in fp:
            print(embedding)
    return embeddings


def sentences2vectors(jpn_sentences):
    vectors = []
    with open(jpn_sentences, 'r') as fp:
        for jpn_sentence in jpn_sentences:
            # TODO embedding fasttext
            vector = jpn_sentence
            vectors.append(vector)
            #convert sentence2vetor
    return vectors


def main():
    args = parse()

    training_data = sentences2vectors(args.training_data)
    embeddings = load_embedding(args.embeddings)

    # embedding [mask_zero=True] after input

    model = Sequential()
    #model.add(LSTM(units = N_HIDDEN, input_shape=(LENGTH_OF_SEQUENCE, N_IN)))
    model.add(Dense(units = N_OUT))
    model.add(Activation('sigmoid'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    x_train = np.random.random((100, 100))
    y_train = np.random.randint(100, size=(100, 100))

    model.fit(x_train, y_train)

if __name__ == '__main__':
    main()
