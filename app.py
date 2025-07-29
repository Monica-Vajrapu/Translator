from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator

app = Flask(__name__)

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
        translated = GoogleTranslator(source=source, target=target).translate(text)
        return jsonify({'translated': translated})
    except Exception as e:
        return jsonify({'translated': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
