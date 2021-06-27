# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import re


class TextProcessor:

    @staticmethod
    def __load_stop_words(filename):
        file = open(filename)
        stop_words = set()
        line = file.readline()
        while line:
            words = re.sub("\s|\t", "", line).split(",")
            for word in words:
                stop_words.add(word)
            line = file.readline()
        file.close()
        return stop_words


    def __init__(self, filename):
        self.stop_words = self.__load_stop_words(filename)


    def preprocess_text(self, text):
        return re.sub("^\W+|\W+$|\!|\,|\?|\.", " ", text, flags=re.UNICODE).lower()


    def text_to_words(self, text):
        preprocessed_text = self.preprocess_text(text)
        all_words = re.split("\W*\s+\W*", preprocessed_text, flags=re.UNICODE)
        words = []
        for word in all_words:
            if not word in self.stop_words:
                words.append(word)
        return words


    def sentence_to_words(self, sentence):
        preprocessed_sentence = re.sub("[!?.]+$", "", sentence, flags=re.UNICODE).lower()
        all_words = re.split("\W*\s+\W*", preprocessed_sentence, flags=re.UNICODE)

        words = []
        for word in all_words:
            if word not in self.stop_words:
                words.append(word)
        return words


    def text_to_sentences(self, text):
        sentences = re.split("\!|\?|\.", text, flags=re.UNICODE)
        filtered_sentences = []

        adding_sentence = ""
        commulative_len = 0

        for sentence in sentences:
            slen = len(sentence)
            # need form new sentence
            processed_sentence = re.sub("^\W+", "", sentence, flags=re.UNICODE)
            processed_sentence = re.sub("\t|\r|\n", " ", processed_sentence, flags=re.UNICODE)
            processed_sentence = re.sub("\"", "'", processed_sentence, flags=re.UNICODE)

            if adding_sentence == "":
                adding_sentence = processed_sentence
            else:
                if re.match("^\W*[A-Z]|^\W*[А-Я]", processed_sentence):
                    # detected start of new sentence
                    adding_sentence = re.sub("\s+", " ", adding_sentence, flags=re.UNICODE)
                    filtered_sentences.append(adding_sentence + text[commulative_len-1])
                    adding_sentence = processed_sentence
                else:
                    # join 2 parts of one sentence
                    adding_sentence = adding_sentence + text[commulative_len-1] + processed_sentence

            commulative_len = commulative_len + slen + 1

        if not adding_sentence == "":
            adding_sentence = re.sub("\s+", " ", adding_sentence, flags=re.UNICODE)
            filtered_sentences.append(adding_sentence)

        return filtered_sentences


    def get_stop_words(self):
        return self.stop_words
