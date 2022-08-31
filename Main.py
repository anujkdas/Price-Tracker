from flask import Flask
from flask_mail import Mail
from flask_mail import Message
from flask import render_template
from flask import request
from decouple import config
import requests
from bs4 import BeautifulSoup
import time

headers = {
    "User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
}

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "anujintern07@gmail.com"
app.config['MAIL_PASSWORD'] = config("PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route("/")
def index():
    return render_template('form.html')

@app.route("/data", methods=["POST"])
def data():
    form_data = request.form
    # print(form_data["Sender_email"])

    print(form_data)
    check(form_data)


def send_mail(data):
    msg = Message("Grab your product",
                sender=data["Sender_email"], 
                  recipients=[data["Reciever_email"]])
    pdt = data["link"]
    msg.body = "Hurry UP, Your product  " + pdt + " is available at the price you want"
    mail.send(msg)

def check_price(data):
    page = requests.get(data["link"], headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id="productTitle").get_text()
    price = soup.find(class_ = "a-offscreen").get_text()
    price = price.replace(',', '')
    Actual_price = float(price[1:])

    print(Actual_price)
    target_price = float(data["price"])

    print(target_price)
    if(Actual_price < target_price):
        send_mail(data)
        print("mail send")
        # return False


def check(data):
    while(True):
        check_price(data)
        time.sleep(60*60)


if __name__ == "__main__":
    app.run(debug=True)