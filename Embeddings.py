import sys
import torch

class Embeddings():

    def __init__(self):
        self.word2vec = {}

    def load_embeddings(self, fname):
        with open(fname, 'r') as fp:
            line = fp.readline()
            for line in fp:
                line = line.rstrip('\n')
                line = line.rstrip(' ')
                line = line.split(' ')
                word = line[0]
                vec = line[1::]
                vec_len = len(vec)
                for i in range(vec_len):
                    vec[i] = float(vec[i])
                self.word2vec[word] = vec
        return self.word2vec

    def sentences2embeddings(self, sentences):
        max_ = 50
        padding_vec = [[0.0 for i in range(100)] for j in range(200)]
        # padding_vec = torch.zeros(200, 100) # (n個, m要素)
        unk_vec = [float(0) for i in range(100)]
        embedded_sentences = []
        for sentence in sentences:
            embedded_sentence = []
            for word in sentence:
                word = self.word2vec.get(word, unk_vec)
                embedded_sentence.append(word)
            len_ = len(embedded_sentence)
            embedded_sentence = embedded_sentence + padding_vec[len_::]
            embedded_sentences.append(embedded_sentence)
        return embedded_sentences

def main():
    embeddings = Embeddings()
    embeddings.load_embeddings(sys.argv[1])
    for word, vec in embeddings.word2vec.items():
        print(word, vec)
        print('\n')

if __name__ == '__main__':
    main()
