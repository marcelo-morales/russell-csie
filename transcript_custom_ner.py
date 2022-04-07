# Load pre-existing spacy model
import spacy
nlp=spacy.load('en_core_web_sm')
# Import requirements
import random
from spacy.util import minibatch, compounding
from pathlib import Path
import speech_recognition as sr
import time 
from spacy import displacy
from spacy.training.example import Example
import os


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

def refactor_for_backend(result_array):
    entity = result_array["trait"]
    returned_string = result_array["adjective"]

    #hair color blonde
    if (entity == "hair_color" and (returned_string == "blond" or returned_string == "blonde" 
        or returned_string == "yellow" or returned_string == "gold" or returned_string == "golden")):
        result_array["adjective"] = "blond"

    #hair color red
    if (entity == "hair_color" and (returned_string == "red" or returned_string == "ginger" 
        or returned_string == "auburn")):
        result_array["adjective"] = "red"

    #hair color brown
    if (entity == "hair_color" and (returned_string == "brown" or returned_string == "brunette" 
        )):
        result_array["adjective"] = "brown"

    return result_array
    





def speech_to_text():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    print("\n\n*******************************************************************")
    instruction = "Hi, I'm Russell! Ask me question based on a specific attribute for my character to try to guess who it is!"
    print(instruction)
    #time.sleep(1)

    PROMPT_LIMIT = 1 #number of times a user is allowed to speak to microphone

    for i in range(PROMPT_LIMIT):
        response_from_user = recognize_speech(recognizer, microphone)
        
        if not response_from_user["success"]:
            break
        print("Sorry, I didn't catch that. What did you say?\n")

    print("You said: {}".format(response_from_user["transcription"]))

    return response_from_user["transcription"]

def main():

    #if folder exists
    if os.path.isdir("./content"):
        #load data from content
        print('have content folder')
        print("Loading from", "./content")
        nlp_updated = spacy.load("./content")

        transcription = speech_to_text()
        doc = nlp_updated(transcription) 

        for ent in doc.ents:
            trait = ent.text
            value = ent.label_

        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
        print("\n The value label (adjective)  is " + str(ent.text) + " and the field label (trait) is " +  str(ent.label_) + "\n")



        result_array = {"trait" : str(ent.label_), "adjective" :  str(ent.text)}

        result_array = refactor_for_backend(result_array)



        print("what is returned to game backend is " + result_array["trait"] + " and " + result_array["adjective"])


        return result_array
    else:

        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")
        if 'ner' not in nlp.pipe_names:
            ner = nlp.create_pipe('ner')
            nlp.add_pipe('ner')
            print("created ner")
        else:
            ner = nlp.get_pipe('ner')

        # Getting the pipeline component
        ner=nlp.get_pipe("ner")

        # training data
        # NEW TRAIN_DATA
        TRAIN_DATA = [
              ("what's for dinner", {"entities": []}),
              ("got any dinner", {"entities": []}),
              ("did you eat dinner", {"entities": []}),
              ("wait what's going on again", {"entities": []}),
              ("i'm confused", {"entities": []}),
              ("where did you all learn frightened", {"entities": []}),
              ("hi my name is", {"entities": []}),
              ("what is this game called", {"entities": []}),
              ("is it cold outside", {"entities": []}),
              ("could you raise the thermostat", {"entities": []}),
              ("call my nurse", {"entities": []}),
              ("like that that's fair", {"entities": []}),
              ("that's a butt", {"entities": []}),
              ("it's a person", {"entities": []}),
              ("oh yeah there's a persons", {"entities": []}),
              ("yes does the character have a pleasant expression", {"entities": []}),
              # Note: take this null example out when beard trait is added
              ("does the character have a beard or a goatee", {"entities": []}),
              ("no does a character have", {"entities": []}),
              # Notes: that this null example out when gender is added
              ("Is a character a male", {"entities": []}),
              ("someone told me this would be fun", {"entities": []}),
              
              ("is your person wearing glasses", {"entities": [(23,30,"wearing_glasses")]}),
              ("do they have glasses", {"entities": [(13,20,"wearing_glasses")]}),
              ("does your person have glasses on", {"entities": [(22,29,"wearing_glasses")]}),
              ("does your person not have glasses on?", {"entities": [(17,24,"wearing_glasses")]}),
              ("does your character not have glasses on?", {"entities": [(20,36,"wearing_glasses")]}),
              ("does your character not wear glasses on?", {"entities": [(20,36,"wearing_glasses")]}),
              ("does she not have glasses on?", {"entities": [(9,25,"wearing_glasses")]}),
              ("does he not have glasses on?", {"entities": [(8,24,"wearing_glasses")]}),
              ("do they not wear glasses?", {"entities": [(8,24,"wearing_glasses")]}),
              ("does he not wear glasses?", {"entities": [(8,24,"wearing_glasses")]}),

              ("is she blond", {"entities": [(7,12,"hair_color")]}),
              ("is your person blond haired", {"entities": [(15,20,"hair_color")]}),
              ("is he golden haired", {"entities": [(6,12,"hair_color")]}),
              ("are they gold haired", {"entities": [(9,13,"hair_color")]}),
              ("does your person have yellow hair", {"entities": [(22,28,"hair_color")]}),
              ("are they auburn haired?", {"entities": [(9,15,"hair_color")]}),
              ("is your person a ginger", {"entities": [(17,24,"hair_color")]}),
              ("is their hair brown", {"entities": [(14,19,"hair_color")]}),
              ("is her hair red", {"entities": [(12,15,"hair_color")]}), 
              ("is she red haired", {"entities": [(7,10,"hair_color")]}),
              ("is she brunette", {"entities": [(7,15,"hair_color")]}),
              ("is your character a brunette" , {"entities": [(20,28,"hair_color")]}),
              
              ("is your person wearing a green hat", {"entities": [(25,30,"hat_color")]}),
              ("are they wearing a green hat", {"entities": [(19,24,"hat_color")]}),
              ("does your person have a green hat", {"entities": [(24,29,"hat_color")]}), 
              ("do they have a green hat", {"entities": [(15,20,"hat_color")]}),

              ("does your person wear a hat", {"entities": [(24,27,"wearing_a_hat")]}), 
              ("do they wear a hat", {"entities": [(15,18,"wearing_a_hat")]}), 
              ("do they have a hat", {"entities": [(15,18,"wearing_a_hat")]}),
              ("do they not have a hat?", {"entities": [(8,22,"wearing_a_hat")]}),
              ("do they not wear a hat?", {"entities": [(8,22,"wearing_a_hat")]}),
              ("does your character not have a hat?", {"entities": [(19,33,"wearing_a_hat")]}),  
              ("does she not wear a hat?", {"entities": [(9,23,"wearing_a_hat")]}), 
              ("does your person not have a hat on?", {"entities": [(17,31,"wearing_a_hat")]}), 

              ("does your person not have head hair", {"entities": [(17,35,"bald")]}),
              ("is your person bald", {"entities": [(15,19,"bald")]}),
              ("is she bald", {"entities": [(7,13,"bald")]}),
              ("is he bald", {"entities": [(6,10,"bald")]}),
              ("does he not have head hair", {"entities": [(8,26,"bald")]}),
              ("does she not have hair on her head", {"entities": [(8,21,"bald")]}),
              ("do they have hair on their head", {"entities": [(8,17,"bald")]}),
              ("does she have hair", {"entities": [(9,18,"bald")]}),
              ("is their head bald", {"entities": [(14,18,"bald")]}),

              ("is your person bernard", {"entities": [(15,22,"name")]}), 
              ("is it anita", {"entities": [(6,11,"name")]}),
              ("is she susan", {"entities": [(7,12,"name")]}), 
              ("is he sam", {"entities": [(6,9,"name")]}), 
              ("are they alex", {"entities": [(9,13,"name")]}),
              ("are they paul", {"entities": [(9,13,"name")]}),
              ("my guess is arthur", {"entities": [(12,18,"name")]}),
              ("how about jamie ", {"entities": [(10,15,"name")]}),
              ("is your character charles", {"entities": [(18,25,"name")]}),
              ("shannon", {"entities": [(0,7,"name")]}), 
              ("claire", {"entities": [(0,6,"name")]})                                           
              # ("Walmart is a leading e-commerce company", {"entities": [(0, 7, "ORG")]})
              ]

        # Adding labels to the `ner`

        for _, annotations in TRAIN_DATA:
            for ent in annotations.get("entities"):
                ner.add_label(ent[2])
        # print("adding label")

        # Disable pipeline components you dont need to change
        pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
        unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

        optimizer = nlp.begin_training()

        # TRAINING THE MODEL
        with nlp.disable_pipes(*unaffected_pipes):

         # Training for 30 iterations
            for iteration in range(200): # train for longer, maybe 200 iterations or until loss < 0
                # shuufling examples  before every iteration
                random.shuffle(TRAIN_DATA)
                losses = {}
                # batch up the examples using spaCy's minibatch
                batches = minibatch(TRAIN_DATA, size=64) # size=32 or 64 or even len(TRAIN_DATA) is better
                for batch in batches:
                    texts, annotations = zip(*batch)
                    nlp.update(
                                texts,  # batch of texts
                                annotations,  # batch of annotations
                                drop=0.5,  # dropout - make it harder to memorise data
                                losses=losses,
                            )
                print("Losses", losses)

        # SAVE the  model to directory
        output_dir = Path('./content/')
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)
        
        #TRANSCRIPTION
        transcription = speech_to_text()

        # Testing the model
        doc = nlp(transcription)
        print("\n Entities", [(ent.text, ent.label_) for ent in doc.ents])

        for ent in doc.ents:
            trait = ent.text
            value = ent.label_

        print("\n The value label (adjective)  is " + str(ent.text) + " and the field label (trait) is " +  str(ent.label_) + "\n")

        # #result_array = {"trait" : str(ent.label_), "adjective" :  str(ent.text)}

        # # for ent in doc.ents:
        # # 	print(ent.text, ent.start_char, ent.end_char, ent.label_)

        # displacy.render(doc, style='ent',jupyter=True)



        # Load the saved model and predict
        print("Loading from", output_dir)
        nlp_updated = spacy.load(output_dir)
        doc = nlp_updated(transcription) 
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
        result_array = {"trait" : str(ent.label_), "adjective" :  str(ent.text)}

        #send to backend
        return result_array



if __name__ == "__main__":
    main()
