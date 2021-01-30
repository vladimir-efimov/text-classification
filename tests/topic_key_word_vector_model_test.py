import sys

sys.path.append("..")
from modules.vector_models.topic_key_word_vector_model import TopicKeyWordVectorModel


if __name__ == "__main__":
    model = TopicKeyWordVectorModel("topic_key_words.txt")

    print("Model is loaded")
    print("Model size is " + str(model.size()))
    print("Vector length is " + str(model.get_vector_length()))
    print("Model topics is " + str(model.get_topics()))
    print("'Footbal_' is in the model: " + str(model.has_word("Footbal_")))
    print("'tennis' is in the model: " + str(model.has_word("tennis")))
    print("Vector for 'tennis' is: " + str(model.get_vector("tennis")))
    print("'hotel' is in the model: " + str(model.has_word("hotel")))
    print("Vector for 'hotel' is: " + str(model.get_vector("hotel")))
