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
    TRAIN_DATA = [
              ("Is your person wearing glasses?", {"entities": [(23,30,"glasses")]}),
              ("Do they have glasses?", {"entities": [(13,20,"glasses")]}),
              ("Does your person have glasses on?", {"entities": [(22,29,"glasses")]}),

              ("Is your person four-eyed?", {"entities": [(15,24,"glasses")]}),
              ("Is she four-eyed?", {"entities": [(7,16,"glasses")]}),

              ("Is she blond?", {"entities": [(7,12,"hair_color")]}),
              ("Is your person blond-haired?", {"entities": [(15,20,"hair_color")]}),
              ("Is he golden-haired?", {"entities": [(6,12,"hair_color")]}),
              ("Are they gold-haired?", {"entities": [(9,13,"hair_color")]}),
              ("Does your person have yellow hair?", {"entities": [(22,28,"hair_color")]}),
              ("Are they auburn-haired?", {"entities": [(9,15,"hair_color")]}),
              ("Is your person a ginger?", {"entities": [(17,24,"hair_color")]}),              
              
              ("Is your person wearing a green hat?", {"entities": [(25,30,"hat_color")]}),
              ("Are they wearing a green hat?", {"entities": [(19,24,"hat_color")]}),
              ("Does your person have a green hat?", {"entities": [(24,29,"hat_color")]}), 
              ("Do they have a green hat?", {"entities": [(15,20,"hat_color")]}),

              ("Does your person wear a hat?", {"entities": [(24,27,"hat")]}), 
              ("Do they wear a hat?", {"entities": [(15,18,"hat")]}), 
              ("Do they have a hat?", {"entities": [(15,18,"hat")]}), 

              ("Does your person not have head hair?", {"entities": [(17,35,"bald")]}),
              ("Is your person bald?", {"entities": [(15,19,"bald")]}),
              ("Is she bald?", {"entities": [(7,13,"bald")]}),
              ("Is he bald?", {"entities": [(6,10,"bald")]}),
              ("Does he not have head hair?", {"entities": [(8,26,"bald")]}),
              ("Does he not have hair on his head?", {"entities": [(8,33,"bald")]})  
        
              ("Is your person Dave?", {"entities": [(15,19,"character_guess")]}) 
              ("Is it Sarah?", {"entities": [(6,11,"character_guess")]}) 
              ("Is she Kelly?", {"entities": [(7,12,"character_guess")]}) 
              ("Is he Sam?", {"entities": [(6,9,"character_guess")]}) 
              ("Are they Alex?", {"entities": [(9,13,"character_guess")]}) 
              ("Is your character Harry?", {"entities": [(18,23,"character_guess")]})
              ("Sarah?", {"entities": [(0,5,"character_guess")]}) 
              ("James?", {"entities": [(0,5,"character_guess")]}) 
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
        for iteration in range(30):

            # shuufling examples  before every iteration
            # random.shuffle(TRAIN_DATA)
            # losses = {}
            # # batch up the examples using spaCy's minibatch
            # batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            # for batch in batches:
            #     texts, annotations = zip(*batch)
            #     nlp.update(
            #                 texts,  # batch of texts
            #                 annotations,  # batch of annotations
            #                 drop=0.5,  # dropout - make it harder to memorise data
            #                 losses=losses,
                # )
            # shuufling examples  before every iteration
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                for text, annotations in batch:
                    # create Example
                    doc = nlp.make_doc(text)
                    example = Example.from_dict(doc, annotations)
                    # Update the model
                    nlp.update([example], losses=losses, drop=0.3)
                    # from Spact 2.2.4, now on 3.0
                    # nlp.update(
                    #             texts,  # batch of texts
                    #             annotations,  # batch of annotations
                    #             drop=0.5,  # dropout - make it harder to memorise data
                    #             losses=losses,
                    #         )

    print("Losses", losses)
    
    #response form user passed to transcription variable
    transcription = speech_to_text()

    # Testing the model
    doc = nlp(transcription)
    print("\n Entities", [(ent.text, ent.label_) for ent in doc.ents])

    for ent in doc.ents:
        trait = ent.text
        value = ent.label_

    print("\n The value label (adjective)  is " + str(ent.text) + " and the field label (trait) is " +  str(ent.label_) + "\n")

    result_array = {"trait" : str(ent.label_), "adjective" :  str(ent.text)}

    # for ent in doc.ents:
    # 	print(ent.text, ent.start_char, ent.end_char, ent.label_)

    displacy.render(doc, style='ent',jupyter=True)

    return result_array

    # Save the  model to directory
    # output_dir = Path('/content/')
    # nlp.to_disk(output_dir)
    # print("Saved model to", output_dir)

    # # Load the saved model and predict
    # print("Loading from", output_dir)
    # nlp_updated = spacy.load(output_dir)
    # doc = nlp_updated("Fridge can be ordered in FlipKart" )
    # print("Entities", [(ent.text, ent.label_) for ent in doc.ents])



if __name__ == "__main__":
    main()
