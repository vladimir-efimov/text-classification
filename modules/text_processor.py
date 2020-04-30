# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import re

class TextProcessor:

    def __load_stop_words(self, filename):
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
        #return re.sub("^\W+|\W+$", "", text, flags=re.UNICODE).lower()
        return re.sub("^\W+|\W+$|\!|\,|\?|\.", " ", text, flags=re.UNICODE).lower()


    def text_to_words(self, text):
        all_words = re.split("\W*\s+\W*", text, flags=re.UNICODE)
        words = []
        for word in all_words:
            if not word in self.stop_words:
                words.append(word)
        return words


    def get_stop_words(self):
        return self.stop_words


