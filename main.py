# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask, render_template, request
#from werkzeug import secure_filename

from google.appengine.api import app_identity


from docx import Document

import adlamConversion
import convertOfficeAdlam
import convertOffice


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    who = app_identity.get_default_version_hostname()
    return 'Hello World! ' + who

@app.route('/test/')
def test():
    """Return a friendly HTTP greeting."""
    return 'Testing World!'

@app.route('/adlm/')
def convertAdlam():
    """Convert Adlam fonts to Unicode."""
    converter = adlamConversion.converter()
    converter.setLowerMode(True)
    converter.setSentenceMode(True)
    inPath = 'a2_online.docx'
    outPath = 'output'
    convertOffice.convertOffice(inPath, outPath,
                                converter, version=2)
    return 'Converted to %s' % outPath
    
    
@app.route('/doc/')
def doc1():
    """Return a friendly HTTP greeting."""
    doc = Document('a2_short.docx')
    paragraph = doc.add_paragraph()
    run = doc.add_paragraph().add_run()
    run.text = ' = "”𞤱𞤭𞤲𞤣𞤫𞤲 𞤶𞤢𞤲𞤺𞤫𞤲 𞤫 𞤸𞤢𞥄𞤤𞤢 𞤨𞤵'

    font = run.font
    font.name = 'Noto Sans Adlam'
    doc.save('test.docx')
    return 'DOC! ' + font.name

# https://pythonbasics.org/flask-upload-f
@app.route('/upload')
def upload():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      # f.save(secure_filename(f.filename))
      f.save(f.filename)
      return '%s file uploaded successfully' % f.filename


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
