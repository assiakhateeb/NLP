#!/usr/bin/env python
"""
@author: Assia Khateeb ID 206217028
"""

# # Part 1 - data preperations
class Data_prep():

    def __init__(self, input_filename, output_dir_path):
        self.input_filename = input_filename
        self.output_dir_path = output_dir_path

    def read_prep_data(self):
        file = open(input_filename,'rb')
        txt = file.read()
        txt = txt.decode('utf-8')
        new_txt = self.new_reddit_corpus(txt)
        self.new_txt = self.tokenize(new_txt)
        #self.new_txt = new_txt
        self.split()

    def delete_symbols(self, reddit_corpus):
        symbols = ['~', '@', '#', '^', '&', '*', '_', '<', '>','|', "\\", '=', '+', '--']
        res = [symbol for symbol in symbols if (symbol in reddit_corpus)]
        for symbol in res:
            reddit_corpus = reddit_corpus.replace(symbol, ' ')
        reddit_corpus = re.sub('/ ', ' ', reddit_corpus)
        reddit_corpus = re.sub(' /', ' ', reddit_corpus)
        return reddit_corpus

    def delete_url(self, reddit_corpus):
        reddit_corpus = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))\)|[^\s`!()\[\]{};:'"., <>?«»“”‘’]))''', "", reddit_corpus)
        reddit_corpus = re.sub('https|HTTPS|Https', '', reddit_corpus)
        return re.sub(r"\S+\.html", '', reddit_corpus)

    def delete_emoji(self, reddit_corpus):
        return re.sub("[" "\U0001F1E0-\U0001F1FF""\U0001F300-\U0001F5FF""\U0001F600-\U0001F64F""\U0001F680-\U0001F6FF""\U0001F700-\U0001F77F""\U0001F780-\U0001F7FF""\U0001F800-\U0001F8FF""\U0001F900-\U0001F9FF""\U0001FA00-\U0001FA6F""\U0001FA70-\U0001FAFF""\U00002702-\U000027B0""\U000024C2-\U0001F251""]+", '', reddit_corpus)

    def delete_others(self, reddit_corpus):
        reddit_corpus = re.sub('&gt;|&lt;|url|&amp;', '', reddit_corpus)
        reddit_corpus = re.sub(r'()@\w+|/r/\w+|#\w+', r'\1', reddit_corpus)
        reddit_corpus = re.sub(r"[-\#/@<>{}()""/+=~|*^%&_]", "", reddit_corpus)
        reddit_corpus = re.sub('\[', '', reddit_corpus)
        reddit_corpus = re.sub('\]', '', reddit_corpus)
        reddit_corpus = re.sub('\:{2,1000}', ':', reddit_corpus)
        reddit_corpus = re.sub(r'\\{2,1000}', r'\\', reddit_corpus)
        reddit_corpus = re.sub(r'\\ ', '', reddit_corpus)
        reddit_corpus = re.sub(r'\.;|\.,|\.:', '.', reddit_corpus)
        reddit_corpus = re.sub(r'\?.|\?;|\?,|\?:', '?', reddit_corpus)
        reddit_corpus = re.sub(r'\!,|\!;|\!.|\!:', '!', reddit_corpus)
        reddit_corpus = re.sub('\n', ' ', reddit_corpus)
        return reddit_corpus

    def delete_keyword(self, reddit_corpus):
        reddit_corpus = re.sub(r"/r/\S+|r/\S+|\S+/r/\S+", ' ', reddit_corpus)
        reddit_corpus = re.sub(r"/u/\S+|u/\S+", '', reddit_corpus)
        return reddit_corpus

    def delete_spaces(self, reddit_corpus):
        reddit_corpus = re.sub(r"^\s+", '', reddit_corpus)
        reddit_corpus = re.sub(r"\s+$", '', reddit_corpus)
        reddit_corpus = re.sub(r"\s+", ' ', reddit_corpus)
        return reddit_corpus

    def delete_puncuation_marks(self, reddit_corpus):
        reddit_corpus = re.sub(r"\?+", "?", reddit_corpus)
        reddit_corpus = re.sub(r"\.+", ".", reddit_corpus)
        reddit_corpus = re.sub(r"\,+", ",", reddit_corpus)
        reddit_corpus = re.sub(r"\!+", "!", reddit_corpus)
        reddit_corpus = re.sub(r"\'+", "'", reddit_corpus)
        reddit_corpus = re.sub(r"\;+", ";", reddit_corpus)
        return reddit_corpus

    def new_reddit_corpus(self, reddit_corpus):
        reddit_corpus = self.delete_symbols(reddit_corpus)
        reddit_corpus = self.delete_url(reddit_corpus)
        reddit_corpus = self.delete_emoji(reddit_corpus)
        reddit_corpus = self.delete_others(reddit_corpus)
        reddit_corpus = self.delete_keyword(reddit_corpus)
        reddit_corpus = self.delete_spaces(reddit_corpus)
        reddit_corpus = self.delete_puncuation_marks(reddit_corpus)

        reddit_corpus = re.sub(r'\n\n', r'\n', reddit_corpus)
        return reddit_corpus

    def split(self):
        reddit_corpus = re.split(r'(?<!\w\.\w.)(?<=\.|\?|\!|\;|\,)(\s)', self.new_txt)
        #print(reddit_corpus)
        sentences = []
        for sen in reddit_corpus:
            sen1 = sen
            if len(sen1.split(' ')) >= 4:
                sentences.append(sen)
        self.sentences = sentences

    def tokenize(self, sentences):
        t = re.findall(r"\w\.\w.|.\.|.+|[.,?!;']", sentences, flags=re.ASCII)
        t = ' '.join(t)
        return t

# # Part 2 - Language detection

class Lang_detect(Data_prep):

    def __init__(self, input_filename, output_dir_path):
        self.input_filename = input_filename
        self.output_dir_path = output_dir_path
        self.detections = {}

    def detect_senteces(self):
        i = 0
        for sen in self.sentences:
            i+=1
            try:
                scores = detect_langs(sen)
            except Exception as e:
                pass
            self.detect(scores, sen)

    def detect(self, scores, sen):
        num_cand_lang = len(scores)

        if num_cand_lang < 1:
            return

        if scores[0].prob > 0.95:
            lang = scores[0].lang
            try:
                self.detections[lang].append(sen)
            except:
                self.detections[lang] = [sen]
            return

        if num_cand_lang < 2:
            return

        if scores[0].prob < 0.6:
            return

        if scores[1].prob > 0.1:
            lang = scores[0].lang + "_" + scores[1].lang
            try:
                self.detections[lang].append(sen)
            except:
                self.detections[lang] = [sen]
            return

    def print_detections(self):
        #languages = self.detections.keys()
        languages = ["en", "es", "en_es"]
        for lang in languages:
                file = open(self.output_dir_path + lang + ".txt", "wb")
                sentences = self.detections[lang]
                for sen in sentences:
                    sen = sen + u'\n'
                    file.write(sen.encode('utf-8'))
                file.close()


# # Code shell - wrapping all parts together
#python python Khateeb_Assia_ex1.py "C:\\Users\\yasseen\\Desktop\\nlp\\reddit_corpus2.txt" "C:\Users\yasseen\Desktop\New folder\\"

from langdetect import detect_langs
from sys import argv
import re


if __name__ == "__main__":
    input_filename = argv[1]
    output_dir_path = argv[2]

    #input_filename = "reddit_corpus2.txt"
    #output_dir_path = ""

    Language_detector = Lang_detect(input_filename, output_dir_path)

    # Part 1
    Language_detector.read_prep_data()

    # Part 2
    Language_detector.detect_senteces()
    Language_detector.print_detections()


