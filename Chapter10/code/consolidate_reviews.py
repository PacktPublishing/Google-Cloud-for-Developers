# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from glob import glob
import json
import ndjson
import random

# Full path to the output file
OUTPUT_FILE_NAME = "./consolidated_reviews.json"

# Number of random reviews to extract from each data file
REVIEWS_PER_LANGUAGE = 16

final_reviews = []
# Open all data files and iterate
for file_name in glob('data/*.json'):
    print("Processing file {}".format(file_name))
    lang_translations = open(file_name, 'r')
    # Read data file
    tmp_reviews = ndjson.load(lang_translations)
    # Append REVIEWS_PER_LANGUAGE random reviews to the global list
    final_reviews = final_reviews + random.sample(tmp_reviews, 
                                                REVIEWS_PER_LANGUAGE)

print("The final list has {} elements".format(len(final_reviews)))
# Dump final list, ordered randomly
random.shuffle(final_reviews)
with open(OUTPUT_FILE_NAME, 'w') as output_file:
    json.dump(final_reviews, output_file)