# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


# read data from file in tab separated value format
# first row - header with column names,
# first column - defines entry unique name and others - properties for each entry
# returns header line and dictionary with data, properties returned as list
def read_tsv_file(filename):
    f = open(filename)
    # read header which consist of 'File' and name of topics separated by tab
    header = f.readline().strip()

    # data stored in format: file name -> weight of each topic separated by tab
    topics = {}

    line = f.readline()
    while line:
        text_topics = line.strip().split("\t")
        topics[text_topics[0]] = text_topics[1:]
        line = f.readline()

    f.close()
    return header, topics
