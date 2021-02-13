# Copyright (c) 2021, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import numpy as np
from .word_vector_model import WordVectorModel


# Simplest model which represent key words for topic as vectors
# This model is based on assumption that we have some words which defines topic
# So if we have topics t1 and t2, word w1 defines topic t1, word w2 defines topic t2,
# so w1 could be represented as (1,0), w2 - as (0,1).
# And we believe that word w1 shouldn't be in text with topic 2,
# word w2 should't be in text with topic 1, or such cases are quite rare
# and we can tolerate it

class TopicKeyWordVectorModel(WordVectorModel):

    def __init__(self, filename):
        super().__init__()
        self.word_vectors, self.topics = TopicKeyWordVectorModel.__load_model(filename)

    # Reads file in format:
    # <topic1>: <key word 1>, <<key word 2>, ...
    @staticmethod
    def __load_model(filename):
        w_vectors = {}
        topics = []
        words_str_list = []
        with open(filename) as fin:
            line = fin.readline()
            while line:
                line = line.replace(", ", ",").replace(": ", ":")
                if ":" in line:
                    (topic, key_words_str) = line.split(":")
                    topics.append(topic)
                    words_str_list.append(key_words_str)
                line = fin.readline()

        itopic = 0
        vec_len = len(topics)
        for words_str in words_str_list:
            vec = np.zeros(vec_len)
            vec[itopic] = 1.0
            words_arr = words_str.split(",")
            for word in words_arr:
                w_vectors[word] = vec
            itopic += 1

        return w_vectors, topics

    def get_topics(self):
        return self.topics
