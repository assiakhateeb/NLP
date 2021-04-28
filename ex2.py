from sys import argv
from collections import defaultdict
from random import choices


class Ngrams:
    begin_token = "<BS>"
    end_token = "<ES>"

    def __init__(self, corpus):
        self.tokens_histogram = defaultdict(lambda: 0)
        self.bigrams_histogram = defaultdict(lambda: 0)
        self.trigrams_histogram = defaultdict(lambda: 0)
        self.corpus = corpus.lower()

        self.corpus = self.corpus.replace("\n", ' ' + Ngrams.end_token + ' ' + Ngrams.begin_token + ' ')

        self.ungiramP = []
        self.unigram_keys = []

        self.N = 0
        self.V = 0
        self.bigramsV = 0
        self.trigramsV = 0

    def get_unigrams(self):
        # print("~~~~~~~~~~ Unigrams ~~~~~~~~~~~~")
        tokens = self.corpus.split()

        for w in tokens:
            self.tokens_histogram[w] += 1

        self.N = len(tokens)  # the number of all tokens
        self.V = len(self.tokens_histogram)

        for w in self.tokens_histogram:
            self.ungiramP.append((self.tokens_histogram[w] + 1) / (self.N + self.V))
            self.unigram_keys.append(w)

    def get_unigrams_p(self, sentence):
        value = 1
        words = sentence.split()  # ['I', "don’t", 'think', 'so', '…']
        for token in words:
            if token not in self.tokens_histogram:
                value = value * (1 / (self.N + self.V))
            else:
                value = value * ((self.tokens_histogram[token] + 1) / (self.N + self.V))
        return value

    def generate_sentences_unigrams(self, count):
        res = ""
        for n in range(count):
            rand_s = ""
            word = choices(self.unigram_keys, self.ungiramP)
            while (word[0] != Ngrams.end_token):
                rand_s += word[0] + ' '
                word = choices(self.unigram_keys, self.ungiramP)
            res += rand_s + "\n"
        return res

    def bigrams(self):
        tokens = self.corpus.split()
        bigram_words = []
        for i in range(len(tokens) - 1):
            if tokens[i] != Ngrams.begin_token and tokens[i] != Ngrams.end_token:
                bigram_words.append(tokens[i] + ' ' + tokens[i + 1])

        for w in bigram_words:
            self.bigrams_histogram[w] += 1

        self.bigramsV = len(self.bigrams_histogram)

    def get_bigrams_p(self, sentence):
        sentences_split = []
        value = 1
        tokens = sentence.split()
        for i in range(len(tokens) - 1):
            sentences_split.append(tokens[i] + ' ' + tokens[i + 1])
        for token in sentences_split:
            w1_w2 = token.split()
            if token not in self.bigrams_histogram:
                if w1_w2[1] in self.tokens_histogram:
                    value = value * ((self.tokens_histogram[w1_w2[1]] + 1) / (self.N + self.V))
                else:
                    value = value * (1 / (self.N + self.V))
            else:
                value = value * (
                            (self.bigrams_histogram[token] + 1) / (self.tokens_histogram[w1_w2[0]] + self.bigramsV))
        return value

    def get_trigrams(self):
        tokens = self.corpus.split()
        trigram_words = []
        for i in range(len(tokens) - 2):
            if (tokens[i] != Ngrams.begin_token and tokens[i] != Ngrams.end_token):
                trigram_words.append(tokens[i] + ' ' + tokens[i + 1] + ' ' + tokens[i + 2])

        for w in trigram_words:
            self.trigrams_histogram[w] += 1

        self.trigramsV = len(self.trigrams_histogram)

    def get_trigrams_p(self, sentence):
        sentence_split = []
        prop = 1
        words = sentence.split()  # ['This', "is", 'the', 'best']
        for i in range(len(words) - 2):
            sentence_split.append(
                words[i] + ' ' + words[i + 1] + ' ' + words[i + 2])  # ['This is the' , ' is The best ]
        for token in sentence_split:
            w1_w2_w3 = token.split()
            if token not in self.trigrams_histogram:
                w1_w2 = w1_w2_w3[1] + " " + w1_w2_w3[2]
                if w1_w2 not in self.bigrams_histogram:
                    if w1_w2_w3[1] in self.tokens_histogram:
                        prop = prop * (0.5 * (self.tokens_histogram[w1_w2_w3[2]] + 1) / (self.N + self.V))
                    else:
                        prop = prop * (1 / (self.N + self.V))
                else:
                    b = (self.bigrams_histogram[w1_w2] + 1) / (self.tokens_histogram[w1_w2_w3[1]] + self.bigramsV)
                    u = (self.tokens_histogram[w1_w2_w3[2]] + 1) / (self.N + self.V)
                    prop = prop * (0.5 * b + 0.5 * u)

            else:
                prop = prop * ((self.trigrams_histogram[token] + 1) / (self.bigrams_histogram[
                                                                           w1_w2_w3[0] + ' ' + w1_w2_w3[
                                                                               1]] + self.trigramsV))  # C(w1w2w3 )+1/ C(w1w2) +v
        return prop

    def generate_sentences_bigrams(self, count):
        p = []
        words = []
        for w in self.bigrams_histogram:
            w1_w2 = w.split()
            p.append((self.bigrams_histogram[w] + 1) / (self.tokens_histogram[w1_w2[0]] + self.bigramsV))
            words.append(w)
        res = ""
        for n in range(count):
            rand_s = ""
            bigram = choices(words, p)[0].split()
            rand_s += bigram[0] + " " + bigram[1] + " "
            bigram = choices(words, p)[0].split()
            while (bigram[1] != Ngrams.end_token):
                rand_s += bigram[0] + " " + bigram[1] + " "
                bigram = choices(words, p)[0].split()
            res += rand_s + "\n"
        return res

    def generate_sentences_trigrams(self, count):

        p = []
        words = []
        self.trigrams_histogram
        for w in self.trigrams_histogram:
            w1_w2_w3 = w.split()
            p.append((self.trigrams_histogram[w] + 1) / (
                        self.bigrams_histogram[w1_w2_w3[0] + ' ' + w1_w2_w3[1]] + self.trigramsV))
            words.append(w)

        res = ""
        for n in range(count):
            rand_s = ""
            trigram = choices(words, p)[0].split()
            while (trigram[2] != Ngrams.end_token):
                if trigram[0] != Ngrams.begin_token and trigram[1] != Ngrams.begin_token:
                    rand_s += trigram[0] + " " + trigram[1] + " " + trigram[2] + " "
                trigram = choices(words, p)[0].split()
            res += rand_s + "\n"
        return (res)


def print_list(l, out):
    out.write(l)

# python ex2.py out1en.txt out1es.txt "C:\Users\yasseen\Desktop\New folder\\

if __name__ == "__main__":

    en_corpus_file = argv[1]
    es_corpus_file = argv[2]
    output_file = argv[3]
    out = open(output_file + ".txt", "w")
    phrases = ["You never know what you're gonna get",
               "Keep your friends close, but your enemies closer",
               "I've got a feeling we're not in Kansas anymore",
               "Quiero respirar tu cuello despacito",
               "Me gusta la moto, me gustas tú",
               "Dale a tu cuerpo alegría Macarena"]

    # Implement your main program here #
    en_corpus = open(en_corpus_file, encoding='utf-8').read()
    es_corpus = open(es_corpus_file, encoding='utf-8').read()

    en_model = Ngrams(en_corpus)
    es_model = Ngrams(es_corpus)
    bi_model = Ngrams(en_corpus + '\n' + es_corpus)

    en_model.get_unigrams()
    en_model.bigrams()
    en_model.get_trigrams()

    es_model.get_unigrams()
    es_model.bigrams()
    es_model.get_trigrams()

    bi_model.get_unigrams()
    bi_model.bigrams()
    bi_model.get_trigrams()

    for i, ph in enumerate(phrases):
        out.write(ph + '\n')
        out.write("Unigrams Model: " + str(en_model.get_unigrams_p(ph)) + " for English " + str(
            es_model.get_unigrams_p(ph)) + " for Spanish" + '\n')
        out.write("Bigrams Model:" + str(en_model.get_bigrams_p(ph)) + " for English " + str(
            es_model.get_bigrams_p(ph)) + " for Spanish" + '\n')
        out.write("Trigrams Model:" + str(en_model.get_trigrams_p(ph)) + " for English " + str(
            es_model.get_trigrams_p(ph)) + "for Spanish" + '\n')

    out.write("Unigrams Model in English Dataset:" + '\n')
    res = en_model.generate_sentences_unigrams(3)
    print_list(res, out)
    out.write("Bigrams Model in English Dataset:" + '\n')
    res = en_model.generate_sentences_bigrams(3)
    print_list(res, out)
    out.write("Trigrams Model in English Dataset:" + '\n')
    res = en_model.generate_sentences_trigrams(3)
    print_list(res, out)

    out.write("Unigrams Model in Bilingual Dataset:" + '\n')
    res = bi_model.generate_sentences_unigrams(3)
    print_list(res, out)
    out.write("Bigrams Model in Bilingual Dataset:" + '\n')
    res = bi_model.generate_sentences_bigrams(3)
    print_list(res, out)
    out.write("Trigrams Model in Bilingual Dataset:" + '\n')
    res = bi_model.generate_sentences_trigrams(3)
    print_list(res, out)



