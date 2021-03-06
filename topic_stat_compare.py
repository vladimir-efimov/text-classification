# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import argparse
from modules.tsv_reader import read_tsv_file
from modules.table_comparator import compare_table_data

val_format = "{:3.2f}"


def print_metrics(metrics):
    for metric in metrics:
        print(metric + "\t" + str(metrics[metric]))


def print_topics_comparison(topics_comparison, topics_names):
    # --print header--
    header_line = "Topic\tSqrt Error\tMax Error"

    for topic in topics_names:
        if not topic == "Topic":
            header_line += "\t" + topic
    print(header_line)

    # --print comparison--
    for (file_name, topic_comparison) in topics_comparison:
        line = "\t".join([file_name, val_format.format(topic_comparison["sqrt_error"]),
                          val_format.format(topic_comparison["max_error"])])

        for topic in topic_names:
            if not topic == "Topic":
                line += "\t" + topic_comparison[topic]

        print(line)


if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser(prog="python3 " + sys.argv[0],
                                         description="Program compares statistic for labeled text and predicted text topics. " +
                                                     "Output format: File  Sqrt error  Max error  Predicted value - labeled value")
    arg_parser.add_argument("-f", "--format", choices=["values", "formulas"], default="formulas",
                            help="Output format: 'values' or 'formulas' (nice to use in Excel)")
    arg_parser.add_argument("-c", "--content", choices=["data", "metrics", "full"], default="data",
                            help="Ouput content: 'data', 'metrics' or 'full' (metrics and data - file by file comparison)")
    arg_parser.add_argument("labeled_topics_stat_file", metavar="<file with statistic for labeled topics>")
    arg_parser.add_argument("predicted_topics_stat_file", metavar="<file with statistic for predicted topics>")

    args = arg_parser.parse_args()

    # --read data--
    (header_labeled, topics_stat_labeled) = read_tsv_file(args.labeled_topics_stat_file)
    if not header_labeled.startswith("Topic"):
        sys.stderr.write("Error in file content: expected header starts with 'Topic'" + '\n')

    (header_computed, topics_stat_computed) = read_tsv_file(args.predicted_topics_stat_file)
    if not header_computed.startswith("Topic"):
        sys.stderr.write("Error in file content: expected header starts with 'Topic'" + '\n')
    topic_names = header_labeled.split("\t")

    # --compare topics--
    (metrics, _, topics_comparison) = compare_table_data(header_labeled, topics_stat_labeled,
                                                         header_computed, topics_stat_computed,
                                                         args.format == "formulas")

    # --output results--
    if args.content in ["metrics", "full"]:
        print_metrics(metrics)

    if args.content == "full":
        print("")

    if args.content in ["data", "full"]:
        print_topics_comparison(topics_comparison, topic_names)
