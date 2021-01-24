# Copyright (c) 2021, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


# Abstract class representing words as vectors
class WordVectorModel:

    def __init__(self):
        self.word_vectors = {}

    # returns True if word is in model and has some vector representation
    def has_word(self, word):
        return word in self.word_vectors

    def get_vector_length(self):
        if len(self.word_vectors) == 0:
            return 0
        for (word, word_vector) in self.word_vectors.items():
            return len(word_vector)

    def get_vector(self, word):
        if word not in self.word_vectors:
            raise ValueError(word + " is not in the model")
        return self.word_vectors[word]

    def size(self):
        return len(self.word_vectors)
