# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import sys
import math


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Usage: python3 " + sys.argv[0] + " <input labeled file>")
        print("")
        print("\tProgram reads labeled sentences and defines which topics are covered by input texts.")
        print("\tFormat of input file")
        print("\t\t<filename> <tab> <sentence> <tab> <topic>")
        exit()

    topics = {}
    topic_set = set()
    filename = sys.argv[1]
    f = open(filename)
    f.readline()
    #skip header
    line = f.readline()
    
    while line:
        try:
            (textname, _, topic) = line.strip().split("\t");
            if topic:
                topic_set.add(topic)

            if textname in topics:
                text_topics = topics[textname]
                if topic in text_topics:
                    topic_number = text_topics[topic]
                    text_topics[topic] = topic_number + 1
                else:
                    text_topics[topic] = 1
            
            else:
                text_topics = {}
                text_topics[topic] = 1
                topics[textname] = text_topics
            
            line = f.readline()

        except ValueError as e:
            line = f.readline()

    f.close()

    header = "File"
    for topic in topic_set:
        if not topic == "undefined":
            header = header + "\t" + topic
    print(header)

    for textname in topics:
        square_sum = 0
        text_topics = topics[textname]
        for topic in text_topics:
            if not topic == "undefined":
                square_sum = square_sum + text_topics[topic] * text_topics[topic]

        line = textname
        for topic in topic_set:
            if topic == "undefined":
                continue
            if topic in text_topics:
                topic_weight = text_topics[topic] / math.sqrt(float(square_sum))
            else:
                topic_weight = 0.0
            line = line + "\t" + str(topic_weight)
        print(line)
