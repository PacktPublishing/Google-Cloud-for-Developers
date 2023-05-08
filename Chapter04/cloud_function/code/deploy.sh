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

# This is a sample file showing how to deploy the cloud function
# Just fill in your Google Cloud project name in the following line

PROJECT_NAME="boxwood-office-375112"

# Do not edit below this line

gcloud config set project $PROJECT_NAME

gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable run.googleapis.com

echo "If this is your first run, it may take 5 minutes before the APIs are available"
read -p "Wait for a few minutes and press enter to continue..."

gcloud functions deploy resume-server \
--gen2 \
--runtime=python310 \
--region=us-central1 \
--memory=256MB \
--source=. \
--entry-point=return_resume_trigger \
--trigger-http \
--allow-unauthenticated
