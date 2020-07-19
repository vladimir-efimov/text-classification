# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import sys
import math
import argparse
sys.path.append('modules')

val_format="{:3.2f}"

def read_topics(filename):
    f = open(filename)
    header = f.readline().strip()

    # data stored in format: file name -> topics
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


def compare_topics(topics_labeled, topics_computed, topic_names, topics_labeled_indeces, topics_computed_indeces, format):
    topics_comparison = []
    total_sqrt_error = 0.0
    total_max_error = 0.0

    topic_errors = {}
    for topic in topic_names:
        if topic == "File":
            continue
        topic_errors[topic] = (0.0, 0.0)

    for textname in topics_labeled:
        text_topics_computed = topics_computed[textname]
        text_topics_labeled = topics_labeled[textname]
        topic_comparison = {}

        sqrt_error = 0.0
        max_error = 0.0
        line = ""

        for topic in topic_names:
            if topic == "File":
                topic_comparison["File"] = text_topics_labeled[topics_labeled_indeces[topic]]
                continue
            v1 = float(text_topics_labeled[topics_labeled_indeces[topic]])
            v2 = float(text_topics_computed[topics_computed_indeces[topic]])
            sqrt_error += (v2 - v1) * (v2 - v1)
            delta = math.fabs(v2 - v1)
            if format == "values":
                topic_comparison[topic] = val_format.format(v2 - v1)
            else:
                topic_comparison[topic] = "= " + str(v2) + " - " + str(v1)

            if delta > max_error:
                max_error = delta

            (topic_total_error, topic_error_mean) = topic_errors[topic]
            topic_total_error += (v2 - v1) * (v2 - v1)
            topic_error_mean += v2 - v1
            topic_errors[topic] = (topic_total_error, topic_error_mean)


        sqrt_error = math.sqrt(sqrt_error)
        topic_comparison["sqrt_error"] = sqrt_error
        topic_comparison["max_error"] = max_error
        topics_comparison.append(topic_comparison)
        total_sqrt_error += sqrt_error
        total_max_error += max_error

    metrics = {}
    metrics["Total sqrt error"] = total_sqrt_error
    metrics["Total max error"] = total_max_error
    metrics["Average sqrt error"] = total_sqrt_error / len(topics_labeled)
    metrics["Average max error"] = total_max_error / len(topics_labeled)
    metrics["topics_metrics"] = topic_errors
    return (metrics, topics_comparison)


def print_metrics(metrics):
    for metric in metrics:
        if metric == "topics_metrics":
            continue
        print(metric + "\t" + str(metrics[metric]))
    print("")
    print("Topic\tSqrt error\tError mean (>0 - predicted more than labeled)")
    for topic in metrics["topics_metrics"]:
        (topic_total_error, topic_error_mean) = metrics["topics_metrics"][topic]
        print("\t".join([topic,str(topic_total_error),str(topic_error_mean)]))


def print_topics_comparison(topics_comparison, topics_names):
    # --print header--
    header_line = "File\tSqrt Error\tMax Error"

    for topic in topics_names:
        if not topic == "File":
            header_line += "\t" + topic
    print(header_line)

    # --print comparison--
    for topic_comparison in topics_comparison:
        line = "\t".join([topic_comparison["File"], val_format.format(topic_comparison["sqrt_error"]),
               val_format.format(topic_comparison["max_error"])])

        for topic in topic_names:
            line += "\t" + topic_comparison[topic]

        print(line)


if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser(prog = "python3 " + sys.argv[0],
        description = "Program compares labeled text topics and predicted text topics. " +
                      "Output format: File  Sqrt error  Max error  Predicted value - labeled value")
    arg_parser.add_argument("-f", "--format", choices = ["values", "formulas"], default = "formulas",
        help = "Output format: 'values' or 'formulas' (nice to use in Excel)")
    arg_parser.add_argument("-c", "--content", choices = ["data", "metrics", "full"], default = "data",
        help = "Ouput content: 'data', 'metrics' or 'full' (metrics and data - file by file comparison)")
    arg_parser.add_argument("labeled_topics_file", metavar="<file with labeled topics>")
    arg_parser.add_argument("predicted_topics_file", metavar = "<file with predicted topics>")

    args = arg_parser.parse_args()

    # --read data--
    (header_labeled, topics_labeled) = read_topics(args.labeled_topics_file)
    (header_computed, topics_computed) = read_topics(args.predicted_topics_file)

    # note: order of topics in labeled file may differs from topics in file with predicted topics
    topics_labeled_indeces = get_topic_indeces(header_labeled)
    topics_computed_indeces = get_topic_indeces(header_computed)
    if not check_topics(topics_labeled_indeces, topics_computed_indeces):
        sys.stderr.write("Mistmatch of topics set in labeled topics and predicted topics\n");
        exit(1)

    # --compare topics--
    topic_names = header_labeled.split("\t")
    (metrics, topics_comparison) = compare_topics(topics_labeled, topics_computed, topic_names,
                                                  topics_labeled_indeces, topics_computed_indeces, args.format)

    #--output results--
    if args.content in ["metrics", "full"]:
        print_metrics(metrics)

    if args.content == "full":
        print("")

    if args.content in ["data", "full"]:
        print_topics_comparison(topics_comparison, topic_names)

