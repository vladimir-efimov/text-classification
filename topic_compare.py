# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import sys
import math
sys.path.append('modules')


def read_topics(filename):
    f = open(filename)
    header = f.readline().strip()

    #data stored in format: file name -> topics
    topics = {}

    line = f.readline()
    while line:
        text_topics = line.strip().split("\t")
        topics[text_topics[0]] = text_topics
        line = f.readline()

    f.close()
    return (header, topics)


def get_topic_indeces(header):
    topics = header.split("\t")
    topics_indeces = {}
    i = 0
    for topic in topics:
        topics_indeces[topic] = i
        i = i + 1
    return topics_indeces


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Usage: python3 " + sys.argv[0] + "<file with labeled topics> <file with predicted topics>")
        print("")
        print("\tProgram compares labeled text topics and predicted text topics.")
        exit()


    #--read data--
    (header, topics_labeled) = read_topics(sys.argv[1])
    (header2, topics) = read_topics(sys.argv[2])

    #note: order of topics in labeled file may differs from topics in file with predicted topics
    topics_indeces = get_topic_indeces(header)
    topics_indeces2 = get_topic_indeces(header2)


    #--print header--
    header_line = ""
    topics_names = header.split("\t")
    topics_names2 = header2.split("\t")

    for topic in topics_names:
        if topic == "File":
            header_line = header_line + "File\tSqrt Error\tMax Error"
        else:
            header_line = header_line + "\t" + topic
    print(header_line)


    #--compare topics and print errors--

    for textname in topics:
        text_topics = topics[textname]
        text_topics_labeled = topics_labeled[textname]

        #labeled text should have all topics
        sqrt_error = 0.0
        max_error = 0.0
        line = ""

        for topic in topics_names:
            if topic == "File":
                continue
            v1 = float(text_topics_labeled[topics_indeces[topic]])
            if topic in topics_names2:
                v2 = float(text_topics[topics_indeces2[topic]])
            else:
                v2 = 0.0
            sqrt_error = sqrt_error + (v2 - v1) * (v2 - v1)
            delta = math.fabs(v2 - v1)
            if delta > max_error:
                max_error = delta
            line = line + "\t" + str(v2 - v1)

        sqrt_error = math.sqrt(sqrt_error)

        line = text_topics_labeled[topics_indeces["File"]] + "\t" + str(sqrt_error) + "\t" + str(max_error) + line
        print(line)
