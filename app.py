from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from form import SongForm
from tuneBuddy import songFinder
import git
import logging


app = Flask(__name__)
app.config['SECRET_KEY'] = 'cSuT6KxPuOayBkNnvTWXO0e0J'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///songs.db'

db = SQLAlchemy(app)


class Songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lyrics = db.Column(db.String(50), nullable=False)
    artist_name = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    first_possible_song = db.Column(db.String(100), nullable=False)
    second_possible_song = db.Column(db.String(100), nullable=False)
    third_possible_song = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Lyrics: {self.lyrics} matches with songs: {self.first_possible_song}, {self.second_possible_song}, and {self.third_possible_song}"

with app.app_context():
    db.create_all()


# Functionality to support website when hosted on pythonanywhere.com

# @app.route("/update_server", methods=['POST'])
# def webhook():
#     if request.method == 'POST':
#         repo = git.Repo('/home/spava001/SEO-Project-2-NEW')
#         origin = repo.remotes.origin
#         origin.pull()
#         return 'Updated PythonAnywhere successfully', 200
#     else:
#         return 'Wrong event type', 400


@app.route("/", methods=['GET', 'POST'])
def renderHome():
    form = SongForm()
    if form.validate_on_submit():
        try:
            lyrics = form.lyrics.data
            artist_name = form.artist_name.data
            genre = form.genre.data
            possible_songs = songFinder(lyrics, artist_name, genre)
            if artist_name == "":
                artist_name = "None"
            if genre == "":
                genre = "None"
            # Checks if no songs were found with the given lyrics
            if possible_songs == []:
                new_song_data = Songs(lyrics=lyrics, artist_name=artist_name, genre=genre, first_possible_song="None", second_possible_song="None", third_possible_song="None")
            else:
                new_song_data = Songs(lyrics=lyrics, artist_name=artist_name, genre=genre, first_possible_song=possible_songs[0], second_possible_song=possible_songs[1], third_possible_song=possible_songs[2])
            db.session.add(new_song_data)
            db.session.commit()
            logging.info(f"Song data was added successfully!")
            return render_template('home.html', page_title="Home", form=form, song_data=new_song_data)
        except Exception as e:
            logging.error(f"There was an error adding the data: {e}")
    
    return render_template('home.html', page_title='Home', form=form, song_data=None)


@app.route("/db")
def renderDatabase():
    all_songs_data = Songs.query.all()
    return render_template('database.html', page_title="Database", all_songs_data=all_songs_data)

@app.route('/delete-song/<int:id>')
def delete_song(id):
    song = Songs.query.get_or_404(id)

    try:
        db.session.delete(song)
        db.session.commit()
        return redirect(url_for('renderDatabase'))
    except Exception as e:
        logging.error(f"There was an error deleting that: {e}")
        return "There was an error deleting that!"
    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
