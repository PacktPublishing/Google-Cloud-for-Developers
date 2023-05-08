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

from google.cloud import secretmanager
from google.api_core import exceptions
import functions_framework
import requests

# API Endpoint
URL = "http://api.weatherapi.com/v1/current.json"

def return_cityweather(project_id, city_name, api_key = None):
  """Requests and returns the weather for specific city using an external API.
  Args:
      project_id (string): If of the Cloud Project storing the secret.
      city_name (string): Name of the city to get the weather for.
      api_key (string): API Key to use in remote requests, if set.
  Returns:
      Weather data information in JSON format or empty if errors happened.
  """
  # Get API key from Secret Manager if it wasn't passed as a parameter
  if not api_key:
    print('Getting API Key from Secret Manager')
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the latest version of our secret to retrieve.
    # Notice that both secret name and version are harcoded (the latter using an alias)
    secret_name = f'projects/{project_id}/secrets/weatherapi_key/versions/latest'
    print(f'Will try to access secret with name {secret_name}')

    try: 
        # Access the secret version.
        result = client.access_secret_version(request={'name': secret_name})    
    except exceptions.PermissionDenied:
        print("ERROR: Function does not have access to the secret, please check permissions!")
        return "Permission Denied"
    api_key = result.payload.data
    print(f'Using API KEY {api_key} to query weather for {city_name}')

  # q contains the name of the city and key the API key
  # aqi can be set to 'yes' to include air quality information in the response
  PARAMS = {'q': city_name,
            'aqi': 'no',
	  	    'key': api_key
           }

  try:
    r = requests.get(url = URL, params = PARAMS)
    cityWeatherDetails = r.json()	
  except requests.exceptions.RequestException as e:
    # Print information about exception and return an empty JSON dict
    print(e)
    cityWeatherDetails = {}
  
  if 'error' in cityWeatherDetails:
      print('ERROR CODE {code}: {message}'.format(code=cityWeatherDetails['error']['code'], message=cityWeatherDetails['error']['message']))
      cityWeatherDetails = {}
  print(cityWeatherDetails)
  return cityWeatherDetails


@functions_framework.http
def get_city_weather_trigger(request):
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
  print(request.args)
  city_name = request.json.get('city_name')
  project_id = request.json.get('project_id')
  return(return_cityweather(project_id, city_name))

def main():
  """Main function for tests using the command line.
  """
  project_id = 'cloud-developers-365616'
  city_name = 'London'
  api_key = None
  return_cityweather(project_id, city_name, api_key)

if __name__ == "__main__":
  main()
