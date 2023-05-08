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

# Sample file to deploy the example to an App Engine instance
ORIGINAL_PWD=$PWD
if [[ $ORIGINAL_PWD != *Chapter07 ]]
then
    echo "Please run this command from the Chapter directory using 'bash setup.sh'"
    exit 1
else
    echo "Copying content from the 'third party' directory"    
    cp -pR ../third_party/Chapter07/* .
    echo "Setup is completed"
fi
