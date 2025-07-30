from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
from indic_transliteration.sanscript import transliterate, DEVANAGARI, BENGALI, ORIYA, TAMIL, TELUGU, KANNADA, MALAYALAM
import logging

app = Flask(__name__)

# Define transliteration scripts for supported Indian languages
TRANSLIT_SCRIPTS = {
    'hi': DEVANAGARI,
    'mr': DEVANAGARI,
    'ne': DEVANAGARI,
    'sa': DEVANAGARI,
    'bn': BENGALI,
    'or': ORIYA,
    'te': TELUGU,
    'ta': TAMIL,
    'kn': KANNADA,
    'ml': MALAYALAM
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text')
    source = data.get('source')
    target = data.get('target')

    try:
        # Perform translation
        translated = GoogleTranslator(source=source, target=target).translate(text)

        # Perform transliteration for supported Indian languages
        script = TRANSLIT_SCRIPTS.get(target.lower())
        if script:
            transliteration = transliterate(translated, script, 'itrans')
        else:
            transliteration = 'Transliteration not available for this language.'

        return jsonify({'translated': translated, 'transliteration': transliteration})

    except Exception as e:
        logging.exception("Translation failed:")
        return jsonify({'translated': f'Error: {str(e)}', 'transliteration': ''})

if __name__ == '__main__':
    app.run(debug=True)