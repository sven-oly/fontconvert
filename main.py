#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
from flask import Flask, render_template, stream_with_context, request, Response

# https://flask.palletsprojects.com/en/2.1.x/patterns/fileuploads/
from werkzeug.utils import secure_filename

from io import BytesIO
from io import StringIO

#import cloudstorage as gcs

import os

from docx import Document

import adlamConversion

from convertDoc2 import ConvertDocx

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    who = request.url
    return 'Hello World! ' + who

@app.route('/test/')
def test():
    """Return a friendly HTTP greeting."""
    who = request.url
    return 'Testing World! ' + who

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
    try:
        doc = Document('a2_short.docx')
    except BaseException as err:
        return "Document fails %s" % (err)
    
    paragraph = doc.add_paragraph()
    run = doc.add_paragraph().add_run()
    run.text = "TEST TEXT"

    font = run.font
    font.name = 'Noto Sans Adlam'
    doc.save('test.docx')
    return 'DOC! ' + font.name

# https://pythonbasics.org/flask-upload-files
@app.route('/upload')
@app.route('/upload/')
def upload():
   who = request.host_url
   print('URL = %s' % who)
   return render_template('upload.html', base=who)

def read_file_chunks(fd):
  print('FD = %s' % fd)
  chunks = 0
  while 1:
      buf = fd.read(8192)
      print('%d BYTES %s' % (chunks, bytes))
      if buf:
          yield buf
      else:
          break
      chunks += 1
  print('READ DONE')

@app.route('/uploader', methods = ['GET', 'POST'])
@app.route('/uploader/', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']  # FileStorage object
        print('FILE = %s' % file)
        fileName = file.filename
        outFileName = os.path.splitext(fileName)[0] + '_Unicode.docx'
        print(outFileName)
        inputFileName = file.filename
        text = file.stream.read()
        data = BytesIO(text)
        count = len(text)
        print('FILE LENGTH = %s' % count)
        print('doc file = %s' % data)
        doc = Document(data)
        data.close()

        try:
            adlamConverter = adlamConversion.AdlamConverter()      
            paragraphs = doc.paragraphs
            count = len(paragraphs)
        except:
            return 'Bad Adlam converter'
        print('Created converter')

        try:
            docConverter = ConvertDocx(adlamConverter, documentIn=doc)

            print('docConverter = %s' % docConverter)
            print('%d paragraphs in input doc' % len(paragraphs))
            if docConverter:
                result = docConverter.processDocx()

                #for p in paragraphs:
                #    print('p = %s' % p.text)
                target_stream = BytesIO()
                result = doc.save(target_stream)          
                # Download resulting converted document
                # Reset the pointer to the beginning.
                target_stream.seek(0)
                #read_file_chunks(target_stream)
                headerFileName = "attachment;filename=%s" % outFileName
                headers = {
                    "Content-Disposition": headerFileName
                }
                try:
                    return Response(
                        stream_with_context(read_file_chunks(target_stream)),
                        mimetype="application/vnd.openxmlformats-officnedocument.wordprocessingml.document",
                        headers=headers
                    )
                except:
                    error = "ERROR"
                    print('**** Response failure %s' % error)
                    
        except:
            return 'Conversion failed.'
                
    return '%s file uploaded successfully with %d paragraphs' % (file.filename, count)
           
if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
