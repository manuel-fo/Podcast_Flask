from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
import pprint
app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(300))
    episodes = db.relationship('Episode', backref='podcast')

    def __repr__(self):
        return '<Podcast %r>' % self.title

class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    link = db.Column(db.String(500), nullable=False)
    audio_url = db.Column(db.String(500), nullable=False, unique=True)
    time_published = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcast.id'))

    def __repr__(self):
        return '<Episode %r>' % self.title

podcasts = [
    {
        'name': 'Hello Internet',
        'description': 'A podcast about YouTube, technology, productivity, and other random stuff.',
        'episode': '131: This is a podcast'
    },
    {
        'name': 'The Daily',
        'description': 'A daily news podcast from the New York Times.',
        'episode': '200: Brexit Explained'
    }
]

@app.route("/")
@app.route("/home")
def home():
    pprint.pprint(Podcast.query.options(joinedload('episodes')))
    return render_template('home.html', podcasts=Podcast.query.all())

@app.route("/about")
def about():
    return render_template('about.html', title="About")

if __name__ == "__main__":
    app.run(debug=True)