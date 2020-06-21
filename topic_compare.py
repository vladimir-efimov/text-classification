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


def check_topics(topics_labeled_indeces, topics_computed_indeces):
    success_flag = True
    for topic in topics_labeled_indeces:
        if not topic in topics_computed_indeces:
            print("'" + topic + "' is missed in computed dataset")
            success_flag = False
    for topic in topics_computed_indeces:
        if not topic in topics_labeled_indeces:
            print("No '" + topic + "' is labeled dataset")
            success_flag = False
    return success_flag


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Usage: python3 " + sys.argv[0] + "<file with labeled topics> <file with predicted topics>")
        print("")
        print("\tProgram compares labeled text topics and predicted text topics.")
        exit()


    #--read data--
    (header_labeled, topics_labeled) = read_topics(sys.argv[1])
    (header_computed, topics_computed) = read_topics(sys.argv[2])

    #note: order of topics in labeled file may differs from topics in file with predicted topics
    topics_labeled_indeces = get_topic_indeces(header_labeled)
    topics_computed_indeces = get_topic_indeces(header_computed)
    if not check_topics(topics_labeled_indeces, topics_computed_indeces):
        exit(1)

    #--print header--
    header_line = ""
    topics_labeled_names = header_labeled.split("\t")

    for topic in topics_labeled_names:
        if topic == "File":
            header_line = header_line + "File\tSqrt Error\tMax Error"
        else:
            header_line = header_line + "\t" + topic
    print(header_line)


    #--compare topics and print errors--

    for textname in topics_labeled:
        text_topics_computed = topics_computed[textname]
        text_topics_labeled = topics_labeled[textname]

        #labeled text should have all topics
        sqrt_error = 0.0
        max_error = 0.0
        line = ""

        for topic in topics_labeled_names:
            if topic == "File":
                continue
            v1 = float(text_topics_labeled[topics_labeled_indeces[topic]])
            v2 = float(text_topics_computed[topics_computed_indeces[topic]])
            sqrt_error = sqrt_error + (v2 - v1) * (v2 - v1)
            delta = math.fabs(v2 - v1)
            if delta > max_error:
                max_error = delta
            line = line + "\t" + str(v2 - v1)

        sqrt_error = math.sqrt(sqrt_error)

        line = text_topics_labeled[topics_labeled_indeces["File"]] + "\t" + str(sqrt_error) + "\t" + str(max_error) + line
        print(line)
