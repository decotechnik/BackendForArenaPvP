from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import EqualTo, Email, DataRequired, InputRequired, Length


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Tajny klucz' #Generowanie tajnego klucza
'''

Tworzymy formularz rejestracyjny, który dziedzi po klasie FlaskForm, nastepnie będziemy go przekazywać do funkcji registration
w postaci zmiennej form, która przyjmuje klase RegistrationForm().

'''

class RegistrationForm(FlaskForm):
    username = StringField('Type your username:', validators=[DataRequired(), Length(min=3, max=20)], render_kw={'placeholder': 'Username Field'})
    email = EmailField('Type your email: ', validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email Field'})
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Send!') #niepotrzebny 



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect('https://www.youtube.com/watch?v=I-c2WCCDLSw') 
    return render_template('registration.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)