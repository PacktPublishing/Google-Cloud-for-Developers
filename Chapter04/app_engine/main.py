#!/usr/bin/env python
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


from flask import request, current_app, Flask
from google.cloud import storage
import google.cloud.logging
import logging

# Name of the bucket storing the template files
# Please replace this with your own random name
BUCKET_NAME = "resume_xew878w6e"
DEFAULT_TEMPLATE_NAME = "english.html"

app = Flask(__name__)
app.debug = False
app.testing = False

# Configure logging
if not app.testing:
    logging.basicConfig(level=logging.INFO)
    client = google.cloud.logging.Client()
    # Attaches a Cloud Logging handler to the root logger
    client.setup_logging()

def load_resume(template):
  """Loads the raw HTML of the resume from a predefined file.
  Args:
      template (string): File name of the template to use.  
  Returns:
      Full raw HTML of the resume.
  """

  # Instantiate a Cloud Storage client
  storage_client = storage.Client()
  
  # Open the bucket
  bucket = storage_client.bucket(BUCKET_NAME)
  
  # And get to the blob containing our HTML template
  blob = bucket.blob(template)
  
  # Open the blob and return its contents
  with blob.open("r") as resume_file:
    current_app.logger.info(
        'Loading template file %s.', template)
    return(resume_file.read())

def build_resume_header(name, company):
  """Builds the customized header for the resume.
  Args:
      name (string): Name of the person receiving the resume.
      company (string): Company receiving the resume.
  Returns:
      Customized header for the resume.
  """
  custom_header = ""
  if name or company:
    custom_header = "(Specially prepared for "
    if name:
      custom_header = custom_header + "<strong>" + name + "</strong>"
    if company:
      if not name:
        custom_header = custom_header + "<strong>" + company + "</strong>"
      else:
        custom_header = custom_header + " from <strong>" + company + "</strong>"
    custom_header = custom_header + ")"
  return custom_header

def replace_resume_header(resume_html, header_text):
  """Loads the resume, replaces the header and returns it.
  Args:
      resume_html (string): Full raw HTML of the resume.
      header_text (string): Text to be used as customized header.
  Returns:
      The full resume, in HTML format.
  """
  return resume_html.replace("##RESUME_HEAD##", header_text)

def return_resume(template, name, company):
  """Loads the resume, replaces the header and returns it.
  Args:
      template (string): File name of the template to use.
      name (string): Name of the person receiving the resume.
      company (string): Company receiving the resume.
  Returns:
      The full resume, in HTML format.
  """
  resume_html = load_resume(template)
  resume_header = build_resume_header(name, company)
  resume_html = replace_resume_header(resume_html, resume_header)
  return resume_html

@app.route('/')
def get():
  """Receives the GET request and returns the resume in HTML format.
  """  
  template = request.args.get('template', DEFAULT_TEMPLATE_NAME)
  name = request.args.get('name', None)
  company = request.args.get('company', None)
  resume_html = return_resume(template, name, company)
  return resume_html

# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8080, debug=True)