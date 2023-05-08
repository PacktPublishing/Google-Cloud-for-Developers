import functions_framework
from google.cloud import storage

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

# Name of the bucket storing the template files
# Please replace this with your own random name
BUCKET_NAME = "resume_xew878w6e"
DEFAULT_TEMPLATE_NAME = "english.html"

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

@functions_framework.http
def return_resume_trigger(request):
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
  template = request.args.get('template', DEFAULT_TEMPLATE_NAME)
  name = request.args.get('name')
  company = request.args.get('company')
  return(return_resume(template, name, company))

def main():
  """Main function for tests using the command line.
  """
  template = "english.html"
  name = "John Smith"
  company = "StarTalent"
  resume_html = return_resume(template, name, company)
  print(resume_html)

if __name__ == "__main__":
  main()
