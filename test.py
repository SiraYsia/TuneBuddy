import unittest
from flask import Flask
from flask.testing import FlaskClient
from app import app, db, Songs
from form import SongForm
from tuneBuddy import songFinder
from unittest.mock import patch

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def test_home_route(self):
        # Tests if the home route returns a successful response and checks if the response data contains the expected title tag for the home page.
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Home</title>', response.data)

    def test_songFinder(self):
        # Tests the songFinder function by passing lyrics and comparing the returned list of songs with the expected songs.
        lyrics = "save your tears"
        expected_songs = [
            "Here With Me By: d4vd",
            "Calling (Spider-Man: Across the Spider-Verse) (Metro Boomin & Swae Lee, NAV, feat. A Boogie Wit da Hoodie) By: Metro Boomin feat. Swae Lee, NAV & A Boogie Wit da Hoodie",
            "Save Your Tears (with Ariana Grande) (Remix) By: The Weeknd feat. Ariana Grande"
        ]
        songs = songFinder(lyrics)
        self.assertListEqual(songs, expected_songs)

    def test_add_song_to_database(self):
        # Tests adding a song to the database by creating a new song object, adding it to the database, and then retrieving it from the database to verify its presence and the correctness of its attributes.
        lyrics = "save your tears"
        expected_songs = [
            "Here With Me By: d4vd",
            "Calling (Spider-Man: Across the Spider-Verse) (Metro Boomin & Swae Lee, NAV, feat. A Boogie Wit da Hoodie) By: Metro Boomin feat. Swae Lee, NAV & A Boogie Wit da Hoodie",
            "Save Your Tears (with Ariana Grande) (Remix) By: The Weeknd feat. Ariana Grande"
        ]
        with app.app_context():
            possible_songs = songFinder(lyrics)
            new_song_data = Songs(
                lyrics=lyrics,
                first_possible_song=possible_songs[0],
                second_possible_song=possible_songs[1],
                third_possible_song=possible_songs[2]
            )
            db.session.add(new_song_data)
            db.session.commit()

            songs_from_db = Songs.query.filter_by(lyrics=lyrics).first()
            self.assertIsNotNone(songs_from_db)  
            self.assertEqual(songs_from_db.first_possible_song, expected_songs[0])
            self.assertEqual(songs_from_db.second_possible_song, expected_songs[1])
            self.assertEqual(songs_from_db.third_possible_song, expected_songs[2])

    def test_renderHome(self):
        # Tests the rendering of the home page by making a POST request to the home route with lyrics data and checking the status code for the response
        with app.test_client() as client:
            response = client.post('/', data={'lyrics': 'save your tears'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_renderDatabase(self):
        # Tests the rendering of the database page and verifies the presence of specific song data in the response.
        with app.app_context():
            with app.test_client() as client:
                with client.session_transaction() as session:
                    session['csrf_token'] = 'test_token'  # Set a CSRF token to pass validation

                song1 = Songs(lyrics="save your tears", first_possible_song="Song 1", second_possible_song="Song 2", third_possible_song="Song 3")
                song2 = Songs(lyrics="another song", first_possible_song="Song A", second_possible_song="Song B", third_possible_song="Song C")
                db.session.add(song1)
                db.session.add(song2)
                db.session.commit()

                response = client.get('/db')
                self.assertEqual(response.status_code, 200)

                self.assertIn(b'save your tears', response.data)
                self.assertIn(b'Song 1', response.data)
                self.assertIn(b'Song 2', response.data)
                self.assertIn(b'Song 3', response.data)
                self.assertIn(b'another song', response.data)
                self.assertIn(b'Song A', response.data)
                self.assertIn(b'Song B', response.data)
                self.assertIn(b'Song C', response.data)

    def CleanData(self):
        # Cleans up the database after each test by removing the session and dropping all tables.
        with app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
