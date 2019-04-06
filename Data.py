import sys


class Train_data():

    def __init__(self):
        self.train_data = []

    def load_data(self, fname):
        with open(fname, 'r') as fp:
            for datum in fp:
                datum = datum.rstrip('\n')
                datum = datum.split(' ')
                self.train_data.append(datum)

    def __str__(self):
        return 'data:' + self.train_data[1]


class Tweets2vec(Train_data):
    
    def __init__(self):
        self.embeddings = {}

    def load_embedding(self, fname):
        with open(fname, 'r') as fp:
            embedding_info = fp.readline()
            embedding_info = embedding_info.split(' ')
            word_sum = embedding_info[0]
            embedding_dim = embedding_info[1]
            for embedding in fp:
                embedding = embedding.rstrip('\n')
                embedding = embedding.split(' ')
                word = embedding.pop(0)
                vec = embedding
                self.embeddings[word] = vec

    def tweets2vec(self):
        sentences = []
        for sentence in self.train_data:
            sentence = []
            for word in sentence:
                sentence.append(self.embeddings[word])
            sentences.append(sentence)
        self.train_data = sentences


def main():
    embeddings = Tweets2vec()
    embeddings.load_data(sys.argv[2])
    embeddings.load_embedding(sys.argv[1])
    embeddings.tweets2vec()


if __name__ == '__main__':
    main()
