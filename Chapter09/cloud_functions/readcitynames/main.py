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

import functions_framework
import json
# Imports the Google Cloud client library
from google.cloud import storage
from google.cloud import exceptions

def get_city_list(bucket_name, city_list_path):
  """Loads A CSV file with the name of a city in each line.
  Args:
      bucket_name (string): Name of the Cloud Storage bucket containing the CSV file.
      city_list_path (string): Full path to the city list CSV inside the GCS bucket.
  Returns:
      List of city names
  """

  # Instantiate a Cloud Storage client
  storage_client = storage.Client()
  
  try:
    # Open the bucket
    bucket = storage_client.bucket(bucket_name)
    
    # And get to the blob containing our HTML template
    blob = bucket.blob(city_list_path)
  except exceptions.NotFound:
    print('ERROR: Unable to open CSV file, please check bucket and file name!')
    return []
  
  # Open the blob and return its contents
  with blob.open("r") as city_list_file:
    city_list_raw = city_list_file.readlines()
  
  city_list = []
  for line in city_list_raw:
      city_list.append(line.strip())

  print(city_list)
  return city_list

@functions_framework.http
def read_city_names_trigger(request):
  """HTTP Cloud Function.
  Args:
      request (flask.Request): The request object.
      <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
  Returns:
      The response text, or any set of values that can be turned into a
      Response object using `make_response`.
      <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
  Note:
      For more information on how Flask integrates with Cloud
      Functions, see the `Writing HTTP functions` page.
      <https://cloud.google.com/functions/docs/writing/http#http_frameworks>
  """
  bucket_name = request.json.get('bucket_name')
  city_list_path = request.json.get('city_list_path')
  print(f'Will read city list from file {city_list_path} in bucket {bucket_name}')
  return(get_city_list(bucket_name, city_list_path))

def main():
  """Main function for tests using the command line.
  """
  # Replace the sample names here with your own ones for command line testing
  bucket_name = "sampleprivate384"
  city_list_path = "input/city_list.csv"
  get_city_list(bucket_name, city_list_path)

if __name__ == "__main__":
  main()
