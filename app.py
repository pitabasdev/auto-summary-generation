from flask import Flask, render_template, request, redirect, url_for
from watchdog.events import EVENT_TYPE_OPENED
from PIL import Image
import pytesseract
from summa import summarizer

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
            return redirect(url_for('result', text=text))

    return "No image uploaded."


@app.route('/generate_summary', methods=['POST'])
def generate_summary():
    if 'text' in request.form:
        input_text = request.form['text']
        summary = summarizer.summarize(input_text)
        return redirect(url_for('result', summary=summary))

    return "No text provided."


# @app.route('/summary')
# def summary():
#     summary = request.args.get('summary')
#     return render_template('index.html', summary=summary)


@app.route('/result')
def result():
    text = request.args.get('text')
    summary = request.args.get('summary')
    return render_template('index.html', extracted_text=text, summary=summary)


if __name__ == '__main__':
    app.run(debug=True)
