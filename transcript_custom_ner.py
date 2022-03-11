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

#from gensim.parsing.preprocessing import remove_stopwords
#look into finding a way to remove stop words without anaconda, installation issues
#without using filtering out words library, i still dont catch umms and filler words, so 
#can just keep it like this?

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

    nlp = spacy.blank('en')  # create blank Language class
    print("Created blank 'en' model")
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner)
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

    # training data
    ## ORG - glasses
    ## DATE - hair_color
    ## NORP - hat_color
    ## GPE = hat
    ## LAW - bald
    TRAIN_DATA = [
                ("Is your person wearing glasses?", {"entities": [(23,30,"ORG")]}),
                ("Do they have glasses?", {"entities": [(13,20,"ORG")]}),
                ("Does your person have glasses on?", {"entities": [(22,29,"ORG")]}),

                ("Is your person four-eyed?", {"entities": [(15,24,"ORG")]}),
                ("Is she four-eyed?", {"entities": [(7,16,"ORG")]}),

                ("Is she blond?", {"entities": [(7,12,"DATE")]}),
                ("Is your person blond-haired?", {"entities": [(15,20,"DATE")]}),
                ("Is he golden-haired?", {"entities": [(6,12,"DATE")]}),
                ("Are they gold-haired?", {"entities": [(9,13,"DATE")]}),
                ("Does your person have yellow hair?", {"entities": [(22,28,"DATE")]}),
                ("Are they auburn-haired?", {"entities": [(9,15,"DATE")]}),
                ("Is your person a ginger?", {"entities": [(17,24,"DATE")]}),              
                
                ("Is your person wearing a green hat?", {"entities": [(25,30,"NORP")]}),
                ("Are they wearing a green hat?", {"entities": [(19,24,"NORP")]}),
                ("Does your person have a green hat?", {"entities": [(24,29,"NORP")]}), 
                ("Do they have a green hat?", {"entities": [(15,20,"NORP")]}),

                ("Does your person wear a hat?", {"entities": [(24,27,"GPE")]}), 
                ("Do they wear a hat?", {"entities": [(15,18,"GPE")]}), 
                ("Do they have a hat?", {"entities": [(15,18,"GPE")]}), 

                ("Does your person not have head hair?", {"entities": [(17,35,"LAW")]}),
                ("Is your person bald?", {"entities": [(15,19,"LAW")]}),
                ("Is she bald?", {"entities": [(7,13,"LAW")]}),
                ("Is he bald?", {"entities": [(6,10,"LAW")]}),
                ("Does he not have head hair?", {"entities": [(8,26,"LAW")]}),
                ("Does he not have hair on his head?", {"entities": [(8,33,"LAW")]})                                          
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
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                            texts,  # batch of texts
                            annotations,  # batch of annotations
                            drop=0.5,  # dropout - make it harder to memorise data
                            losses=losses,
                )
    print("Losses", losses)



    #auio to text transcription

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("these are the stopwords i will use \n")
    #print(stopwords.words('english'))
    #words_to_filter = set(stopwords.words('english'))
    
    instruction = "ask me question based on a specific attribute for my character"
    print(instruction)
    time.sleep(1)

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


    print("this is actual trascription " + response_from_user["transcription"])
    #response form user passed to transcription variable
    transcription = response_from_user["transcription"]

    # Testing the model
    doc = nlp(transcription)
    print("Entities", [(ent.text, ent.label_) for ent in doc.ents])


    # for ent in doc.ents:
    # 	print(ent.text, ent.start_char, ent.end_char, ent.label_)

    displacy.render(doc, style='ent',jupyter=True)

    ## ent.text ('blond') and ent.label ( 'hair_color') will then be sent to the game backend to check
    ##
    ## guess_trait = ent.label
    ## guess_adj = ent.text
    ## if guess_trait == guess_adj:
    ##		return affirmative_response

    # Save the  model to directory
    output_dir = Path('/content/')
    nlp.to_disk(output_dir)
    print("Saved model to", output_dir)

    # Load the saved model and predict
    print("Loading from", output_dir)
    nlp_updated = spacy.load(output_dir)
    doc = nlp_updated("Fridge can be ordered in FlipKart" )
    print("Entities", [(ent.text, ent.label_) for ent in doc.ents])



