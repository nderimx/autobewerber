#!/usr/bin/python3
from bs4 import BeautifulSoup
import pdfkit
from datetime import date
import os

def application_filler(html_file, output_file, unternehmen, strasse, platz, stellenbeschreibung, ansprache, html=False):

    datum               = date.today().strftime("%d.%m.%Y")

    with open(html_file, 'r') as html:
        soup = BeautifulSoup(html, 'html.parser')

    soup.find(id='Unternehmen').string = unternehmen
    soup.find(id='Strasse').string = strasse
    soup.find(id='Platz').string = platz
    soup.find(id='Datum').string = datum
    soup.find(id='Stellenbeschreibung').string = stellenbeschreibung
    soup.find(id='Ansprache').string = ansprache

    if html == True:
        with open('output.html', 'w') as output:
            output.write(soup.prettify())
    else:
        options = {
            'enable-local-file-access' : '',
            'page-size'                 : 'Letter'
        }
        # pdfkit.from_string(str(soup), html_file.split('.')[0]+'.pdf', options=options)

        # Deprecate this after resolving the XDG_RUNTIME_DIR not set, defaulting to '/tmp/runtime-prie' bug when using from_string,
        # because this is too slow
        html_output = os.path.dirname(html_file)+"/output.html"
        with open(html_output, 'w') as output:
            output.write(soup.prettify())
        pdfkit.from_file(html_output, output_file, options=options)
        os.remove(html_output)