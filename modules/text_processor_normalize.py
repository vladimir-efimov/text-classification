# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import text_processor as tp
import re
import pymorphy2


class TextProcessorNormalize(tp.TextProcessor):

    def __init__(self, filename):
        super().__init__(filename)
        self.analyzer = pymorphy2.MorphAnalyzer()


    def text_to_words(self, text):
        all_words = re.split("\W*\s+\W*", text, flags=re.UNICODE)
        words = []
        for word in all_words:
            if not word in self.stop_words:
                normalized_word = self.analyzer.parse(word)[0].normal_form
                words.append(normalized_word)
        return words

