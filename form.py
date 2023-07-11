from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional, Length

class SongForm(FlaskForm):
    lyrics = StringField('Enter Your Lyrics: ', validators=[DataRequired(), Length(min=3, max=150, message='Invalid lyric length. Must be between 3-50 characters.')], render_kw={"autocomplete": "off"})
    artist_name = StringField('Artist Name: ', validators=[Optional(), Length(min=3, max=50, message='Invalid artist name. Must be between 3-50 characters.')], render_kw={"autocomplete": "off"})
    genre = StringField('Genre: ', validators=[Optional(), Length(min=3, max=50, message='Invalid genre. Must be between 3-50 characters.')], render_kw={"autocomplete": "off"})
    submit = SubmitField('Find Your Song')