# Copyright (c) 2021, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import math
import numpy as np
from .word_vector_model import WordVectorModel
from modules.tsv_reader import read_tsv_file


# Simplest model which represent words as topic vectors based on statistic file.
# Statistic file could be obtained as output of
# `key_words_from_stat.py --output-type=stat-table`
# So if we have topics t1 and t2, word w1 always appears in topic t1,
# word w2 always appears in topic t2, then
# w1 could be represented as (1,0), w2 - as (0,1).
# If word w3 appears equal number in topics t1 and t2 then
# w3 could be represented as (sqrt(2)/2, sqrt(2)/2)
# Assumption is that words are actually key words,
# undefined component of vectors are eliminated.
# Compare to key words vector model, in this model some key words could be related
# for example to 2 topics, and if topic set is large this word is still key word.

class WordTopicStatVectorModel(WordVectorModel):

    # first_topic_index refers index in [values], header = term name, [values]
    first_topic_index = 4

    def __init__(self, filename):
        super().__init__()
        self.word_vectors, self.topics = WordTopicStatVectorModel.__load_model(filename)

    # Reads file produced by key_words_from_stat.py --output-type=stat-table
    @staticmethod
    def __load_model(filename):
        (header_line, term_stat) = read_tsv_file(filename)
        # first_topic_index refers index in values, not in header, so add 1
        header_parts = header_line.split("\t")
        topics = []
        w_vectors = {}
        undefined_topic_index = -1
        vec_len = len(header_parts) - WordTopicStatVectorModel.first_topic_index - 1
        for i in range(WordTopicStatVectorModel.first_topic_index + 1, len(header_parts)):
            if header_parts[i] == "undefined":
                undefined_topic_index = i - 1
                vec_len -= 1
                continue
            topics.append(header_parts[i])

        for (term, values) in term_stat.items():
            vec = np.zeros(vec_len)
            itopic = 0
            for i in range(WordTopicStatVectorModel.first_topic_index, len(values)):
                if i == undefined_topic_index:
                    continue
                vec[itopic] = float(values[i])
                itopic += 1
            norm = math.sqrt(np.dot(vec, vec))
            if norm > 0.0:
                vec = (1.0 / norm) * vec
            w_vectors[term] = vec

        return w_vectors, topics

    def get_topics(self):
        return self.topics
