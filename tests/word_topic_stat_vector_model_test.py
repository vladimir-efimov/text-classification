import math
import numpy
import unittest
import sys

sys.path.append("..")
from modules.vector_models.word_topic_stat_vector_model import WordTopicStatVectorModel


class TestWordTopicStatVectorModel(unittest.TestCase):
    def test_model(self):
        model = WordTopicStatVectorModel("topic_key_words.csv")

        print("Model is loaded")
        print("Model size is " + str(model.size()))
        self.assertEqual(5, model.size())
        print("Vector length is " + str(model.get_vector_length()))
        self.assertEqual(2, model.get_vector_length())
        print("Model topics is " + str(model.get_topics()))
        self.assertFalse(model.has_word("Footbal_"))
        self.assertTrue(model.has_word("tennis"))
        vec = model.get_vector("tennis")
        print("Vector for 'tennis' is: " + str(vec))
        norm = math.sqrt(numpy.dot(vec, vec))
        self.assertTrue(0.999 < norm and norm < 1.001)

        self.assertTrue(model.has_word("hotel"))
        print("Vector for 'hotel' is: " + str(model.get_vector("hotel")))


if __name__ == "__main__":
    unittest.main()
