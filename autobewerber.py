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
import pandas

config_location = "config/config.json"

def load_config(config_file):
    with open(config_file) as config:
        return json.loads(config.read())

def save_job(log_file, unternehmen, strasse, platz, stellenbeschreibung, ansprache, link, receiver, zustand = "gesendet"):
    # df = pandas.DataFrame({ 'link': [link],
    #                         'unternehmen': [unternehmen],
    #                         'strasse': [strasse],
    #                         'platz': [platz],
    #                         'stellenbeschreibung': [stellenbeschreibung],
    #                         'ansprache': [ansprache]})
    # df.to_csv("application.csv", index = False, index_label = False, mode = "a")
    datum               = date.today().strftime("%d.%m.%Y")
    with open(log_file, 'a') as csv_file:
        csv_file.write(link+','+unternehmen+','+strasse+','+platz+',\"'+stellenbeschreibung+'\",'+ansprache+','+receiver+','+datum+','+zustand+'\n')
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

    if receiver == "":
        print(message)
        print("Press enter when application is sent.", end="")
        input()
        save_job(config["log_file"], unternehmen, strasse, platz, stellenbeschreibung, ansprache, link, receiver, "web_form")
    else:
        sender      = config["sender_email"]
        subject     = "Bewerbung als " + stellenbeschreibung
        attachments = [application_letter, cv, certificates]

        send_application(sender, receiver, subject, message, attachments, password)
        save_job(config["log_file"], unternehmen, strasse, platz, stellenbeschreibung, ansprache, link, receiver)

def display_details(unternehmen, strasse, platz, stellenbeschreibung, ansprache):
    print("-- unternehmen (u):\t\t\t"+unternehmen)
    print("-- strasse (str):\t\t\t"+strasse)
    print("-- platz (p):\t\t\t\t"+platz)
    print("-- stellenbeschreibung (stb):\t\t"+stellenbeschreibung)
    print("-- ansprache (a):\t\t\t"+ansprache)

def bewerber_shell():
    password    = getpass()
    config      = load_config(config_location)
    search_term = config["search_term"]
    links = scraper.scrape_links(search_term)
    print("%d results" % len(links))
    for link in links:
        link = config["host"]+link
        # check if this link has already been used or skipped
        df = pandas.read_csv(config["log_file"], sep=',', encoding='latin1', dayfirst=True, index_col='link')
        try:
            df.loc[link]
            continue
        except:
            print("")

        # this is for wsl for now (it's adhoc because the template looks terrible with the windows version of wkhtmltopdf) TODO: template needs to be standardized
        os.system("/mnt/c/Program\\ Files/Google/Chrome/Application/chrome.exe"+" "+link)

        unternehmen, strasse, platz, stellenbeschreibung, ansprache = scraper.scrape_ad(link)

        repeated = 0
        while unternehmen == "0" and repeated < 10:
            print("Repeating due to error")
            unternehmen, strasse, platz, stellenbeschreibung, ansprache = scraper.scrape_ad(link)
            repeated += 1
            
        if repeated >= 10:
            continue

        print("Are the details ok?")
        display_details(unternehmen, strasse, platz, stellenbeschreibung, ansprache)
        print("->", end =" ")
        answer = input()

        while not (answer == "y" or answer == "yes" or answer == "ok" or answer == "kk" or answer == "web" or answer == "skip"):
            print("edit info>>", end = " ")
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
        if answer == "skip":
            receiver = "none"
            save_job(config["log_file"], unternehmen, strasse, platz, stellenbeschreibung, ansprache, link, receiver, "uebersprungen")
        elif answer == "web":
            bewerben("1", link, "", unternehmen, strasse, platz, stellenbeschreibung, ansprache)
        else:
            print("receiver's email: ", end ="")
            receiver = input()
            print("Make sure the receiver's email is correct: %s" % receiver)
            answer = input()
            while not (answer == "y" or answer == "yes" or answer == "ok" or answer == "kk"):
                print("correct receiver's email: ", end ="")
                receiver = input()
                print("Make sure the receiver's email is correct: %s" % receiver)
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
