# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
from modules.tsv_reader import read_tsv_file
val_format = "{:3.2f}%"


# return index in topic_stat which corresponds to topic majority
def get_topic_majority(weight):
    if weight > 0.7:
        # main topic
        return 0
    if weight > 0.5:
        # major topic
        return 1
    if weight > 0.2:
        # topic presents
        return 2
    # topic absents
    return 3


def compute_topic_stat(header, documents_topics):
    topic_stat = {}
    topics = header.split("\t")
    topics.remove("File")

    for topic_name in topics:
        topic_stat[topic_name] = [0.0, 0.0, 0.0, 0.0]

    for document_name  in documents_topics:
        document_topics = documents_topics[document_name]

        i = 0
        for topic_name in topics:
            majority_index = get_topic_majority(float(document_topics[i]))
            topic_stat[topic_name][majority_index] += 1
            i += 1

    # compute percentage
    ndocs = len(documents_topics)
    for topic_name in topics:
        for j in range(0, 4):
            topic_stat[topic_name][j] = float(topic_stat[topic_name][j]) / float(ndocs) * 100.0

    return topic_stat


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Usage: python3 " + sys.argv[0] + " <file with topics>")
        print("")
        print("\tProgram produces topics statistic for file with topics")
        print("\tin which percentage of documents topic present, in which topic is major topic or main")
        exit()

    filename = sys.argv[1]
    (header, documents_topics) = read_tsv_file(filename)
    if not header.startswith("File"):
        sys.stderr.write("Unsupported file format: first column should have name 'File'\n")
        exit(1)

    topic_stat = compute_topic_stat(header, documents_topics)

    print("\t".join(["Topic", "Main topic", "Major topic", "Topic presents", "Topic absents"]))
    for topic_name in topic_stat:
        line = topic_name
        for value in topic_stat[topic_name]:
            line += "\t" + val_format.format(value)
        print(line)
