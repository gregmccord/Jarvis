import speech_recognition as sr
import DictionaryServices as ds
import wolframalpha
import wikipedia
import subprocess
import string
import socket
import time
import sys
import re

# Global variables
app_id = 'GTH7KE-J86XHKY6UU' # App_ID for WolframAlpha connection
r = sr.Recognizer() # Speech recognition object

# Evaluate a mathetmatical expression
def eval(search):
    client = wolframalpha.Client(app_id)
    res = client.query(search)
    for pod in (temp for temp in res.pods if temp.id == 'Result'):
        for sub in pod.subpods:
            output = search + ' = ' + sub.plaintext
            speak(output)
    
    ask_another()

# Integrate some expression using WolframAlpha
def integ(search):
    client = wolframalpha.Client(app_id)
    res = client.query(search)
    isDef = search.contains('from') # Definite integral

    # Definite vs. Indefinite Integral
    if isDef:
        for pod in (temp for temp in res.pods if temp.id == 'Definite integral'):
            for sub in pod.subpods:
                speak(sub.plaintext)
    else:
        for pod in (temp for temp in res.pods if temp.id == 'Indefinite integral'):
            for sub in pod.subpods:
                speak(sub.plaintext)

    ask_another()

# Find the Derivative of some expression using WolframAlpha
def deriv(search):
    client = wolframalpha.Client(app_id)
    res = client.query(search)
    for pod in (temp for temp in res.pods if temp.id == 'Derivative'):
        for sub in pod.subpods:
            output = search + ' = ' + sub.plaintext
            speak(sub.plaintext)
    
    ask_another()

# Find the definition of some English word
def define(query):
    if re.search('define', query):
        term = re.match('define (.+)',query).group(1)
    else:
        term = re.match('what does (.+) mean',query).group(1)

    wordRange = (0, len(term))
    result = ds.DCSCopyTextDefinition(None, term, wordRange).encode('utf-8')
    partOfSpeech = result.split('\xe2\x96\xb6') # Split on utf-8 right arrow
    definition = []
    for meaning in partOfSpeech:
        definition.append(meaning.split('\xe2\x80\xa2')) # Split on utf-8 dot

    done = False
    i = 1
    while not done:
        iterate(definition[i], query, 0)

        i += 1
        if i == len(definition):
            time.sleep(0.75) # Natural pause
            speak('There are no more parts of speech.')
            done = True
        else:
            speak('Would you like another part of speech?')
            text = yes_or_no()

            if text == 'no':
                done = True

    ask_another()

def iterate(arrays, query, i):
    output = re.sub(':([^:]+$)',r'; For Example: \1' , arrays[i])
    speak(output)
    if i == len(arrays) - 1:
            time.sleep(0.75) # Natural pause
            speak('There are no more definitions for this part of speech.')
            return
    else:
        time.sleep(0.75) # Natural pause
        speak('Would you like another definition?')
        text = yes_or_no()

        if text == 'yes':
            iterate(arrays, query, i + 1)
        else: # text == 'no'
            return 

# Search for some person/place/thing on Wikipedia
def wiki(query, search):
    summary = wikipedia.summary(search)
    speak(summary)
    speak('Should I open the website?')
    audio = r.listen(source)
    text = r.recognize_google(audio)
    text = text.lower()
    if text == 'yes':
        page = wikipedia.WikipediaPage(search).title
        page = page.replace(' ','_')
        website = 'http://wikipedia.org/wiki/' + page
        args = ['open',website]
        subprocess.Popen(args)

    ask_another()

# Repeat what the user says
def repeat(search):
    speak(search)
    ask_another()

# Because Mom is the best
def mom():
    speak("Your mom is the most beautiful woman in the world")

# Determine if the device is connected to the internet or not
def internet_on():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False

# Will the user ask another question
def ask_another():
    speak('Will there be anything else, sir?')
    text = yes_or_no()

    # Give another query (yes) or end the program (no)
    if text == 'yes':
        speak('Alright')
        jarvis()
    else: # text == 'no'
        speak('Goodbye, sir.')
        return

# If the user is asked a yes/no question, ensure the answer is yes/no
def yes_or_no():
    with sr.Microphone() as source:
            audio = r.listen(source)
    text = r.recognize_google(audio)
    text = text.lower()
    
    # Repeat until valid input is received
    while text != 'yes' and text != 'no':
        speak('Please say yes or no.')
        with sr.Microphone() as source:
            audio = r.listen(source)
        text = r.recognize_google(audio)
    print(text)
    return text

# The 'brain' of Jarvis - controls the actions
def jarvis():

    # Take in speech and recognize the English words
    with sr.Microphone() as source:
        audio = r.listen(source)

    if internet_on():
        text = r.recognize_google(audio)
    else:
        speak('Unable to connect.')
        return

    # Treat the input
    print(text)
    text = text.lower()

    if re.match('^(jarvis |)exit|stop|quit$',text):
        speak('Goodbye, sir.')
    else:
        # Regular Expressions for parsing input
        re_eval = '(evaluate|find) (.+)'
        re_integ = '(integrate|what is the integral of) (.+)'
        re_deriv = '(derivative of) (.+)'
        re_def = 'define (.+)|what does (.+) mean'
        re_wiki = '(what is|who is|where is) (.+)'
        re_repeat = '(repeat after me) (.+)'
        re_mom = 'jarvis who is the most beautiful woman in the world'

        # Determine which method to call
        if re.match(re_eval,text):
            eval(re.match(re_eval,text).group(2))
        elif re.match(re_integ,text):
            integ(re.match(re_integ,text).group(2))
        elif re.match(re_deriv,text):
            deriv(re.match(re_deriv,text).group(2))
        elif re.match(re_def,text):
            define(text)
        elif re.match(re_wiki,text):
            wiki(text, re.match(re_wiki,text).group(2))
        elif re.match(re_repeat,text):
            repeat(re.match(re_repeat,text).group(2))
        elif re.match(re_mom,text):
            mom()
        else: # No matches
            speak('No input matches. Please enter valid input.')
            jarvis()

# Print speech and use Unix say command to speak
def speak(speech):
    print(speech)
    subprocess.Popen(['say', '-r', '210', speech]).wait()

# main method - starts Jarvis's 'brain'
def main():
    speak('Jarvis is listening.')
    jarvis()

if __name__ == '__main__':
    main()