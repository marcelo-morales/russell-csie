import speech_recognition as sr
import time
#from gensim.parsing.preprocessing import remove_stopwords
#look into finding a way to remove stop words without anaconda, installation issues

#using speech_recognition library
#tutorial: https://realpython.com/python-speech-recognition/

#input as a string
#microphone low
def recognize_speech(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("these are the stopwords i will use \n")
   # print(stopwords.words('english'))
    #words_to_filter = set(stopwords.words('english'))
    
    

    #format 
    instruction = "ask me question based on a specific attribute for my character"
    print(instruction)
    #time.sleep(2)

    PROMPT_LIMIT = 1 #number of times a user is allowed to speak to microphone

    for i in range(PROMPT_LIMIT):
        response_from_user = recognize_speech(recognizer, microphone)
        
        if not response_from_user["success"]:
            break
        print("I didn't catch that. What did you say?\n")

    print("You said: {}".format(response_from_user["transcription"]))

    # word_tokens = word_tokenize(response_from_user["transcription"])

    # filtered_sentence = [w for w in word_tokens if not w.lower() in words_to_filter]
 
    # filtered_sentence = []

    # for w in word_tokens:
    #     if w not in words_to_filter:
    #         filtered_sentence.append(w)

    #print("after filtering out words we dont need, you said " + str(filtered_sentence))

    print("these are all the microphone inputs I can find " + str(sr.Microphone.list_microphone_names()))