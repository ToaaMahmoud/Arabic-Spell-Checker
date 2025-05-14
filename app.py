from flask import Flask, render_template, request, jsonify
from spellchecker import SpellChecker
from camel_tools.tokenizers.word import simple_word_tokenize

app = Flask(__name__)


spell = SpellChecker(language='ar')


def check_spelling(text):
    words = simple_word_tokenize(text)  
    misspelled = spell.unknown(words)
    corrections = {}


    for word in misspelled:
        suggestions = list(spell.candidates(word))
        corrections[word] = suggestions[:5]

    return corrections

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_spelling', methods=['POST'])
def check_spelling_api():
    text = request.json.get('text', '')
    suggestions = check_spelling(text)
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
