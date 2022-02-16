import speech_recognition as sr
import time

#using speech_recognition library
#tutorial: https://realpython.com/python-speech-recognition/

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
    

    instruction = "ask me question based on a specific attribute for my character"
    print(instruction)
    time.sleep(3)

    PROMPT_LIMIT = 3 #number of times a user is allowed to speak to microphone

    for i in range(PROMPT_LIMIT):
        guess = recognize_speech(recognizer, microphone)
        if guess["transcription"]:
            break
        if not guess["success"]:
            break
        print("I didn't catch that. What did you say?\n")

    print("You said: {}".format(guess["transcription"]))
    
    print("these are all the microphone inputs I can find " + sr.Microphone.list_microphone_names())

    print("hello world\n")