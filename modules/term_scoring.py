# Copyright (c) 2020, Vladimir Efimov
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import math

def get_term_score(count, term_documents, num_documents):
    return float(count) * math.log10(1.0 + float(num_documents) / float(term_documents))
