# autobewerber
Automatisierung vom Bewerbungsprozess

_Nur Inserat Link und Empfaenger Email sind noetig um dich zu bewerben, das Vorbereiten von deinen Dokumenten und andere Kleinigkeiten werden von Autobewerber erledigt._

##### Momentan nur mit jobs.ch

#### config/config.json Struktur:
`{`
`    "log_file"              : "logs/applications.csv",`
`    "sender_name"           : "John Doe",`
`    "sender_email"          : "johndoe1888@gmail.com",`
`    "docs_directory"        : "documents",`
`    "cv"                    : "Lebenslauf.pdf",`
`    "certificates"          : "Zeugnisse_und_Diplome.pdf",`
`    "email_message"         : "message_without_greeting.txt",`
`    "application_letter"    : "Bewerbungsschreiben.pdf",`
`    "app_letter_template"   : "documents/application_letter_template/Bewerbungsschreiben.html"`
`}`

#### Bewerbungsschreiben.html id's die von autofiller.py identifiziert und benutzt werden:
* 'Unternehmen'
* 'Strasse'
* 'Platz'
* 'Datum'
* 'Stellenbeschreibung'
* 'Ansprache'