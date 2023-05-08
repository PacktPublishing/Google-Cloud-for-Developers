#!/bin/bash
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

# Please configure your project name and region below
PROJECT_ID="boxwood-office-375112"
REGION="us-east1"

# Do not modify anything below this line
echo "Using configured values:"
echo "PROJECT_ID=$PROJECT_ID"
echo "REGION=$REGION"
echo ""
gcloud config set project $PROJECT_ID

echo ""
echo "Deploying cloud function weatherinfo-readcitynames..."

cd readcitynames

gcloud functions deploy weatherinfo-readcitynames \
--gen2 --runtime=python310 --region=$REGION \
--memory=256MB --source=. \
--entry-point=read_city_names_trigger \
--trigger-http --allow-unauthenticated

cd ..

echo ""
echo "Deploying cloud function weatherinfo-getcityweather..."

cd getcityweather

gcloud functions deploy weatherinfo-getcityweather \
--gen2 --runtime=python310 --region=$REGION \
--memory=256MB --source=. \
--entry-point=get_city_weather_trigger \
--service-account weather-agent@boxwood-office-375112.iam.gserviceaccount.com \
--trigger-http --allow-unauthenticated

cd ..


echo ""
echo "Deploying cloud function weatherinfo-storecityweather..."

cd storecityweather

gcloud functions deploy weatherinfo-storecityweather \
--gen2 --runtime=python310 --region=$REGION \
--memory=256MB --source=. \
--entry-point=store_city_weather_trigger \
--trigger-http --allow-unauthenticated

cd ..

echo ""
echo "Deploying cloud function weatherinfo-updateweatherpage..."

cd updateweatherpage

gcloud functions deploy weatherinfo-updateweatherpage \
--gen2 --runtime=python310  --region=$REGION \
--memory=256MB --source=. \
--entry-point=update_weather_page_trigger \
--trigger-http --allow-unauthenticated

cd ..

echo "Deployment completed"