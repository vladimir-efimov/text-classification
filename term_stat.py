# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
sys.path.append('modules')


import text_processor
import text_processor_normalize
from term_scoring import get_term_score

def count_term_entries(text, tp, term_count, term_document_count):
    try:
        document_terms = set()

        words = tp.text_to_words(text)
        for word in words:
            if word in term_count:
                term_count[word] = term_count[word] + 1
                if not word in document_terms:
                    term_document_count[word] = term_document_count[word] + 1
                    document_terms.add(word)
            else:
                term_count[word] = 1
                term_document_count[word] = 1
                document_terms.add(word)
    except ValueError as e:
        print(e)


if __name__ == "__main__":

    term_count = {}
    term_document_count = {}
    term_score = {}
    num_documents = 0

    tp = text_processor_normalize.TextProcessorNormalize("stop_words.txt")
#    tp = text_processor.TextProcessor("stop_words.txt")
    stop_words = tp.get_stop_words()
    #empty word could be in word list represented text as specific of text processing
    stop_words.add("")

    if len(sys.argv) == 1:
        print("Usage: python3 " + sys.argv[0] + " <text file(s)>")
        print("")
        print("\tProgram counts terms in text files and evaluates term's score")
        exit()

    for iarg in range(1, len(sys.argv)):
        filename = sys.argv[iarg]
        f = open(filename)
        text = f.read()
        text = tp.preprocess_text(text)
        num_documents = num_documents + 1

        count_term_entries(text, tp, term_count, term_document_count)
        
        f.close()
        

    for (term, count) in term_count.items():
        term_score[term] = get_term_score(count, term_document_count[term], num_documents)

    sorted_items=sorted(term_score.items(), reverse = True, key = lambda key_value:(key_value[1], key_value[0]))

    print("Term\tScore\tCount\tDocument count")
    for (term, score) in sorted_items:
        print(term + "\t" + str(score) + "\t" + str(term_count[term]) + "\t" + str(term_document_count[term]))

