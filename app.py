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

TOKEN=os.getenv('TOKEN')

debug_mode = True if os.getenv('DEBUG_MODE') == '1' else False

if debug_mode:
    logging.basicConfig(filename='scraper.log', level=logging.DEBUG, format="%(asctime)s - %(message)s",
                        datefmt="%d-%b-%y %H:%M:%S")


app = Flask(__name__)
app.wsgi_app = DBConnect(app.wsgi_app)


def parse_message(message):
    print("message -->", message)
    try:
        chat_id = message["message"]["chat"]["id"]
        txt = message["message"]["text"]
        print("chat_id-->", chat_id)
        print("txt-->", txt)
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


def tel_send_document(chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    # document = open('/Users/nuraim/Desktop/Cover_letter.docx', 'rb')
    payload = {
        "chat_id": chat_id,
        "document": "/Users/nuraim/Desktop/reference.pdf"
    }
    k = requests.post(url, json=payload)
    return k


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
        else:
            tel_send_message(chat_id, "Hello, World!")

        return Response('ok', status=200)
    else:
        return "<h1>Hello!</h1>" 


if __name__ == "__main__":
    app.run('0.0.0.0', '5000', debug=debug_mode, threaded=True)
