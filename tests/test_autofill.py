from autofiller import application_filler
import sys

if len(sys.argv) < 2:
    # print("pass in the file name as the argument")
    # sys.exit()
    html_file = "Bewerbung_Security.html"
else:
    html_file = sys.argv[1]

# Sanitize for Word Size, so an address for instance, doesn't overflow on a second line

unternehmen         = "Security Group"
strasse             = "Rosastrasses 19"
platz               = "8000 Zurich"
stellenbeschreibung = "Security Engineer"
ansprache           = "Sehr geehrte Damen und Herren"

application_filler(html_file, unternehmen, strasse, platz, stellenbeschreibung, ansprache, False)