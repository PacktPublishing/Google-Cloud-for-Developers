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
from google.cloud import datastore
from google.cloud import storage
from google.cloud import exceptions

HTML_HEADER ="""
<HTML>
<HEAD>
<STYLE>
h2 {
  font-family: Arial, Helvetica, sans-serif;
}

#forecast {
  font-family: Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

#forecast td, #forecast th {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

#forecast td img { 
  vertical-align: middle;
}

#forecast tr:nth-child(even){background-color: #f2f2f2;}

#forecast tr:hover {background-color: #ddd;}

#forecast th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: center;
  background-color: #04AA6D;
  color: white;
}
</STYLE>
<TITLE>Weather forecast by city</TITLE>
</HEAD>
<BODY>
<H2>Weather forecast by city</H2>
<TABLE ID="forecast">
<TR>
<TH>City Name</TH>
<TH>Current Weather</TH>
<TH>Temperature (Celsius)</TH>
<TH>Feels Like (Celsius)</TH>
<TH>Temperature (Farenheit)</TH>
<TH>Feels Like (Farenheit)</TH>
<TH>Country Name</TH>
<TH>Last Update</TH>
</TR>"""

HTML_FOOTER ="""
</TABLE>
</BODY>
</HTML>
"""


def update_weather_page(project_id, bucket_name, html_path):
  """Gets all weather entities, builds a HTML page and stores it in GCS.
  Args:
      project_id (string): ID of the Cloud project where data is stored.
      bucket_name (string): Name of the bucket containing the page to update.
      html_path (string): Relative path to the html file to update.
  Returns:
      True if success, False if errors happened
  """
  html_content = HTML_HEADER
  # Instantiate a Datastore client
  datastore_client = datastore.Client(project=project_id)

  try:
    # The kind for the new entry
    query = datastore_client.query(kind='city_weather')

    # The Cloud Datastore key for the new entry
    weatherdata_list = query.fetch()
  except Exception as ex:
    print('Exception: ' + str(ex))
    return "Error"

  print('Building HTML file')
  for entity in weatherdata_list:
      weather_info = json.loads(json.dumps(entity), parse_int=str)
      city_name = weather_info['weather_details']['body']['location']['name']
      country_name = weather_info['weather_details']['body']['location']['country']
      temp_c = weather_info['weather_details']['body']['current']['temp_c']
      feelslike_c = weather_info['weather_details']['body']['current']['feelslike_c']
      temp_f = weather_info['weather_details']['body']['current']['temp_f']
      feelslike_f = weather_info['weather_details']['body']['current']['feelslike_f']
      text = weather_info['weather_details']['body']['current']['condition']['text']
      icon = 'https:' + weather_info['weather_details']['body']['current']['condition']['icon']
      last_updated = weather_info['weather_details']['body']['current']['last_updated']
      time_zone = weather_info['weather_details']['body']['location']['tz_id']
      
      row_data = f"""
       <TR>
       <TD><STRONG>{city_name}</STRONG></TD>
       <TD><IMG SRC="{icon}">&nbsp;{text}</TD>
       <TD>{temp_c} &deg;C</TD>
       <TD>{feelslike_c} &deg;C</TD>
       <TD>{temp_f} &deg;F</TD>
       <TD>{feelslike_f} &deg;F</TD>
       <TD>{country_name}</TD>
       <TD>{last_updated} ({time_zone})</TD>
       </TR>\n
      """
      html_content += row_data
  html_content += HTML_FOOTER
    
  # Write HTML file to cloud storage
  print('Writing file to Cloud Storage')
  # Instantiate a Cloud Storage client
  storage_client = storage.Client()
  
  try:
    # Open the bucket
    bucket = storage_client.bucket(bucket_name)
    
    # And get to the blob containing our HTML template
    blob = bucket.blob(html_path)

    with blob.open("w") as f:
      f.write(html_content)

    # Set content-type to enable direct download and no caching
    blob.content_type = 'text/html'
    blob.cache_control = 'no-store'
    blob.patch()
    # Make blob public. This will fail in buckets with uniform ACL
    blob.make_public()
    print(f"HTML file {blob.name} is publicly accessible at {blob.public_url}")    

  except exceptions.NotFound:
    print('ERROR: Unable to create HTML file, check bucket and file name!')
    return "Error"

  print('Success!')
  return "Sucess"

@functions_framework.http
def update_weather_page_trigger(request):
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
  project_id = request.json.get('project_id')
  bucket_name = request.json.get('bucket_name')
  html_path = request.json.get('html_path')
  return(update_weather_page(project_id, bucket_name, html_path))

def main():
  """Main function for tests using the command line.
  """
  # Replace the sample names here with your own ones for command line testing
  project_id = 'cloud-developers-365616'
  bucket_name = 'samplepublic134'
  html_path = 'weather_by_city.html'
  update_weather_page(project_id, bucket_name, html_path)

if __name__ == "__main__":
  main()