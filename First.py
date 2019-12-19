from flask import Flask, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
FLASK_ENV = "development"

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

# Allows simpler python commands than full SQL syntax
DB = SQLAlchemy(APP)

@APP.route('/', methods = ['POST', 'GET'])
def home():
    return render_template('home.html', title = 'page with dog picture', picture = randomImage())

class Dog(DB.Model):
    id = DB.Column(DB.Integer, primary_key = True)
    url = DB.Column(DB.String(100))
    breed = DB.Column(DB.String(50))

@APP.route('/saved', methods = ['POST'])
def saved():
    dog = request.values['URL']
    breed = dog.split('/')[4]
    DB.session.add(Dog(url = dog, breed = breed))
    DB.session.commit()
    return render_template('home.html', picture = randomImage())

@APP.route('/reset')
def reset():
    DB.drop_all()
    DB.create_all()
    return 'DB reset'

@APP.route('/favorites')
def favorites():
    faves = Dog.query.with_entities(Dog.url)
    return render_template('faves.html', faves = faves)

@APP.route('/breeds')
def breeds_list():
    return render_template('breed_list.html', all_breeds = listBreeds())

def listBreeds():
    r=requests.get('https://dog.ceo/api/breeds/list/all')
    b=r.json()
    breeds=[]
    for key, value in b['message'].items():
        if len(value)==0:
            breeds.append(key)
        else:
            for breed in value:
                full= breed + ' ' + key
                breeds.append(full)
    return breeds

def randomImage(number=1):
    if number == 1:
        r=requests.get('https://dog.ceo/api/breeds/image/random')
    elif number <=50:
        r=requests.get('https://dog.ceo/api/breeds/image/random/'+str(number))
    else:
        raise ValueError('Max Number of Dogs Returned is 50')
    pics=r.json()['message']
    return pics

if __name__ == '__main__':
    APP.run()
