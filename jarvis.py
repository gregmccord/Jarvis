import speech_recognition as sr
import wolframalpha
import wikipedia
import subprocess
import string
import re
import socket

# Global variables
app_id = 'GTH7KE-J86XHKY6UU' # App_ID for WolframAlpha connection

def eval(r, search):
    client = wolframalpha.Client(app_id)
    res = client.query(search)
    for pod in (temp for temp in res.pods if temp.id == 'Result'):
        for sub in pod.subpods:
            output = search + ' = ' + sub.plaintext
            speak(output)
    
    ask_another(r)

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

    ask_another(r)

def deriv(r, search):
    client = wolframalpha.Client(app_id)
    res = client.query(search)
    for pod in (temp for temp in res.pods if temp.id == 'Derivative'):
        for sub in pod.subpods:
            output = search + ' = ' + sub.plaintext
            speak(sub.plaintext)
    
    ask_another(r)

def define(r, query):
    if re.contains('define', query):
        term = re.match('define (.+)',input).group(1)
    else:
        term = re.match('what does (.+) mean',input).group(1)

    definition = '#error'

    speak(term + ' means ' + definition)

    ask_another(r)

def wiki(r, query, search):
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

    ask_another(r)

def repeat(r, search):
    speak(search)
    ask_another(r)

def internet_on():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False

def ask_another(r):
    speak('Will there be anything else, sir?')
    with sr.Microphone() as source:
        audio = r.listen(source)
    input = r.recognize_google(audio)
    print(input)

    while input != 'yes' and input != 'no':
        speak('Please say yes or no.')
        with sr.Microphone() as source:
            audio = r.listen(source)
        input = r.recognize_google(audio)
        print(input)

    if input == 'yes':
        speak('Alright')
        jarvis(r)
    else: # input == 'no'
        speak('Goodbye, sir.')
        return

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
        re_eval = '(evaluate|find) (.+)'
        re_integ = '(integrate|what is the integral of) (.+)'
        re_deriv = '(derivative of) (.+)'
        re_def = 'define (.+)|what does (.+) mean'
        re_wiki = '(what is|who is|where is) (.+)'
        re_repeat = '(repeat after me) (.+)'

        if re.match(re_eval,input):
            eval(r, re.match(re_eval,input).group(2))
        elif re.match(re_integ,input):
            integ(r, re.match(re_integ,input).group(2))
        elif re.match(re_deriv,input):
            deriv(r, re.match(re_deriv,input).group(2))
        elif re.match(re_def,input):
            define(r, input)
        elif re.match(re_wiki,input):
            wiki(r, input, re.match(re_wiki,input).group(2))
        elif re.match(re_repeat,input):
            repeat(r, re.match(re_repeat,input).group(2))
        else: # No matches
            speak('No input matches. Please enter valid input.')
            jarvis(r)
    else:
        speak('Goodbye, sir.')

def speak(speech):
    print(speech)
    subprocess.Popen(['say', '-r', '200', speech]).wait()

def main():
    speak('Jarvis is listening.')
    r = sr.Recognizer()
    jarvis(r)

if __name__ == '__main__':
    main()