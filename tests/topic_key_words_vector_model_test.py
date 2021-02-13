import unittest
import sys

sys.path.append("..")
from modules.vector_models.topic_key_word_vector_model import TopicKeyWordVectorModel


class TestTopicKeyWordVectorModel(unittest.TestCase):
    def test_model(self):
        model = TopicKeyWordVectorModel("topic_key_words.txt")

        print("Model is loaded")
        print("Model size is " + str(model.size()))
        self.assertEqual(6, model.size())
        print("Vector length is " + str(model.get_vector_length()))
        self.assertEqual(2, model.get_vector_length())
        print("Model topics is " + str(model.get_topics()))
        self.assertFalse(model.has_word("Footbal_"))
        self.assertTrue(model.has_word("tennis"))
        print("Vector for 'tennis' is: " + str(model.get_vector("tennis")))
        self.assertTrue(model.has_word("hotel"))
        print("Vector for 'hotel' is: " + str(model.get_vector("hotel")))


if __name__ == "__main__":
    unittest.main()
