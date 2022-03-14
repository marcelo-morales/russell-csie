# russell-csie
Please see this colab (https://colab.research.google.com/drive/1XlB6MdMErjjFAI8GFYXBDQTAXFYKtJ5t?usp=sharing) for NLP progress.

# Installing Dependencies

To run our application, you need to make sure you have spaCy[https://spacy.io/usage] installed, which you can do by running the following prompts

  ```bash
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm
```

In addition, you will also need to install the SpeechRecognition[https://pypi.org/project/SpeechRecognition/] library by installing the corresponding dependency

  ```bash
pip install SpeechRecognition
```

# Text-To-Speech
  To test out this subsection, you can run 
  
  ```bash
python audio_transcript.py
```

and speak out loud to see your audio transcribed.

# Classification + Text-To-Speech

 To run the classification process on audio input from the user, you can run 
  
  ```bash
python transcript_custom_ner.py
```

and speak out loud to see your audio transcribed and the corresponding classification of field label (character trait) and value label (character adjective) outputted as well.



