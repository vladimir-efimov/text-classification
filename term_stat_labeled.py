# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import modules.text_processor_normalize as tpn
from modules.term_scoring import get_term_score


def count_term_entries(sentences, tp, term_count, term_document_count, topics_words):
    document_terms = set()

    for (sentence, topic) in sentences:
        words = tp.text_to_words(sentence)
        if topic != "" and topic not in topics_words:
            topics_words[topic] = {}
        for word in words:
            if word in term_count:
                term_count[word] += 1
                if word not in document_terms:
                    term_document_count[word] += 1
                    document_terms.add(word)
            else:
                term_count[word] = 1
                term_document_count[word] = 1
                document_terms.add(word)

            if topic == "":
                continue
            if word in topics_words[topic]:
                topics_words[topic][word] += 1
            else:
                topics_words[topic][word] = 1


if __name__ == "__main__":

    term_count = {}
    term_document_count = {}
    term_score = {}
    topics_words = {}
    num_documents = 0

    text_processor = tpn.TextProcessorNormalize("stop_words.txt")
    stop_words = text_processor.get_stop_words()
    # empty word could be in word list represented text as specific of text processing
    stop_words.add("")

    if len(sys.argv) == 1:
        print("Usage: python3 " + sys.argv[0] + " <file with labeled text>")
        print("")
        print("\tProgram counts terms in labeled text and evaluates term's score as for not labeled text")
        print("\tAdditionally program calculates words distribution across topics")
        exit()

    label_filename = sys.argv[1]
    with open(label_filename) as f:
        f.readline()  # skip header
        line = f.readline().strip()
        old_filename = ""
        sentences = []
        while line:
            line_parts = line.split("\t")
            if len(line_parts) < 2:
                break
            filename = line_parts[0]
            sentence = line_parts[1]
            topic = "" if len(line_parts) == 2 else line_parts[2]
            text = text_processor.preprocess_text(sentence)

            if filename == old_filename or old_filename == "":
                sentences.append((sentence, topic))
            else:
                count_term_entries(sentences, text_processor, term_count, term_document_count, topics_words)
                sentences.clear()
                sentences.append((sentence, topic))
                num_documents += 1
            old_filename = filename
            line = f.readline().strip()

        if len(sentences) > 0:
            num_documents += 1

        count_term_entries(sentences, text_processor, term_count, term_document_count, topics_words)

    for (term, count) in term_count.items():
        term_score[term] = get_term_score(count, term_document_count[term], num_documents)

    sorted_items = sorted(term_score.items(), reverse=True, key=lambda key_value: (key_value[1], key_value[0]))

    topic_list = topics_words.keys()
    header = ["Term", "Score", "Count", "Document count", "Labeled ratio"]
    header.extend(topic_list)
    print("\t".join(header))

    for (term, score) in sorted_items:
        output_line = ""
        labeled_count = 0
        for topic in topics_words:
            if term in topics_words[topic]:
                labeled_count += topics_words[topic][term]
        labeled_ratio = float(labeled_count) / float(term_count[term])

        for topic in topics_words:
            if term in topics_words[topic]:
                topic_word_ratio = float(topics_words[topic][term]) / float(labeled_count)
                output_line += "\t{:f}".format(topic_word_ratio)
            else:
                output_line += "\t0.0"

        output_line = "{}\t{:f}\t{}\t{}\t{:f}".format(
            term, score, term_count[term], term_document_count[term], labeled_ratio) + output_line
        print(output_line)
