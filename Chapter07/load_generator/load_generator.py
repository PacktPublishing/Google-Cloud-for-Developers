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

import os
import random
import requests
import time

def load_generator():
    while 1>0:
        hostname = os.getenv("FRONTEND_ADDR", "localhost")
        some_seconds = random.randint(1, 5)
        if some_seconds < 2:
            load_url = "http://{}/".format(hostname)
        else:
            which_sheep = random.randint(1, 12)
            if which_sheep < 10:
                load_url = "http://{}/product/electric-sheep0{}".format(hostname, which_sheep)
            else:
                load_url = "http://{}/product/electric-sheep{}".format(hostname, which_sheep)

        try:
            response = requests.head(load_url)
            print("{} returned status code {}".format(load_url, response.status_code))
        except requests.ConnectionError:
            print("Load Generator failed to connect to {}".format(load_url))
        time.sleep(some_seconds)
if __name__ == '__main__':
    load_generator()