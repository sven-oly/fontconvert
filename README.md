# fontconvert: modernizing old-style font encodings to Unicode

This directory contains python routines for converting Word .docx files and other formats
from custom, non-Unicode fonts to documents with such text converted to Unicode values.

## What is a font encoding?
Historically, many font encodings (also called "font hacks") have been used to represent characters in a specific script. By substituting the images of a font with the shapes of another writing system that is not well supported. Often, the code positions that have been substituted are for ASCII or Latin or Arabic code points. This was often done to support text for a script that was not standardized in Unicode or where fonts were not yet available.

Note that font encoding is effective for documents that are read by humans. However, text that is shown by a font encoding will apprear to be in the original code points of the font used. There is no way for a program or web site to know that such characters have been used to represent another set of characters, so extracting the actual characters into the language and script visually represented is not possible.

## What is value of Unicode?
Unicode defines code values for many scripts. When text is written with Unicode values and displayed with a Unicode-compatible font, the characters can be read by people and also by programs. Because each script has distinct character codes, the identity of each character is deteremined by the code, not just by a font.

Typing in multiple scripts requires keyboard input and Unicode fonts. These are available from major vendors of software and applications. In addition, applications such as Keyman offer hundreds of keyboards for many languages and scripts. These can be installed on most computers and mobile devices.

An additional benefit of Unicode representation is that the style of the text can be changed by simply picking a different Unicode-compatible font for the writing system. The identity of the characters in the text is not changed by applying a different font.

## Required input format for fontconvert
This **fontconvert** implementation uses the python programming language and a module called *python-docx*. This reads and process.docx files MS Word 2006 format. Newer versions of MS Word documents are not processed by python-docx.

It may be necessary to use "save as" in MS Word or other application such as LibreOffice in order to have the required file version.

**fontconvert** conversion may also be done from .xslx files saved from Excel.

## Supported language codes and font encodings

The programs and functions open existing files and then scan each part of the document for specific encoded fonts. These represent characters in a script by substituting the images of a font for another writing system such as Latin or Arabic. This was often done for writing text in a script that was not standardized in Unicode.

Several converter files are already built for use with the following sets of languages

* Fulfulde language in Adlam script using non-Unicode fonts Aissata, Fuuta, and Pulaar
** Output is in Noto Sans Adlam font by default.
** Latin Fulfulde text may also be converted to Adlam script in Unicode for .docx and .xlsx files.

* Tai Phake (phk) and others. A group of font encodings are converted that include Tai Phake, Aiton, Assames, Tai Ahom, Shan, ST_Metta, and Indic New diacritics.

* Tai Ahom, from AHOMFONT and Amon Manuscript font

## Online use of the tools

https://fontconvert.appspot.com presents the following main page:
<img width="615" height="348" alt="image" src="https://github.com/user-attachments/assets/893004c7-1fc1-4516-b5b2-8aed9c47fff2"/>

# How to convert a document
After selecting the language group, the conversion page is shown. Options include:
* Select a file
* Show some details of the selected file such as number of paragraphs with each font
* Convert the file to Unicode. This uploads the document to the server, runs the conversion, and downloads the resulting document with Unicode characters and fonts.

## Additional options:
The possible options depend on the language group being converted.

In the case of the Tai Phake group, there are possible replacements offered for each of the encoding fonts in this image:
<img width="877" height="423" alt="image" src="https://github.com/user-attachments/assets/1714c619-bd20-4df4-9a40-6cf9669120f3" />

## Command line operation

The online converter described above operates on a single file. In some cases, the user may have a number of files that should be converted.

In this case, the conversions can be executed with a command line in a terminal window such as "Windows PowerShell".

The conversion is done entirely on the user's computer, using no online resources. This may be significantly faster than requesting individual conversion. However, some options such as output fonts are not selectable.

### Requirements:
1. python3 in a recent version, e.g., 3.12
1. python-docx module (installation via pip, shown below.)

### Install the fontconvert code
1. Download the directory from:
https://github.com/sven-oly/fontconvert as a .zip file. This is done using the green "code" button at the upper right of the main screen
<img width="469" height="390" alt="image" src="https://github.com/user-attachments/assets/6f37549a-830f-4839-ad21-40d7b97d26ad" />

1. Select "Download ZIP" to copy the project to your computer's download directory.

1. Next, open a terminal window and navigate to a directory on your computer that has sufficient space.

1. Move the .zip file to this directory, then *unzip* the downloaded file in this directory.

1. Enter the folder containing the fontconvert program.

1. Install needed python modules with these commands
```
pip uninstall docx
pip3 install python-docx
```
# Running the converter
To execute the program from the installed directory, use the following commands in the terminal window
```
python3 command_line.py php <path>
# <path> may include one or more names of individual files
# <path> may also include directory names. Each .docx file will be converted.
```
By default, each converted file will be added to the directory.

Note that files with "Unicode" in their name will be skipped.

Important: verify that output files have been correctly converted with Unicode fonts applied to each section that was labeled with one of the supported encoding fonts.
