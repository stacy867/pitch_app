# from .forms import UpdateProfile
from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField
from wtforms.validators import Required
from .. import db

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')
    
#Pitch Form
class PitchForm(FlaskForm):
    content = TextAreaField('Post Your Pitch')
    submit = SubmitField('Submit Pitch')    