# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import argparse
from modules.tsv_reader import read_tsv_file
from modules.table_comparator import get_property_indexes

# first_topic_index refers index in [values], header = term name, [values]
first_topic_index = 4

if __name__ == "__main__":

    descr_str = "Program detects key words for topics based on terms statistic obtained for labeled text."
    arg_parser = argparse.ArgumentParser(prog="python3 " + sys.argv[0], description=descr_str)
    arg_parser.add_argument(dest="input_file", help="File with term statistic")
    arg_parser.add_argument("--min-score", default=100.0, type=float,
                            help="filter out terms which score is less than specified")
    arg_parser.add_argument("--min-labeled-ratio", default=0.01, type=float,
                            help="filter out terms which labeled ratio is less than specified")
    arg_parser.add_argument("--min-topic-ratio", default=0.75, type=float,
                            help="filter out terms which max topic ratio for is less than specified")
    arg_parser.add_argument("--output-format", default="keyword-list", choices=["keyword-list", "stat-table"],
                            help="filter out terms which max topic ratio for is less than specified")

    args = arg_parser.parse_args()

    # --read data--
    (header_line, term_stat) = read_tsv_file(args.input_file)
    header_indexes = get_property_indexes(header_line)
    header = header_line.split("\t")
    score_index = header_indexes["Score"]
    labeled_ratio_index = header_indexes["Labeled ratio"]
    undefined_topic_index = header_indexes["undefined"]

    # --process data--
    key_words = {}
    if (args.output_format == "keyword-list"):
        # first_topic_index refers index in values, not in header, so add 1
        for i in range(first_topic_index + 1, len(header)):
            if i == undefined_topic_index + 1:
                continue
            key_words[header[i]] = []
    else:
        print(header_line)

    for (term, values) in term_stat.items():
        score = float(values[score_index])
        if score < args.min_score:
            continue
        labeled_ratio = float(values[labeled_ratio_index])
        if labeled_ratio < args.min_labeled_ratio:
            continue

        max_topic_ratio = 0.0
        max_topic_index = 0
        for i in range(first_topic_index, len(values)):
            if i == undefined_topic_index:
                continue
            if float(values[i]) > max_topic_ratio:
                max_topic_ratio = float(values[i])
                max_topic_index = i

        if max_topic_ratio < args.min_topic_ratio:
            continue

        if args.output_format == "stat-table":
            output_str = "\t".join([term, "\t".join(values)])
            print(output_str)
        else:
            key_words[header[max_topic_index + 1]].append(term)

    if args.output_format == "keyword-list":
        for topic in key_words:
            print("{}: {}".format(topic, ", ".join(key_words[topic])))
