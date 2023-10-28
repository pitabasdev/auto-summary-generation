from flask import Flask, render_template, request, redirect, url_for
from watchdog.events import EVENT_TYPE_OPENED
from PIL import Image
import pytesseract
import nltk
nltk.download('all')


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' in request.files:
        uploaded_image = request.files['image']
        if uploaded_image.filename != '':
            image = Image.open(uploaded_image)
            text = pytesseract.image_to_string(image)
            from nltk.corpus import stopwords
            from nltk.tokenize import sent_tokenize, word_tokenize

            stop_words = set(stopwords.words('english'))
            words = word_tokenize(text)
            sentences = sent_tokenize(text)
            word_frequencies = {}
            for word in words:
                if word not in stop_words:
                    if word not in word_frequencies:
                        word_frequencies[word] = 1
                    else:
                        word_frequencies[word] += 1
            max_frequency = max(word_frequencies.values())
            for word in word_frequencies:
                word_frequencies[word] = word_frequencies[word] / max_frequency
            sentence_scores = {}
            for sentence in sentences:
                for word in word_tokenize(sentence.lower()):
                    if word in word_frequencies:
                        if sentence not in sentence-scores:
                            sentence_scores[sentence] = word_frequencies[word]
                        else:
                            sentence_scores[sentence] += word_frequencies[word]

            summary = max(sentence_scores, key=sentence_scores.get)

            return redirect(url_for('result', text=text, summary=summary))

    return "No image uploaded."


@app.route('/result')
def result():
    text = request.args.get('text')
    summary = request.args.get('summary')
    return render_template('index.html', extracted_text=text, summary=summary)


if __name__ == '__main__':
    app.run(debug=True)
