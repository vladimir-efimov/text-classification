# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys

from modules.text_processor_normalize import TextProcessorNormalize
from modules.vector_models.topic_key_word_vector_model import TopicKeyWordVectorModel
from modules.classifiers.bag_of_words_classifier import BagOfWordsClassifier 


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: python3 " + sys.argv[0] + " <key_words_file>  <text file(s)>")
        print("")
        print("Program classifies text files using topic key words file in following format")
        print("\t<topic 1>: <key word 1>, <key word 2>, ...")
        exit()

    tp = TextProcessorNormalize("stop_words.txt")
    model_file = sys.argv[1]
    model = TopicKeyWordVectorModel(model_file)
    classifier = BagOfWordsClassifier(model, tp)

    topics = model.get_topics()
    print("File\t" + "\t".join(topics))
    if len(topics) == 0:
        print("Error: no topics are loaded")
        exit(1)

    for iarg in range(2, len(sys.argv)):
        filename = sys.argv[iarg]
        f = open(filename)
        text = f.read()
        f.close()

        topic_vector = classifier.classify(text)
        output_str = filename
        for val in topic_vector:
            output_str += "\t" + str(val)
        print(output_str)
