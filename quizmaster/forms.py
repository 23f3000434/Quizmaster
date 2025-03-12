from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, DateField, SelectField,FileField,TimeField
from wtforms.validators import Length, Email, DataRequired, EqualTo, ValidationError
from datetime import date
from quizmaster.models import User

class DateRange:
    def __init__(self, min=None, max=None, message=None):
        self.min = min
        self.max = max
        if not message:
            message = f'Date must be between {min} and {max}.'
        self.message = message

    def __call__(self, form, field):
        if field.data < self.min or field.data > self.max:
            raise ValidationError(self.message)

class Register(FlaskForm):
    Full_Name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=80)])
    Email = EmailField('Email Address', validators=[DataRequired(), Email(message='Invalid email address')])
    Qualification = StringField('Qualification', validators=[DataRequired(), Length(min=2)])
    Password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters')])
    Confirm_Password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('Password', message='Passwords must match')])
    dob = DateField('Date of Birth', validators=[DataRequired(), DateRange(min=date(1900, 1, 1), max=date.today())])
    Submit = SubmitField('Sign Up')
    
    def validate_Email(self, Email):
        user = User.query.filter_by(Email=Email.data).first()
        if user:
            raise ValidationError('That Email is already taken. Please enter some other email')

class Login(FlaskForm):
    Email = EmailField('Email Id', validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message="Enter minimum 8 characters")])
    Submit = SubmitField('Login')
    
class Newsubject(FlaskForm):
    Name = StringField('Name of Subject',validators=[DataRequired()])
    Description = StringField('Description')
    Submit = SubmitField('Submit')
    
class Newchapter(FlaskForm):
    Name = StringField('Name of Chapter', validators=[DataRequired()])
    Description = StringField('Description', validators=[DataRequired()])
    Submit = SubmitField('Submit')

class Newquestion(FlaskForm):
    Title = StringField('Title', validators=[DataRequired()])
    statement = StringField('Question Statement', validators=[DataRequired()])
    image = FileField('Question image if neccessary', validators=[DataRequired()])
    Submit = SubmitField('Upload')
    
class Newquiz(FlaskForm):
    Chapter_Id = SelectField('Chapter Id', validators=[DataRequired()])
    Date = DateField('Date', validators=[DataRequired()])
    Duration = TimeField('Time', validators=[DataRequired()])
    Save = SubmitField('Save')