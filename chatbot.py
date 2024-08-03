import openai  #used for easier access of gpt3 api
import pyttsx3   #text to speech converter
import speech_recognition as sr
from api_secrets import API_KEY


openai.api_key = API_KEY

engine = pyttsx3.init()    #initializing the text to speech converter

r = sr.Recognizer()     #creating a variable/reference for speech recognizer function
mic = sr.Microphone(device_index=1)   #selecting mic(input device)


conversation = ""
user_name = "Khush"
bot_name = "Ai"
sleep = False

while True:
    with mic as source:
        print("\nlistening...")
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print("no longer listening.\n")

    try:
        user_input = r.recognize_google(audio)
    except:
        continue

    prompt = user_name + ": " + user_input + "\n" + bot_name+ ": "

    conversation += prompt  # allows for context
    if "wake up" in user_input and sleep==True:
        sleep = False
        print("How may I help you?")
        engine.say("How may I help you?")
        engine.runAndWait()
        continue
    elif sleep==True:
        continue
    elif "goodbye" in user_input:
        print("Goodbye")
        engine.say("goodbye")
        engine.runAndWait()
        break
    elif "enter sleep mode" in user_input and sleep==False:
        sleep = True
        print("entering sleep mode...")
        engine.say("entering sleep mode")
        engine.runAndWait()
        continue
    else:
        pass



    # fetch response from open AI api
    response = openai.Completion.create(engine='text-davinci-003', prompt=conversation, max_tokens=100)
    response_str = response["choices"][0]["text"].replace("\n", "")
    response_str = response_str.split(user_name + ": ", 1)[0].split(bot_name + ": ", 1)[0]

    conversation += response_str + "\n"
    print(response_str)   #printing response

    engine.say(response_str)   #using pyttsx3 module to convert text to speech
    engine.runAndWait()