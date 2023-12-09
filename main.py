from flask import Flask, render_template, request
from string import ascii_lowercase, digits
from random import choice
from bs4 import BeautifulSoup
import requests

tempmail = Flask(__name__)
API = 'https://www.1secmail.com/api/v1/'
domain_list = ['1secmail.com', '1secmail.org', '1secmail.net']
domain = choice(domain_list)
global email
email = ''


def generate_username():
    name = ascii_lowercase + digits
    username = ''.join(choice(name) for i in range(10))
    email = f'{username}@{domain}'
    return email


def check_mail():
    global email
    req_json_list = []
    req_empty_box = [{'from': 'отправитель',
                    'subject': 'тема',
                    'date': 'data',
                    'body': 'Нет входящих писем'}]
    if email == '':
        email = generate_username()
    try:
        r_link = f'https://www.1secmail.com/api/v1/?action=getMessages&login={email.split("@")[0]}&domain={email.split("@")[1]}'
        req = requests.get(r_link).json()
        volume = len(req)
        if volume != 0:
            id_list = []
            for id in req:
                for key, vol in id.items():
                    if key == 'id':
                        id_list.append(vol)
            for id in id_list:
                read_msg = f'https://www.1secmail.com/api/v1/?action=readMessage&login={email.split("@")[0]}&domain={email.split("@")[1]}&id={id}'
                r = requests.get(read_msg).json()
                print(r['body'])
                # r['body'] = '<html>' + r['body'] + '</html>'
                r['body'] = BeautifulSoup(r['body'], 'html.parser').get_text()
                req_json_list.append(r)
            return req_json_list
        else:
            return req_empty_box
    except:
        req_empty_box[0]['body'] = 'НЕТ СОЕДИНЕНИЯ С API!'
        return req_empty_box





@tempmail.route('/', methods = ['POST', 'GET'])
def index():
    global email
    if request.method == 'POST':
        email = generate_username()
    if email == '':
        email = generate_username()
    email = email
    return render_template('index.html', email=email)



@tempmail.route('/about')
def about():
    return render_template('about.html')


@tempmail.route('/mailbox')
def mailbox():
    global email
    mail = check_mail()
    return render_template('mailbox.html', box=mail, email=email)


if __name__ == "__main__":
    tempmail.run()

