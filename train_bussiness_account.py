import argparse
import numpy as np
import tensorflow
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers.recurrent import LSTM

import model

def main():
    m = model.BILSTM_Model()

if __name__ == '__main__':
    main()
