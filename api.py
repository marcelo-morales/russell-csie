from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from transcript_custom_ner import main
# from google.cloud import texttospeech
# import base64

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def get_question():
    result = main()
    response = jsonify(result)
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response

'''
@app.route('/audio/', methods=['POST', 'OPTIONS'])
@cross_origin()
def get_audio():
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()
    text = request.json['text']
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.MALE, name="en-US-Wavenet-A",
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    api_response = {
        "audioContent": str(base64.b64encode(response.audio_content))[2:-1]
    }

    to_return = jsonify(api_response)
    # to_return.headers.add('Access-Control-Allow-Origin', '*')
    return to_return
    
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response
'''