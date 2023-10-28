from flask import Flask, render_template
from watchdog.events import EVENT_TYPE_OPENED

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
