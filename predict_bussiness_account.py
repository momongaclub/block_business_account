import argparse
import numpy as np
import tensorflow
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers.recurrent import LSTM
import model


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='config_file have any parametors.')
    parser.add_argument('training_data', help='To training_data')
    parser.add_argument('embeddings_data', help='To embeedings_data')
    args = parser.parse_args()
    return args

def main():
    args = parse()
    embeddings = model.Embeddings()
    embeddings.load_training_data(args.training_data)
    embeddings.load_embeddings(args.embeddings_data)
    embeddings.sentences2embeddings()

    bilstm_model = model.BILSTM_Model()
    bilstm_model.load_config(args.config_file)
    bilstm_model.load_model()
    bilstm_model.compile()

    bilstm_model.model.fit(embeddings.x_train, embeddings.y_train, epochs=80000, batch_size=100)



if __name__ == '__main__':
    main()
