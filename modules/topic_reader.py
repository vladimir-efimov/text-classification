# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


# read topics from labeled file
def read_topics(filename):
    f = open(filename)
    # read header which consist of 'File' and name of topics separated by tab
    header = f.readline().strip()

    # data stored in format: file name -> weight of each topic separated by tab
    topics = {}

    line = f.readline()
    while line:
        text_topics = line.strip().split("\t")
        topics[text_topics[0]] = text_topics
        line = f.readline()

    f.close()
    return (header, topics)

