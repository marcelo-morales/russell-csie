from flask import Flask, jsonify
from transcript_custom_ner import main

app = Flask(__name__)

@app.route('/')
def get_question():
    result = main()
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
