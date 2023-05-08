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
# Imports the Google Cloud client library
from google.cloud import datastore
from google.cloud import exceptions

def store_city_weather(project_id, city_name, city_weather_details):
  """Loads A CSV file with the name of a city in each line.
  Args:
      project_id (string): ID of the Cloud project where data will be stored.
      city_name (string): Name of the city to update the weather for.
      city_weather_details (string): Updated weather data for the city.
  Returns:
      True if success, False if errors happened
  """

  # Instantiate a Datastore client
  datastore_client = datastore.Client(project=project_id)

  try:
    # The kind for the new entry
    kind = 'city_weather'

    # The Cloud Datastore key for the new entry
    city_weather_details_key = datastore_client.key(kind, city_name)

    # Prepares the new entity
    weather_details = datastore.Entity(key=city_weather_details_key)
    weather_details['weather_details'] = city_weather_details

    # Saves the entity
    datastore_client.put(weather_details)

  except Exception as ex:
    print('Exception: ' + str(ex))
    return "Error"
  
  print('Success!')
  return "Sucess"

@functions_framework.http
def store_city_weather_trigger(request):
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
  city_name = request.json.get('city_name')
  city_weather_details = request.json.get('city_weather_details')
  return(store_city_weather(project_id, city_name, city_weather_details))

def main():
  """Main function for tests using the command line.
  """
  # Replace the sample names here with your own ones for command line testing
  project_id = 'cloud-developers-365616'
  city_name = 'London'
  city_weather_details = {
    "location": {
        "name": "London",
        "region": "City of London, Greater London",
        "country": "United Kingdom",
        "lat": 51.52,
        "lon": -0.11,
        "tz_id": "Europe/London",
        "localtime_epoch": 1671269529,
        "localtime": "2022-12-17 9:32"
    },
    "current": {
        "last_updated_epoch": 1671269400,
        "last_updated": "2022-12-17 09:30",
        "temp_c": -1.0,
        "temp_f": 30.2,
        "is_day": 1,
        "condition": {
            "text": "Sunny",
            "icon": "//cdn.weatherapi.com/weather/64x64/day/113.png",
            "code": 1000
        },
        "wind_mph": 2.2,
        "wind_kph": 3.6,
        "wind_degree": 176,
        "wind_dir": "S",
        "pressure_mb": 1023.0,
        "pressure_in": 30.21,
        "precip_mm": 0.0,
        "precip_in": 0.0,
        "humidity": 86,
        "cloud": 0,
        "feelslike_c": -3.4,
        "feelslike_f": 25.9,
        "vis_km": 10.0,
        "vis_miles": 6.0,
        "uv": 1.0,
        "gust_mph": 8.5,
        "gust_kph": 13.7
    }
  }
  store_city_weather(project_id, city_name, city_weather_details)

if __name__ == "__main__":
  main()
