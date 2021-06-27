# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from .text_processor import TextProcessor
import re
import pymorphy2


class TextProcessorNormalize(TextProcessor):

    def __init__(self, filename):
        super().__init__(filename)
        self.analyzer = pymorphy2.MorphAnalyzer()

    def text_to_words(self, text):
        preprocessed_text = self.preprocess_text(text)
        all_words = re.split("\W*\s+\W*", preprocessed_text, flags=re.UNICODE)
        words = []
        for word in all_words:
            if word not in self.stop_words:
                normalized_word = self.analyzer.parse(word)[0].normal_form
                words.append(normalized_word)
        return words

    def sentence_to_words(self, sentence):
        preprocessed_sentence = re.sub("[!?.]+$", "", sentence, flags=re.UNICODE).lower()
        all_words = re.split("\W*\s+\W*", preprocessed_sentence, flags=re.UNICODE)
        words = []
        for word in all_words:
            if word not in self.stop_words:
                normalized_word = self.analyzer.parse(word)[0].normal_form
                words.append(normalized_word)
        return words
