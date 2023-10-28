from flask import Flask, render_template
from watchdog.events import EVENT_TYPE_OPENED
from PIL import Image
import pytesseract
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route(/upload)
def upload():
         if 'image' in request.files:
            uploaded_image = request.files['image']
        if uploaded_image.filename != '':
            image = Image.open(uploaded_image)
            text = pytesseract.image_to_string(image)

if __name__ == '__main__':
    app.run(debug=True)
