# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import math

val_format = "{:3.2f}"
percentage_format = "{:3.2f}%"
formula_format = "= {:3.2f} - {:3.2f}"
formula_percentage_format = "= {:3.2f}% - {:3.2f}%"


# Compares table data presented as dictionary, where key - entry name,
# value - list of values for entry for each property listed in header
# value for entry could be string represented float or in percentage value
# Returns metrics, errors by property and value-by-value comparison as list of dictionaries
def compare_table_data(header_line1, data_dict1, header_line2, data_dict2, output_formulas=False):
    dataset_comparison = []
    metrics_per_property = {}
    total_sqrt_error = 0.0
    total_max_error = 0.0

    properties_indexes1 = get_property_indexes(header_line1)
    properties_indexes2 = get_property_indexes(header_line2)
    check_properties(properties_indexes1, properties_indexes2)

    properties = header_line1.split("\t")[1:]

    for property_name in properties:
        metrics_per_property[property_name] = (0.0, 0.0)

    for entry_name in data_dict1:
        entry_values1 = data_dict1[entry_name]
        entry_values2 = data_dict2[entry_name]
        entry_comparison = {}

        sqrt_error = 0.0
        max_error = 0.0

        for property_name in properties:
            v1str = entry_values1[properties_indexes1[property_name]]
            v1 = float(v1str) if not str(v1str).endswith("%") else float(v1str.replace('%', '')) / 100.0
            v2str = entry_values2[properties_indexes2[property_name]]
            v2 = float(v2str) if not str(v2str).endswith("%") else float(v2str.replace('%', '')) / 100.0
            sqrt_error += (v2 - v1) * (v2 - v1)
            delta = math.fabs(v2 - v1)

            if output_formulas:
                if v1str.endswith("%") or v2str.endswith("%"):
                    entry_comparison[property_name] = formula_percentage_format.format(v2 * 100.0, v1 * 100.0)
                else:
                    entry_comparison[property_name] = formula_format.format(v2, v1)
            else:
                if v1str.endswith("%") or v2str.endswith("%"):
                    entry_comparison[property_name] = percentage_format.format((v2 - v1) * 100.0)
                else:
                    entry_comparison[property_name] = val_format.format(v2 - v1)

            if delta > max_error:
                max_error = delta

            (property_total_error, property_error_mean) = metrics_per_property.get(property_name)
            property_total_error += (v2 - v1) * (v2 - v1)
            property_error_mean += v2 - v1
            metrics_per_property[property_name] = (property_total_error, property_error_mean)

        sqrt_error = math.sqrt(sqrt_error)
        entry_comparison["sqrt_error"] = sqrt_error
        entry_comparison["max_error"] = max_error
        dataset_comparison.append((entry_name, entry_comparison))
        total_sqrt_error += sqrt_error
        total_max_error += max_error

    metrics = {"Total sqrt error": total_sqrt_error, "Total max error": total_max_error,
               "Average sqrt error": total_sqrt_error / len(data_dict1),
               "Average max error": total_max_error / len(data_dict1)}
    return metrics, metrics_per_property, dataset_comparison


def get_property_indexes(header_line):
    properties = header_line.split("\t")
    properties_indexes = {}
    i = -1
    for property_name in properties:
        if i < 0:
            i = i + 1
            continue
        properties_indexes[property_name] = i
        i = i + 1
    return properties_indexes


def check_properties(properties_indexes1, properties_indexes2):
    for property_name in properties_indexes1:
        if property_name not in properties_indexes2:
            raise ValueError("'" + property_name + "' only in first dataset")
    for property_name in properties_indexes2:
        if property_name not in properties_indexes2:
            raise ValueError("'" + property_name + "' only in second dataset")
