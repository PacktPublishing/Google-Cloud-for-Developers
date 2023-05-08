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
"""Basic implementation of a phonebook.

Basic web-based phonebook implemented using Flask. Each contact has two 
fields: name and phone number. The home page will list all contacts sorted by
name together with a form to add new entries. Each contact is listed with a
button to delete it.
"""
import os
import sqlalchemy
from flask import Flask
from flask import request
from sqlalchemy.ext.automap import automap_base


HTML_TEMPLATE = """
    <HTML>
    <HEAD><TITLE>Phonebook running on GKE</TITLE></HEAD>
    <STYLE>
    html {
      font-family: 'helvetica neue', helvetica, arial, sans-serif;
    }
    a:link, a:visited {
      background-color: green;
      color: white;
      border: 2px solid grey;
      padding: 10px 20px;
      text-align: center;
      text-decoration: none;
      display: inline-block;
    }
    </STYLE>
    <BODY>
    <H2 style="color:###COLOR###;">###MESSAGE###</H2><BR>
    <A HREF="/">Click here to return to the home screen</A>
    </BODY>
    </HTML>
"""

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")

pool = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL.create(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_pass,
        host="127.0.0.1",
        port="3306",
        database="phonebook",
    ),
)

def html_list(results):
  """Function to return the database connection object.

  Args:
    results: List of rows containing phonebook entries.
  Returns:
    HTML for the main page listing all phonebook entries.
  """
  html = """
  <HTML>
  <HEAD><TITLE>Phonebook running on GKE</TITLE></HEAD>
  <STYLE>
  html {
    font-family: 'helvetica neue', helvetica, arial, sans-serif;
  }

  table {
    table-layout: fixed;
    border-collapse: collapse;
    border: 1px solid green;
  }

  th, td {
    padding: 10px;
    border: 1px solid green;
    letter-spacing: 1px;
  }

  h2, th {
    color: green;
  }

  input[type=submit] {
    color: white;
    background-color: green;
    text-decoration: none;
    padding: 10px;
  }
  </STYLE>
  <BODY>
  <H2>Phonebook entries:</H2>
  ###PHONEBOOK-LIST###
  <H2>Add new entry:</H2>
  <FORM ACTION="/add" METHOD="POST">
    <LABEL FOR="name">Name:</LABEL><BR>
    <INPUT TYPE="text" ID="name" NAME="name"><BR>
    <LABEL FOR="number">Phone Number:</LABEL><BR>
    <INPUT TYPE="text" ID="number" NAME="number"><BR><BR>
    <INPUT TYPE="submit" VALUE="Add new entry">
  </FORM>
  </BODY>
  </HTML>
  """

  list_html = ""
  if results:
    list_html += "<TABLE>\n"
    list_html += "<TR><TH>Name</TH><TH>Phone Number</TH><TH>Actions</TH></TR>"
    for row in results:
      row_html = "<TR>\n"
      row_html += "<TD>{name}</TD>\n".format(name=row[1])
      row_html += "<TD>{number}</TD>\n".format(number=row[2])
      row_html += "<TD><FORM ACTION='/delete' METHOD='POST'>\n"
      row_html += "<INPUT TYPE='hidden' NAME='id' VALUE='{id}'>\n".format(
          id=row[0])
      row_html += "<INPUT TYPE='submit' VALUE='Delete entry'>\n"
      row_html += "</FORM></TD>\n"
      row_html += "</TD>\n"
      row_html += "</TR>\n"
      list_html += row_html
    list_html += "</TABLE>\n"
  return html.replace("###PHONEBOOK-LIST###", list_html)


def html_ok(message):
  html = HTML_TEMPLATE.replace("###COLOR###", "green")
  return html.replace("###MESSAGE###", message)


def html_error(message):
  html = HTML_TEMPLATE.replace("###COLOR###", "red")
  return html.replace("###MESSAGE###", message)

app = Flask(__name__)


def print_phonebook():
  """Function to return the database connection object.

  Returns:
    HTML of the list containing all entries in the phonebook.
  """
  # connect to connection pool
  with pool.connect() as db_conn:
    # create phonebook data table if it doesn't exist
    if not sqlalchemy.inspect(pool).has_table("phonebook_data"):
        meta = sqlalchemy.MetaData()
        Phonebook = sqlalchemy.Table(
            "phonebook_data", meta, 
            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key = True), 
            sqlalchemy.Column("name", sqlalchemy.String(255)), 
            sqlalchemy.Column("phone_number", sqlalchemy.String(255)),
        )
        meta.create_all(pool)

    # Prepare reference to existing table
    Base = automap_base()
    Base.prepare(pool, reflect=True)
    Phonebook = Base.classes.phonebook_data
    # query and fetch ratings table
    select_stmt = sqlalchemy.select(Phonebook)
    results = db_conn.execute(select_stmt).fetchall()
    return html_list(results)


def add_entry(new_name, new_number):
  # Prepare reference to existing table
  Base = automap_base()
  Base.prepare(pool, reflect=True)
  Phonebook = Base.classes.phonebook_data
  # connect to connection pool
  with pool.connect() as db_conn:
    # insert data into our phonebook table
    insert_stmt = (
      sqlalchemy.insert(Phonebook).
      values(name=new_name, phone_number=new_number)
    )    
    # insert entries into table
    db_conn.execute(insert_stmt)
    db_conn.commit()


def delete_entry(entry_id):
  # Prepare reference to existing table
  Base = automap_base()
  Base.prepare(pool, reflect=True)
  Phonebook = Base.classes.phonebook_data
  # connect to connection pool
  with pool.connect() as db_conn:
    # delete entry from our phonebook table
    delete_stmt = (
        sqlalchemy.delete(Phonebook).
        where(Phonebook.id == entry_id)
    )
    # insert entries into table
    db_conn.execute(delete_stmt)
    db_conn.commit()

@app.route("/")
def print_phonebook_worker():
  content = print_phonebook()
  return(content)


@app.route("/add", methods=["POST"])
def add_entry_worker():
  new_name = request.values.get("name")
  new_number = request.values.get("number")
  if new_name and new_number:
    add_entry(new_name, new_number)
    return html_ok("Entry was successfully added")
  else:
    return html_error("You must specify a name and a number")


@app.route("/delete", methods=["POST"])
def delete_entry_worker():
  entry_id = request.values.get("id")
  if entry_id and entry_id.isdigit():
    delete_entry(entry_id)
    return html_ok("Entry was successfully deleted")
  else:
    return html_error("You must specify a valid entry ID to delete")

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
