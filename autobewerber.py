#!/usr/bin/python3
import sys
import os
sys.path.append(os.getcwd()+"/src")
import scraper
from autofiller import application_filler
from email_sender import send_application
import json
from datetime import date
from getpass import getpass

config_location = "config/config.json"

def load_config(config_file):
    with open(config_file) as config:
        return json.loads(config.read())

def save_job(log_file, unternehmen, strasse, platz, stellenbeschreibung, ansprache, link, receiver):
    # df = pandas.DataFrame({ 'link': [link],
    #                         'unternehmen': [unternehmen],
    #                         'strasse': [strasse],
    #                         'platz': [platz],
    #                         'stellenbeschreibung': [stellenbeschreibung],
    #                         'ansprache': [ansprache]})
    # df.to_csv("application.csv", index = False, index_label = False, mode = "a")
    datum               = date.today().strftime("%d.%m.%Y")
    with open(log_file, 'a') as csv_file:
        csv_file.write(link+','+unternehmen+','+strasse+','+platz+',\''+stellenbeschreibung+'\','+ansprache+','+receiver+','+datum+',gesendet\n')
    print(unternehmen, strasse, platz, stellenbeschreibung, ansprache, link)

def bewerben(password, link, receiver, unternehmen, strasse, platz, stellenbeschreibung, ansprache):
    config              = load_config(config_location)
    docs_dir            = config["docs_directory"]

    html_file           = config["app_letter_template"]
    message_file        = docs_dir + "/" + config["email_message"]
    application_letter  = docs_dir + "/" + config["application_letter"]
    cv                  = docs_dir + "/" + config["cv"]
    certificates        = docs_dir + "/" + config["certificates"]

    application_filler(html_file, application_letter, unternehmen, strasse, platz, stellenbeschreibung, ansprache, False)


    with open(message_file) as f:
        message = ansprache + f.read().replace("*Stellenbeschreibung*", stellenbeschreibung) + config["sender_name"]

    sender      = config["sender_email"]
    subject     = "Bewerbung als " + stellenbeschreibung
    attachments = [application_letter, cv, certificates]

    send_application(sender, receiver, subject, message, attachments, password)
    save_job(config["log_file"], unternehmen, strasse, platz, stellenbeschreibung, ansprache, link, receiver)

def display_details(unternehmen, strasse, platz, stellenbeschreibung, ansprache):
    print("-- unternehmen:\t\t\t"+unternehmen)
    print("-- strasse:\t\t\t"+strasse)
    print("-- platz:\t\t\t"+platz)
    print("-- stellenbeschreibung:\t\t"+stellenbeschreibung)
    print("-- ansprache:\t\t\t"+ansprache)

def bewerber_shell():
    password = getpass()
    while True:
        print("link: ", end ="")
        link = input()
        print("receiver's email: ", end ="")
        receiver = input()

        unternehmen, strasse, platz, stellenbeschreibung, ansprache = scraper.scrape_ad(link)

        print("Are the details ok?")
        display_details(unternehmen, strasse, platz, stellenbeschreibung, ansprache)
        print("->", end =" ")
        answer = input()
        while not (answer == "y" or answer == "yes" or answer == "ok" or answer == "kk"):
            if answer == "u":
                unternehmen = input()
            elif answer == "str":
                strasse = input()
            elif answer == "p":
                platz = input()
            elif answer == "stb":
                stellenbeschreibung = input()
            elif answer == "a":
                ansprache = input()
            print("What about now?")
            display_details(unternehmen, strasse, platz, stellenbeschreibung, ansprache)
            print("->", end =" ")
            answer = input()
        bewerben(password, link, receiver, unternehmen, strasse, platz, stellenbeschreibung, ansprache)


def main():
    if len(sys.argv) < 3:
        bewerber_shell()
    else:
        link        = sys.argv[1]
        receiver    = sys.argv[2]
    
        unternehmen, strasse, platz, stellenbeschreibung, ansprache = scraper.scrape_ad(link)
        bewerben("", link, receiver, unternehmen, strasse, platz, stellenbeschreibung, ansprache)



if __name__ == "__main__":
    main()
