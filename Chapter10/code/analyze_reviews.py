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

from google.cloud import language_v1 as language
from google.cloud import translate_v2 as translate

import json
import pandas as pd

REVIEW_LIST_FILE_NAME = "./consolidated_reviews.json"
TARGET_LANGUAGE = "en"

# Load consolidated_reviews.json from disk
review_file = open(REVIEW_LIST_FILE_NAME, 'r')
review_list = json.load(review_file)

# Re-use clients to speed up execution
language_client = language.LanguageServiceClient() 
translate_client = translate.Client() 

# Associate a global score to each identied name
global_score = {}

# Iterate through all 96 reviews
total_reviews = len(review_list)
current_review = 1
for review_data in review_list:
    print("[{}/{}] Starting analysis for review".format(current_review, total_reviews))
    print("- Original review text: {}".format(review_data['review_body']))

    # Translate reviews to the target language only if required
    source_language = review_data['language']
    if source_language == TARGET_LANGUAGE:
        print("- Source and target languages are the same, translation not required")
        review_data["translated_body"] = review_data["review_body"]
    else:
        print("- Translating the review from {} to {}".format(source_language, TARGET_LANGUAGE))

        translate_result = translate_client.translate(
            review_data['review_body'],  
            target_language=TARGET_LANGUAGE
        )

        review_data["translated_body"] = translate_result["translatedText"]
        print("- Review translated to: {}". format(review_data["translated_body"]))
  
    # Run an Entity Sentiment Analysis for each review body
    lang_document_type = language.Document.Type.PLAIN_TEXT 
    lang_encoding_type = language.EncodingType.UTF8 

    lang_document = {
        "content": review_data["translated_body"],
        "type": lang_document_type,
        "language": TARGET_LANGUAGE
    } 

    # We will use text annotation to request two features simultaneously:
    # syntax and document sentiment analysis
    lang_features = {
        "extract_syntax": True,
        "extract_document_sentiment": True
    }

    language_result = language_client.annotate_text( 
        request={
            "document": lang_document, 
            "encoding_type": lang_encoding_type,
            "features": lang_features
        } 
    ) 

    # Create list of nouns
    noun_list = set()
    for token_info in language_result.tokens:
        token_text = token_info.text.content.lower()
        token_type = token_info.part_of_speech.tag
        if token_type == 6: # If it’s a NOUN 
            if token_text not in noun_list:
                noun_list.add(token_text)

    # Find nouns in sentences and update their global score
    for sentence_info in language_result.sentences:
        sentence_text = sentence_info.text.content
        magnitude = sentence_info.sentiment.magnitude
        score = sentence_info.sentiment.score
        sentence_score = magnitude * score
        print("+ Sentence score is {} * {} = {}".format(magnitude, score, sentence_score))

        word_list = sentence_text.split()
        for word in word_list:
            word = word.lower()
            if word in noun_list:
                print("* Score for {} modified by {}".format(word, sentence_score))
                if word in global_score:
                    global_score[word] = global_score[word] + sentence_score
                else:
                    global_score[word] = sentence_score
    print("*****************************")
    current_review = current_review + 1

# Print the top and bottom 10 nouns ordered by global score
ordered_scores = pd.DataFrame(global_score.items(), columns=['word', 'score']).sort_values(by='score', ascending=False)
print("TOP 10 Nouns with the highest scores:")
print(ordered_scores.head(10))
print("\nBOTTOM 10 Nouns with the lowest scores:")
print(ordered_scores.tail(10))