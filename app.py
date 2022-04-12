from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import EqualTo, Email, DataRequired, InputRequired, Length, ValidationError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.functions import database
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Tajny klucz' #Generowanie tajnego klucza
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
'''

Tworzymy formularz rejestracyjny, który dziedzi po klasie FlaskForm, nastepnie będziemy go przekazywać do funkcji registration
w postaci zmiennej form, która przyjmuje klase RegistrationForm().

'''

class RegistrationForm(FlaskForm):
    username = StringField('Type your username:', validators=[DataRequired(), Length(min=3, max=20)], render_kw={'placeholder': 'Username Field'})
    email = EmailField('Type your email: ', validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email Field'})
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Send!')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Sorry, this username is already used!')
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Sorry, this E-mail is already used!')

'''Tworzenie bazy danych'''

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    image_file = db.Column(db.String, nullable=False, default='img.jpg')
    
    def __repr__(self):
        return f"USER('{self.username}, '{self.email}', {self.image_file}'"
    
    


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        if database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
            db.create_all()
        else:
            db.session.add(user)
            db.session.commit()
            print(f'Dodano użytkownika do bazy danych użytkownika: {form.username.data}')
            return redirect(url_for('index')) 
    return render_template('registration.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
    
