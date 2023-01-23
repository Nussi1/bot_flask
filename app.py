import os
import logging
from flask import Flask
from flask import request
from flask import Response
import requests
import dotenv
from library.flask.logging import FlaskLogging
from middleware.dbConnect import DBConnect

dotenv.load_dotenv()

TOKEN = os.getenv('TOKEN')

debug_mode = True if os.getenv('DEBUG_MODE') == '1' else False

if debug_mode:
    logging.basicConfig(filename='scraper.log', level=logging.DEBUG, format="{asctime} {levelname:<8} {message}",
                        style="{", datefmt="%d-%b-%y %H:%M:%S", filemode="w")


app = Flask(__name__)
app.wsgi_app = DBConnect(app.wsgi_app)


def get_file_path():
    return '/Users/nuraim/Desktop/Cover_letter.docx'


def get_log_data():
    try:
        with open("scraper.log", "r") as f:
            log_data = f.read()
    except:
        log_data = "Error reading log file"
    return log_data

def parse_message(message):
    print("message -->", message)
    try:
        chat_id = message["message"]["chat"]["id"]
        txt = message["message"]["text"]
        print("chat_id-->", chat_id)
        print("txt-->", txt)
        if not chat_id:
            raise ValueError("Invalid chat_id")
        return chat_id, txt
    except:
        print('No text found-->>')


def tel_send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    k = requests.post(url, json=payload)
    return k


def tel_send_log(chat_id, max_length = 1000):
    try:
        with open("scraper.log", "r") as f:
            log_data = f.read()
            log_data = log_data[-max_length:]
    except:
        log_data = "Error reading log file"
    tel_send_message(chat_id, log_data)



def tel_send_document(chat_id):
    file_path = get_file_path()
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    file = {'document': open(file_path, 'rb')}
    payload = {
        "chat_id": chat_id,
    }
    r = requests.post(url, json=payload, files=file)
    if r.status_code != 200:
        print(r.content)
    else:
        print(r.json())


app.add_url_rule('/logging', view_func=FlaskLogging.get, endpoint='logging_get', methods=['GET'])


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        print(msg)
        chat_id, txt = parse_message(msg)
        if txt == "hello":
            tel_send_message(chat_id, "Hello!")
        elif txt == "doc":
            tel_send_document(chat_id)
        elif txt == "log":
            tel_send_log(chat_id)
        else:
            tel_send_message(chat_id, "Hello, World!")

        return Response('ok', status=200)
    else:
        return "<h1>Hello!</h1>" 


if __name__ == "__main__":
    app.run('0.0.0.0', '5000', debug=True, threaded=True)
