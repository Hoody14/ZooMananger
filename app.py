from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from form import MyForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///animals.db'

db = SQLAlchemy(app)


class Animal(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(30))
    breed = db.Column(db.String(30))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(6))

    def to_dict(self):
        return {
            'id': self.id,
            'species': self.species,
            'breed': self.breed,
            'age': self.age,
            'gender': self.gender
        }


@app.route('/api/animals')
def get_animals():
    animal_species = request.args.get('species')
    animal_breed = request.args.get('breed')
    animal_age = request.args.get('age')
    animal_gender = request.args.get('gender')
    if animal_species and animal_age:
        animals = [animal.to_dict() for animal in Animal.query.filter(Animal.species == animal_species).filter(Animal.age == animal_age)]
    elif animal_species:
        animals = [animal.to_dict() for animal in Animal.query.filter(Animal.species == animal_species)]
    elif animal_breed:
        animals = [animal.to_dict() for animal in Animal.query.filter(Animal.breed == animal_breed)]
    elif animal_age:
        animals = [animal.to_dict() for animal in Animal.query.filter(Animal.age == animal_age)]
    elif animal_gender:
        animals = [animal.to_dict() for animal in Animal.query.filter(Animal.gender == animal_gender)]
    else:
        animals = [animal.to_dict() for animal in Animal.query.all()]
    return {'animals': animals, 'status_code': 200}


@app.route('/api/students/<int:id>')
def get_animal(id):
    animal = Animal.query.get(id)
    return {'animal': animal, 'status_code': 200}


@app.route('/api/animals', methods=['POST'])
def create_animal():
    data = request.get_json()
    species = data['species']
    breed = data['breed']
    age = data['age']
    gender = data['gender']
    animal = Animal(species=species, breed=breed, age=age, gender=gender)
    db.session.add(animal)
    db.session.commit()
    return "Successfully created", 201


@app.route('/api/animals/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    species = data['species']
    breed = data['breed']
    age = data['age']
    gender = data['gender']
    animal = Animal.query.get(id)
    if animal is not None:
        animal.species = species
        animal.breed = breed
        animal.age = age
        animal.gender = gender
        db.session.commit()
    return "Successfully updated", 200


@app.route('/api/animals/<int:id>', methods=['DELETE'])
def delete_animal(id):
    animal = Animal.query.get(id)
    db.session.delete(animal)
    db.session.commit()
    return "Successfully delete", 200

@app.route('/')
def index():
    animals = [animal.to_dict() for animal in Animal.query.all()]
    return render_template('index.html', animals=animals)

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = MyForm()
    if form.validate_on_submit():
        species = form.species.data
        breed = form.breed.data
        age = form.age.data
        gender = form.gender.data
        animal = Animal(species=species, breed=breed, age=age, gender=gender)
        db.session.add(animal)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('create.html', form=form)


@app.route('/success')
def success():
    return 'Form submitted successfully!'


# ქვემოთ ვქმნით აპლიკაციის კონტექსტს
# ამ კონტექსტში ვწერთ თუ როგორ უნდა დაისტარტოს ჩვენი API
# db.create_all() გადაიკითხავს ზემოთ განმარტებულ მოდელს და შექმნის მონაცემთა ბაზას ცხრილით students
# შემდეგ app.run() გაუშვებს აპლიკაციას დეფოლტ პორტზე 127.0.0.1:5000

with app.app_context():
    db.create_all()
