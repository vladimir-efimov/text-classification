# Copyright (c) 2021, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import math
import numpy as np

# Base class which classifies text using Bag-Of-Words approach and some word vector model
# So model just sums word vectors.
# In simplest case weights of vectors reflects topics.
# Otherwise translation of summary vector is needed from original vector space to topic vector
# It could be done with trained classifier which may be implemented as inheritor of this class
# Need to override _get_topic_vector() then.


class BagOfWordsClassifier:

    def __init__(self, vector_model, text_processor):
        self.model = vector_model
        self.text_processor = text_processor

    def _get_text_vector(self, text):
        preprocessed_text = self.text_processor.preprocess_text(text)
        words = self.text_processor.text_to_words(preprocessed_text)
        vec_len = self.model.get_vector_length()
        sum_vector = np.zeros(vec_len)

        for word in words:
            if self.model.has_word(word):
                sum_vector += self.model.get_vector(word)
        norm = math.sqrt(np.dot(sum_vector, sum_vector))
        if norm > 0.0:
            text_vector = (1.0 / norm) * sum_vector
        else:
            text_vector = sum_vector
        return text_vector

    def _get_topic_vector(self, text_vector):
        return np.ndarray.tolist(text_vector)

    def classify(self, text):
        text_vector = self._get_text_vector(text)
        topic_vector = self._get_topic_vector(text_vector)
        return topic_vector
