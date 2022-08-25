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

import threading
import time

#import cloudstorage as gcs

import os

from docx import Document
from docx.enum.style import WD_STYLE_TYPE


import adlamConversion

from convertDoc2 import ConvertDocx

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def hello():
    """Top of the conversion application."""
    who = request.url
    return render_template('main.html', base=who)


# https://pythonbasics.org/flask-upload-files
@app.route('/upload/adlam')
def upload():
   who = request.host_url
   scriptIndex = request.args.get('scriptIndex', 0)
   return render_template('upload.html',
                          base=who,
                          scriptIndex=scriptIndex
   )

# Global
msgToSend = 'First Message'
countSent = 0

def read_file_chunks(fd):
  chunks = 0
  while 1:
      buf = fd.read(8192)
      if buf:
          yield buf
      else:
          break
      chunks += 1
  if app.debug:
      progressFn('Download complete')

# Simple output function for tracking processing
def progressFn(msg):
    global msgToSend
    global countSent
    if app.debug:
        print('PROGRESS: %s' % msg)
    msgToSend = msg
    countSent = 1
    
def findDocFonts(doc):
    fontsFound = {}
    if not doc:
        return fontsFound

    if doc.paragraphs:
        fontsFound = getFontsInParagraphs(doc.paragraphs, fontsFound)

    for table in doc.tables:
        rows = table.rows
        for row in rows:
            for cell in row.cells:
                paragraphs = cell.paragraphs
                fontsFount = getFontsInParagraphs(cell.paragraphs, fontsFound)

    sections = doc.sections
    for section in sections:
        try:
            header = section.header
            fontsFound = getFontsInParagraphs(header.paragraphs, fontsFound)
        except:
            pass
        try:
            footer = section.footer
            fontsFound = getFontsInParagraphs(footer.paragraphs, fontsFound)
        except:
            pass

    return fontsFound


def getFontsInParagraphs(paragraphs, fonts):
    for p in paragraphs:
        for r in p.runs:
            font = r.font.name
            if font in fonts:
                fonts[font] += 1
            else:
                fonts[font] = 1
    return fonts
            
#https://tedboy.github.io/flask/generated/flask.stream_with_context.html
@app.route('/uploader/', methods = ['GET', 'POST'])
def upload_file():
    convertDoc = False
    if request.method == 'POST':
        formData = request.form.to_dict()
        #print('FORMDATA = %s' % formData)
        if 'ConvertToUnicode' in formData:
            # DO THE CONVERSION
            convertDoc = True

        try:
            lang = formData['lang']
        except:
            lang = 'Fula'

        file = request.files['file']  # FileStorage object
        fileName = file.filename
        if not fileName:
            who = '/upload/adlam'
            return render_template('nofileselected.html', who=who)
            
        outFileName = os.path.splitext(fileName)[0] + '_Unicode.docx'
        inputFileName = file.filename

        doc, count = createDocFromFile(file)

        if not convertDoc:
            # Just show information.
            fontsFound = findDocFonts(doc)

            return render_template(
                'docinfo.html',
                size="{:,}".format(count),
                filename=inputFileName,
                paragraphs="{:,}".format(len(doc.paragraphs)),
                sections=len(doc.sections),
                tables=len(doc.tables),
                fontDict=fontsFound,
                unicodeFont=formData['UnicodeFont']
            )
                               

        scriptIndex = int(formData['scriptIndex'])
        # Call conversions on the document.
        adlamConverter = adlamConversion.AdlamConverter()      
        try:
            adlamConverter.setScriptIndex(scriptIndex)
            adlamConverter.setLowerMode(True)
            adlamConverter.setSentenceMode(True)
            paragraphs = doc.paragraphs
            count = len(paragraphs)
            msgToSend = '%d paragraphs in %s\n' % (count, fileName)
            countSent = 0

        except BaseException as err:
            return 'Bad Adlam converter. Err = %s' % err
        
        if app.debug:
            print('Created converter')

        try:
            docConverter = ConvertDocx(adlamConverter, documentIn=doc,
                                       reportProgressFn=progressFn)

            if docConverter:
                result = docConverter.processDocx()

                target_stream = BytesIO()
                result = doc.save(target_stream)          

                # Download resulting converted document
                # Reset the pointer to the beginning.
                target_stream.seek(0)

                # Deal with non-ASCII in the file name
                outFileName = fixNonAsciiFilename(outFileName)
                if not outFileName.isascii():
                    outFileName = outFileName.encode('utf8').decode('unicode_escape')
                if app.debug:
                    print(outFileName)
                headerFileName = "attachment;filename=%s" % outFileName

                headers = {
                    "Content-Disposition": headerFileName
                }
                try:
                    msgToSend += 'Starting download\n'
                    countSent = 1
                    return Response(
                        stream_with_context(read_file_chunks(target_stream)),
                        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        headers=headers
                    )
                except BaseException as err:
                    return '**** Response download failure. Err = %s' % err
                
        except BaseException as err:
            return 'Conversion failed. with err %s' % err
        
        # TODO: Try to show conversion results...

def fixNonAsciiFilename(filename):
    charList = []
    for i in [ord(x) for x in filename]:
        if i < 128:
            charList.append(chr(i))
        else:
            charList.append('\\u%04x' % i)
    return ''.join(charList)

# get uploaded file into document form
def createDocFromFile(file):
    try:
        text = file.stream.read()
        data = BytesIO(text)
        count = len(text)
        if app.debug:
            print('FILE LENGTH = %s' % count)
            print('doc file = %s' % data)
        doc = Document(data)
        data.close()
        return doc, count
    except BaseException as err:
        print('Cannot create Docx for %s. Err = %s' % (file, err))
        return None, -1

@app.route('/convertAdlam', methods = ['GET', 'POST'])
def convertAdlam():
    if request.method == 'POST':
        formData = request.form.to_dict()
        if app.debug:
            print('FORMDATA = %s' % formData)

        file = request.files['file']  # FileStorage object
        fileName = file.filename
        outFileName = os.path.splitext(fileName)[0] + '_Unicode.docx'
        if app.debug:
            print('FILE = %s' % file)
            print(outFileName)
        inputFileName = file.filename

        doc, count = createDocFromFile(file)

        try:
            adlamConverter = adlamConversion.AdlamConverter()      
            #
            adlamConverter.setScriptIndex(0)
            adlamConverter.setLowerMode(True)
            adlamConverter.setSentenceMode(True)
            paragraphs = doc.paragraphs
            count = len(paragraphs)
            msgToSend = '%d paragraphs in %s\n' % (count, fileName)
            countSent = 0

        except BaseException as err:
            return 'Bad Adlam converter. Err = %s' % err
        
        if app.debug:
            print('Created converter')

        try:
            docConverter = ConvertDocx(adlamConverter, documentIn=doc,
                                       reportProgressFn=progressFn)

            if docConverter:
                result = docConverter.processDocx()

                target_stream = BytesIO()
                result = doc.save(target_stream)          

                # Download resulting converted document
                # Reset the pointer to the beginning.
                target_stream.seek(0)

                # Deal with non-ASCII in the file name
                outFileName = outFileName.encode(
                    'ascii', errors='backslashreplace')
                if app.debug:
                    print('FILE OUTPUT: %s' % outFileName)
                        
                headerFileName = "attachment;filename=%s" % outFileName

                headers = {
                    "Content-Disposition": headerFileName
                }
                try:
                    msgToSend += 'Starting download\n'
                    countSent = 1
                    return Response(
                        stream_with_context(read_file_chunks(target_stream)),
                        mimetype="application/vnd.openxmlformats-officnedocument.wordprocessingml.document",
                        headers=headers
                    )
                except BaseException as err:
                    print('**** Response download failure. Err = %s' % err)
                
        except BaseException as err:
            return 'Conversion failed. with err %s' % err
        
#    return '%s file uploaded successfully with %d paragraphs' % (file.filename, count)

# https://stackoverflow.com/questions/12232304/how-to-implement-server-push-in-flask-framework
def event_stream():
    global msgToSend
    global countSent
    print('STREAM count = %d, msg=%s' % (countSent, msgToSend))
    if countSent < 1:
        print('STREAM msg:%s' % msgToSend)
        yield "data: {}\n\n".format(msgToSend);
        msgToSend = msgToSend + '.'
        countSent += 1
        
# One way to push data to client. Not working right.
# @app.route('/stream')
# def stream():
#     return Response(event_stream(), mimetype="text/event-stream")

           
if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)
# [END gae_python37_app]
