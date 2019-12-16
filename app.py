from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from flask_login import LoginManager, current_user, login_user, login_required, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
import podcastparser
import urllib.request
from rss_links import rss_links
import pprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)


class Playlist_Song(db.Model):
    id = db.Column(db.Integer, primary_key=Truef)
    playlist_id = db.Column(db.Integer, nullable=False)
    song_id = db.Column(db.Integer, nullable=False)


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


login = LoginManager(app)
app.config["SECRET_KEY"] = "podcaster"
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
            validators=[DataRequired(),
            EqualTo('password', message="The passwords must match")])
    submit = SubmitField('Register')


@app.route("/home")
def home():
    pprint.pprint(Podcast.query.options(joinedload('episodes')))
    return render_template('home.html', podcasts=Podcast.query.all(), title="Home")


@app.route("/playlists")
def playlists():
    if current_user.is_authenticated:
        return render_template('playlists.html', title="Playlist")
    flash('You must login before viewing your playlists', 'error')
    return redirect(url_for('login'))


@app.route("/<id>")
@app.route("/episodes/<id>")
def episodes(id):
    return render_template('episodes.html', title="Title", podcast=Podcast.query.filter(Podcast.id==id).first())


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data,
                    password=hash)
        emailExists = User.query.filter_by(email=form.email.data).first()
        userExists = User.query.filter_by(username=form.username.data).first()
        if(emailExists is None and userExists is None):
            db.session.add(user)
            db.session.commit()
            flash('Account successfully created, please login', 'success')
            return redirect(url_for('login'))
        if(emailExists):
            flash('That email is already in use, please login or use a different email', 'error')
        if(userExists):
            flash('That username is already in use, please login or use a different username', 'error')
    return render_template('register.html', title="Register", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in', 'info')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(form.email.data)
        pprint.pprint(user)
        if user is None or not user.check_password(form.password.data):
            flash('Incorrect Email or Password', 'error')
            return redirect(url_for('login'))
        login_user(user)
        flash('Successfully logged in', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('home')


@app.route("/reloadDB")
def reloadDB():
    refresh()
    return redirect('home')


def remove_html(text):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def refresh():
    for rss in rss_links:
        parsed = podcastparser.parse(rss, urllib.request.urlopen(rss), 10)
        title = parsed.get('title')
        description = remove_html(parsed.get('description'))
        image = parsed.get('cover_url')
        link = parsed.get('link')

        podcast = Podcast.query.filter_by(link=parsed.get('link')).first()

        if(podcast is None):
            podcast = Podcast(title=title, description=description, image=image, link=link)
            db.session.add(podcast)
            db.session.commit()

        for episode in parsed.get('episodes'):
            episode_title = episode.get('title')
            episode_link = episode.get('link')
            episode_audio_url = episode.get('enclosures')[0]['url']
            episode_time_published = episode.get('published')
            episode_length = episode.get('total_time')
            episode_podcast = podcast

            episode = Episode.query.filter_by(audio_url=episode_audio_url).first()

            if(episode is None):
                episode = Episode(title=episode_title,
                                    link=episode_link,
                                    audio_url=episode_audio_url,
                                    time_published=episode_time_published,
                                    length=episode_length,
                                    podcast=episode_podcast)
                db.session.add(episode)

        db.session.commit()
        # pprint.pprint(parsed)


if __name__ == "__main__":
    app.run(debug=True)
