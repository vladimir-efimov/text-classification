# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import math

val_format = "{:3.2f}"


# Compares table data presented as dictionary, where key - entry name,
# value - list of properties for entry described by header
# Returns metrics and value-by-value comparison as list of dictionaries
def compare_table_data(header_line1, data_dict1, header_line2, data_dict2, output_formulas=False):
    dataset_comparison = []
    errors_by_property = {}
    total_sqrt_error = 0.0
    total_max_error = 0.0

    properties_indexes1 = get_property_indexes(header_line1)
    properties_indexes2 = get_property_indexes(header_line2)
    check_properties(properties_indexes1, properties_indexes2)

    properties = header_line1.split("\t")[1:]

    for property_name in properties:
        errors_by_property[property_name] = (0.0, 0.0)

    for entry_name in data_dict1:
        entry_values1 = data_dict1[entry_name]
        entry_values2 = data_dict2[entry_name]
        entry_comparison = {}

        sqrt_error = 0.0
        max_error = 0.0

        for property_name in properties:
            v1 = float(entry_values1[properties_indexes1[property_name]])
            v2 = float(entry_values2[properties_indexes2[property_name]])
            sqrt_error += (v2 - v1) * (v2 - v1)
            delta = math.fabs(v2 - v1)
            if output_formulas:
                entry_comparison[property_name] = "= " + str(v2) + " - " + str(v1)
            else:
                entry_comparison[property_name] = val_format.format(v2 - v1)

            if delta > max_error:
                max_error = delta

            (property_total_error, property_error_mean) = errors_by_property[property_name]
            property_total_error += (v2 - v1) * (v2 - v1)
            property_error_mean += v2 - v1
            errors_by_property[property_name] = (property_total_error, property_error_mean)

        sqrt_error = math.sqrt(sqrt_error)
        entry_comparison["sqrt_error"] = sqrt_error
        entry_comparison["max_error"] = max_error
        dataset_comparison.append((entry_name, entry_comparison))
        total_sqrt_error += sqrt_error
        total_max_error += max_error

    metrics = {"Total sqrt error": total_sqrt_error, "Total max error": total_max_error,
               "Average sqrt error": total_sqrt_error / len(data_dict1),
               "Average max error": total_max_error / len(data_dict2), "Property_metrics": errors_by_property}
    return metrics, dataset_comparison


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
