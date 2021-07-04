# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import unittest

sys.path.append("..")
from modules.text_processor_normalize import TextProcessorNormalize
from modules.vector_models.word_topic_stat_vector_model import WordTopicStatVectorModel
from modules.classifiers.bag_of_words_classifier import BagOfWordsClassifier 


class TestWordTopicStatClassifier(unittest.TestCase):
    def test_model(self):
        tp = TextProcessorNormalize("../stop_words.txt")
        model_file = "topic_key_words.csv"
        model = WordTopicStatVectorModel(model_file)
        classifier = BagOfWordsClassifier(model, tp)

        self.assertTrue(model.has_word("tennis"))
        self.assertTrue(model.has_word("hotel"))

        topics = model.get_topics()
        print("# test\t" + "\t".join(topics))

        # test case 1
        text = "We've booked chip room in a hotel."
        topic_vector = classifier.classify(text)
        output_str = "test_case_1"
        for val in topic_vector:
            output_str += "\t" + str(val)
        print(output_str)
        self.assertTrue(0.12 > topic_vector[0])
        self.assertTrue(0.99 < topic_vector[1])


        # test case 2
        text = "We've booked chip room in a hotl."
        topic_vector = classifier.classify(text)
        output_str = "test_case_2"
        for val in topic_vector:
            output_str += "\t" + str(val)
        print(output_str)
        self.assertEqual(0.0, topic_vector[0])
        self.assertEqual(0.0, topic_vector[1])

        # test case 3
        text = "Have you bought a tickets to the tennis match?"
        topic_vector = classifier.classify(text)
        output_str = "test_case_3"
        for val in topic_vector:
            output_str += "\t" + str(val)
        print(output_str)
        self.assertTrue(0.8 < topic_vector[0])
        self.assertTrue(topic_vector[1] < 0.5)


if __name__ == "__main__":
    unittest.main()
