import speech_recognition as sr
import wikipedia
import sys
import codecs
import subprocess
import string
import re
import wolframalpha
import ssl
import certifi
import socket

# Global variables
app_id = 'GTH7KE-J86XHKY6UU' # App_ID for WolframAlpha connection

def wiki(r, search):
    summary = wikipedia.summary(search)
    speak(summary)
    speak('Should I open the website?')
    audio = r.listen(source)
    input = r.recognize_google(audio)
    input = input.lower()
    if input == 'yes':
        page = wikipedia.WikipediaPage(search).title
        page = page.replace(' ','_')
        website = 'http://wikipedia.org/wiki/' + page
        args = ['open',website]
        subprocess.Popen(args)

    jarvis(r)

def define(r, search):
    speak('define: ' + search)

    jarvis(r)

def eval(r, search):
    client = wolframalpha.Client(app_id)
    res = client.query(search)
    for pod in (temp for temp in res.pods if temp.id == 'Result'):
        for sub in pod.subpods:
            output = search + ' = ' + sub.plaintext
            speak(output)
    
    jarvis(r)

def integ(r, search):
    client = wolframalpha.Client(app_id)
    res = client.query(search)
    isDef = search.contains('from') # Definite integral

    if isDef:
        for pod in (temp for temp in res.pods if temp.id == 'Definite integral'):
            for sub in pod.subpods:
                print(sub.plaintext)
    else:
        for pod in (temp for temp in res.pods if temp.id == 'Indefinite integral'):
            for sub in pod.subpods:
                print(sub.plaintext)

    jarvis(r)

def deriv(r, search):
    client = wolframalpha.Client(app_id)
    res = client.query(search)
    for pod in (temp for temp in res.pods if temp.id == 'Derivative'):
        for sub in pod.subpods:
            output = search + ' = ' + sub.plaintext
            speak(sub.plaintext)
    
    jarvis(r)

def repeat(r, search):
    speak(search)
    jarvis(r)

def internet_on():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False

def jarvis(r):
    with sr.Microphone() as source:
        audio = r.listen(source)

    if internet_on():
        input = r.recognize_google(audio)
    else:
        speak('Unable to connect.')
        return
    print(input)
    input = input.lower()

    if input != 'exit' and input != 'stop':
        re_eval = 'evaluate (.+)|find (.+)'
        re_integ = 'integrate (.+)|what is the integral of (.+)'
        re_deriv = 'derivative of (.+)'
        re_def = 'define (.+)|what does (.+) mean'
        re_wiki = 'what is (.+)|who is (.+)|where is (.+)'
        re_repeat = 'repeat after me (.+)'

        if re.match(re_eval,input,re.I):
            eval(r, re.match(re_eval,input,re.I).group())
        elif re.match(re_integ,input,re.I):
            integ(r, re.match(re_integ,input,re.I).group())
        elif re.match(re_deriv,input,re.I):
            deriv(r, re.match(re_deriv,input,re.I).group())
        elif re.search(re_def,input,re.I):
            define(r, re.search(re_def,input,re.I).group())
        elif re.match(re_wiki,input,re.I):
            wiki(r, re.match(re_wiki,input,re.I).group())
        elif re.match(re_repeat,input,re.I):
            repeat(r, re.match(re_repeat,input,re.I).group(1))
        else: # No matches
            speak('No input matches. Please enter valid input.')
            jarvis(r)
    else:
        speak('Jarvis shutting down.')

def speak(speech):
    print(speech)
    subprocess.Popen(['say', '-r', '200', speech]).wait()

def main():
    speak('Jarvis is listening.')
    r = sr.Recognizer()
    jarvis(r)

if __name__ == '__main__':
    main()