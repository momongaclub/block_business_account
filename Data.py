import sys

UNK = '<unk>'


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
        Train_data.__init__(self)
        self.embeddings = {}

    def load_embedding(self, fname):
        with open(fname, 'r') as fp:
            embedding_info = fp.readline()
            embedding_info = embedding_info.split(' ')
            word_size = int(embedding_info[0])
            embedding_dim = int(embedding_info[1])
            self.embeddings[UNK] = [0.0 for i in range(0, embedding_dim)]
            for embedding in fp:
                embedding = embedding.rstrip('\n')
                embedding = embedding.split(' ')
                word = embedding.pop(0)
                vec = embedding
                self.embeddings[word] = vec

    def tweets2vec(self):
        sentences = []
        for sentence in self.train_data:
            words = []
            for word in sentence:
                word = self.embeddings.get(word, self.embeddings[UNK])
                words.append(word)
            sentences.append(words)
        self.train_data = sentences


def main():
    embeddings = Tweets2vec()
    embeddings.load_data(sys.argv[1])
    embeddings.load_embedding(sys.argv[2])
    embeddings.tweets2vec()


if __name__ == '__main__':
    main()
