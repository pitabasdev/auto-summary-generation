from flask import Flask, render_template, request, redirect, url_for
from watchdog.events import EVENT_TYPE_OPENED
from PIL import Image
import pytesseract

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


@app.route('/result')
def result():
    text = request.args.get('text')
    return render_template('index.html', extracted_text=text)


if __name__ == '__main__':
    app.run(debug=True)
