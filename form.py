from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class SongForm(FlaskForm):
    lyrics = StringField('Enter your lyrics: ', validators=[DataRequired(), Length(min=3, max=150, message='Invalid lyric length. Must be between 3-50 characters.')])
    submit = SubmitField('Find Your Song')