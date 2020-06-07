# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
sys.path.append('modules')

import text_processor


def split_text(text, tp):
    try:
        sentences = tp.text_to_sentences(text)
        return sentences

    except ValueError as e:
        print(e)
        return []


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Usage: python3 " + sys.argv[0] + " <text file(s)>")
        print("")
        print("\tProgram split text from input files on sentences and outputs result in format:")
        print("\tTabs substituted with spaces, double quotes is substituted with quotes.")
        print("\t<filename> <tab> <sentence>")
        exit()

    tp = text_processor.TextProcessor("stop_words.txt")
    print("File\tSentence")

    for iarg in range(1, len(sys.argv)):
        filename = sys.argv[iarg]
        f = open(filename)
        text = f.read()
        f.close()

        sentences = split_text(text, tp)
        for sentence in sentences:
            print(filename + "\t" + sentence)
